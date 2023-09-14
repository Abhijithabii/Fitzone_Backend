from django.shortcuts import render
from django.conf import settings

# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
import stripe


from . import serializer
from .emails import *

from rest_framework.views import APIView
from django.http import Http404

from rest_framework.parsers import MultiPartParser



from .serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


User = get_user_model()

class UserRegisterationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializer.UserRegisterationSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_mail(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': 'Registration successful check your email',
                    'data': serializer.data,
                })
        
            return Response({
                'status': 400,
                'message': 'Something Went Wrong',
                'data': serializer.errors,
            })
        except Exception as e:
            print(e)

class VerifyOTP(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializer.VerifyAccountSerializer

    def post(self, request):
        try:
            print(request.data,'----------rrrrrrrrrr')
            data_serializer = self.get_serializer(data=request.data)
            data_serializer.is_valid(raise_exception=True)  

            email = data_serializer.validated_data['email']
            otp = data_serializer.validated_data['otp']

            user = CustomUser.objects.filter(email=email)
            print(user,'-----------user')
            if not user.exists():
                return Response({
                    'status': 400,
                    'message': 'Something Went Wrong',
                    'data': 'invalid email',
                })

            if not user[0].otp == otp:
                print('------otp error')
                return Response({
                    'status': 400,
                    'message': 'Something Went Wrong',
                    'data': 'wrong otp',
                })

            user = user.first()
            user.is_verified = True
            user.otp = ''
            user.save()
            UserProfile.objects.create(user=user)
            print('----mission sucess----')

            return Response({
                'status': 200,
                'message': 'Account Verified',
                'data': {},
            })

        except Exception as e:
            print(e)

            return Response({
                'status': 500,
                'message': 'Internal Server Error',
                'data': str(e),
            })
        


class UserProfileUpdateView(APIView):

    parser_classes = [MultiPartParser]

    def get_user(self,id):
        try:
            return CustomUser.objects.get(id=id)
        except UserProfile.DoesNotExist:
            raise Http404
        

    def get(self, request, id, format=None):
        user = self.get_user(id)
        serializer = UserProfileUpdateSerializer(user.profile)
        
        return Response(serializer.data)
    

    def put(self, request, id, format=None):
        user = self.get_user(id)
        
        serializer = UserProfileUpdateSerializer(user.profile, data=request.data)
        
        if serializer.is_valid():
           
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors,'-----errrrrrrr')
        return Response(serializer.errors, status=400)
        



class PasswordChangeView(APIView):
    def put(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        print(user, '-------usergot')
        print(current_password, '--------curent pas')
        print(new_password, '------newwwwwww pass')

        if not user.check_password(current_password):
            print("Current password error")
            return Response({"message": "Current password is incorrect"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
