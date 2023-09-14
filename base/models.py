from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    




class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255,null=True,blank=True)
    mobile_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contain digits")
    mobile = models.CharField(validators=[mobile_regex], max_length=10 ,null=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='user/', null=True, blank=True)
    age_regex = RegexValidator(regex=r'^\d+$', message="Pincode should only contain digits")
    age = models.PositiveIntegerField(validators=[age_regex],null=True, blank=True)
    blood_group = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.user.email
    
    


