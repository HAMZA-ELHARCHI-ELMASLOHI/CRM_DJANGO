import email
from django.db import models
from django.db.models.signals import post_save


from account.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=20, null=True)
    email=models.EmailField(null=True)

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=20, null=True)
    email=models.EmailField(null=True)

class Country(models.Model):
    name = models.CharField(max_length=30)

class City(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    population = models.PositiveIntegerField()


def post_user_created_signal(sender, instance, created, **kwargs):
    if created and instance.is_customer:
        Customer.objects.create(user=instance, name=instance.username, email=instance.email)
    if created and instance.is_manager:
        Manager.objects.create(user=instance, name=instance.username, email=instance.email)

post_save.connect(post_user_created_signal, sender=User)