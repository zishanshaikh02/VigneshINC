from rest_framework.serializers import ModelSerializer
from api.models import User 
from rest_framework.serializers import ModelSerializer ,Serializer ,CharField ,EmailField,CharField
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username','is_active', 'is_staff',"is_verified")  # Add more fields as needed


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']




class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.get('password')

        if len(password) < 8:
            raise serializers.ValidationError("Password should be at least 8 characters long")

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password  # Use the validated password
        )
        return user

  
    

class VerifyUserSerializer(Serializer):

    email = CharField()
    otp = CharField()
    
class VerifyUserForgotSerializer(Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    password = serializers.CharField()
    # new_password = serializers.CharField()



class PasswordResetRequestSerializer(Serializer):
    email = EmailField()



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        print(user.is_authenticated)
       

        # Add custom claims
        data['email'] = user.email

        if user.is_active is None:
            raise serializers.ValidationError("User is not verified.")

        return data