from django.db import models
from base.models import CustomUser
from django.utils import timezone
from django.db.models import F
from datetime import timedelta


# Create your models here.


class Course(models.Model):
    course_name = models.CharField(max_length=250)
    description = models.TextField()
    course_fee = models.PositiveBigIntegerField()
    course_image = models.FileField(upload_to='Courseimages/',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)



    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.course_name
    


class Trainer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    trainer_photo = models.ImageField(upload_to='trainer_photos/')
    description = models.CharField(max_length=255,null=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    available_morning = models.BooleanField(default=False)
    available_evening = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
    


class TrainerTimeAvailability(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    upper_limit = models.PositiveIntegerField()
    
    
    def __str__(self):
        return f"{self.trainer.user.username} - {self.start_time} to {self.end_time}"
    



class PaymentHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True)
    amount_paid = models.PositiveBigIntegerField()
    purchased_date=models.DateTimeField(auto_now_add=True)
    payment_status=models.BooleanField(default=False)

    
    

    def __str__(self):
        return self.user.email
    
    class Meta:
        ordering = ['-purchased_date']



class PurchasedOrder(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    selected_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True)
    selected_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    time_slot = models.CharField(max_length=100, null=True, blank=True)
    valid_up_to = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.email
    
    
