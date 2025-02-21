

from django.db import models
from rest_framework import serializers
from .models import Menu, Booking
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return {'status': 'success', 'message': 'Login successful'}
    
class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['title', 'price', 'inventory', 'category_fk']
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'name', 'no_of_guests', 'time_slot', 'booking_date']