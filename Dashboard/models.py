import email
from django.db import models

from django.db.models.signals import post_save

from account.models import User
# Create your models here.



class Customer(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone_number=models.CharField(max_length=20)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    name=models.CharField(max_length=50)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    categorie=models.ForeignKey('Categories', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    
class Categories(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Order(models.Model):
    pass





class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username





def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User) 