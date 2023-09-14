from rest_framework import serializers
from base.models import *
from .models import *
from base.serializer import CustomUserSerializer
import random
import string


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        


class CreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')



class CourseViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'







class VerifyTrainerFieldSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    image = serializers.ImageField()
    course_id = serializers.IntegerField()



class TrainerTimeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ['available_morning', 'available_evening']



class TrainerViewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    course = CourseViewSerializer()  # Use SerializerMethodField for custom representation

    class Meta:
        model = Trainer
        fields = ['id', 'user', 'course', 'trainer_photo', 'payment', 'available_evening', 'available_morning']




class PaymentViewSerializer(serializers.ModelSerializer):
    trainer = TrainerViewSerializer()
    user = CustomUserSerializer()

    class Meta:
        model = PaymentHistory
        fields  = ['id', 'user', 'trainer', 'purchased_date', 'payment_status', 'amount_paid']




class PurchasedOrderaSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    selected_trainer = TrainerViewSerializer()
    selected_course = CourseViewSerializer()
    class Meta:
        model = PurchasedOrder
        fields = ['id', 'user', 'selected_trainer', 'selected_course', 'time_slot', 'valid_up_to']


class MonthlyPaymentSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    total_payment = serializers.DecimalField(max_digits=10, decimal_places=2)