from rest_framework import serializers
from .models import Book, Rental

# api/serializers.py
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'cover_image', 'is_available']
        extra_kwargs = {
            'cover_image': {'required': False}  # Makes cover_image optional
        }
class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'
        read_only_fields = ['user', 'rented_at', 'returned_at']
