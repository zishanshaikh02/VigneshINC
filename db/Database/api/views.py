

from django.shortcuts import render


# Create your views here.

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import UserSerializer, MyTokenObtainPairSerializer
from api.models import User
from rest_framework import generics, permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny ,IsAuthenticated
from .serializer import CustomUserSerializer ,VerifyUserSerializer 
from .models import User
from rest_framework.decorators import api_view ,permission_classes
from .email import send_mail_via_email  ,send_forget_password_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view ,throttle_classes
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from random import randint
from .serializer import VerifyUserForgotSerializer






class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)

@permission_classes([IsAuthenticated])
class GetUserView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    





    #################
@api_view(["POST"])
def registration_view(request):
    # Check if the email exists in the database but is not verified
    email = request.data.get('email')
    existing_user = User.objects.filter(email=email, is_verified=False).first()

    if existing_user:
        # Send OTP to the existing user
        send_mail_result = send_mail_via_email(email)
        
        if send_mail_result:
            return Response({"message": "OTP sent to your Email Address"}, status=status.HTTP_201_CREATED)
    else:
        # Register a new user
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            email = serializer.validated_data['email']
            send_mail_result = send_mail_via_email(email)

            if send_mail_result:
                return Response({"message": "OTP sent to your Email Address"}, status=status.HTTP_201_CREATED)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(["POST"])
# @permission_classes([AllowAny])

def verify_otp(request):

    data = request.data 
    print(data)
    serializer = VerifyUserSerializer(data = data)


    if serializer.is_valid():

        email =  serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        print(email,otp)

        try:
            user = User.objects.filter(email =email)
            print(user)
            
        except User.DoesNotExist as e:

            return Response({"status": 400, "message": "Check Your email Correctly {e}"})
            

        
        if not user[0].otp == otp:
            return Response({"status": 400, "message": "Enter OTP is Incorrect"})

        user = user.first()
        user.is_verified = True
        user.is_active = True
        user.save()

        return Response(
            {
                "status": 200,
                "message": "Succuessfully registered ",
                    
            }
        )



@api_view(['POST'])
def password_reset_confirm(request):
    data = request.data
    serializer = VerifyUserForgotSerializer(data=data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['password']

        user = User.objects.filter(email=email)

        if not user.exists():
            return Response({"status": 400, "message": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        user = user.first()

        if not user.otp == otp:
            return Response({"status": 400, "message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        if not new_password:
            return Response({'detail': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password and save the user
        user.set_password(new_password)
        user.save()

        # Authenticate the user with the new password
        user = authenticate(request, email=user.email, password=new_password)

        if user:
            return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Password reset failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'detail': 'Invalid data submitted.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@throttle_classes([UserRateThrottle])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'detail': 'No user with this email address'}, status=400)


    try:
        send = send_forget_password_mail(email)

        if send == True :
            return Response({'detail': 'Password reset email sent successfully'}, status=200)
       

        
    except Exception as e:
        return Response({'detail': 'Failed to send reset email'}, status=500)

    return Response({'detail': 'Password reset email sent successfully'}, status=200)






from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 404:
        # Customize the 404 response here
        custom_response_data = {'detail': 'Not found'}
        response.data = custom_response_data

    return response
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 404:
        # Customize the 404 response here
        custom_response_data = {'detail': 'Not found'}
        response.data = custom_response_data

    return response