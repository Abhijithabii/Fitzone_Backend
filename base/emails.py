from django.core.mail import send_mail
import random
from django.conf import settings
from .models import *




def send_otp_via_mail(email):
    subject = 'Your Account verification Email'
    otp = random.randint(100000 , 999999)
    message = f' Your otp is {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])

    user_obj = CustomUser.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()

 