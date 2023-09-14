from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import *

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if not user.is_verified:
            return AuthenticationFailed('User is not verified.')
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_active'] = user.is_active
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        return token
    

class UserRegisterationSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password", "is_verified")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    


class VerifyAccountSerializer(serializers.Serializer):
 
    email = serializers.EmailField()
    otp = serializers.CharField()
    




class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "first_name", "last_name"]







# class UserLoginSerializer(serializers.Serializer):
#     """
#     Serializer class to authenticate users with email and password.
#     """

#     email = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(**data)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Incorrect Credentials")


class UserProfileUpdateSerializer(serializers.ModelSerializer):


    class Meta:
        model= UserProfile
        fields= '__all__'


