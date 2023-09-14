from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Course)
admin.site.register(Trainer)
admin.site.register(PaymentHistory)
admin.site.register(PurchasedOrder)
admin.site.register(TrainerTimeAvailability)