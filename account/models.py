from re import template
from django.db import models
from django.contrib.auth.models import AbstractUser 
# Create your models here.

class User(AbstractUser):
    is_manager=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=True)

    phone_number = models.CharField(("phone number"), max_length=15, blank=True)


