from re import template
from django.db import models
from django.contrib.auth.models import AbstractUser 
# Create your models here.
from django.db.models.signals import post_save
from django.utils import timezone

class User(AbstractUser):
    is_manager=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=True)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    image = models.ImageField(default='default.png', upload_to='images/profile')
    name=models.CharField(max_length=20, null=True)
    first_name=models.CharField(max_length=20, null=True)
    last_name=models.CharField(max_length=20, null=True)

    email=models.EmailField(null=True)
    born=models.DateTimeField(('born date'), editable=True, null=True)
    adresse=models.CharField(max_length=100, null=True)
    phone_number = models.CharField(("phone number"), max_length=15, blank=True)

    def __str__(self):
        return self.user.username




def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, name=instance.username)

post_save.connect(post_user_created_signal, sender=User) 
