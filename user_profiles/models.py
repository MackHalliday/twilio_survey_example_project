from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    active= models.BooleanField(null=True, blank=True)

