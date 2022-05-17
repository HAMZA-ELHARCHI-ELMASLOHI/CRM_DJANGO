import email
from django.db import models
from django.db.models.signals import post_save, post_delete


from account.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=20, null=True)
    email=models.EmailField(null=True)

    def __str__(self):
       return f"{self.name} "

    

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=20, null=True)
    email=models.EmailField(null=True)
    def __str__(self):
       return f"{self.name} "

    
        

class Csv(models.Model):
    file_name=models.FileField(upload_to='csvs')
    uploaded=models.DateTimeField(auto_now_add=True)
    activated=models.DateTimeField(auto_now=True)


def post_user_created_signal(sender, instance, created, **kwargs):
    if (created and instance.is_customer) or instance.is_customer:
        Customer.objects.update_or_create(user=instance, name=instance.username, email=instance.email)
    if (created and instance.is_manager) or instance.is_manager:
        Manager.objects.update_or_create(user=instance, name=instance.username, email=instance.email)

    '''if instance.is_manager and instance.is_customer==False:
        Customer.objects.filter(user=instance).delete()
    if instance.is_customer and instance.is_manager==False:
        Manager.objects.filter(user=instance).delete()'''
  
post_save.connect(post_user_created_signal, sender=User)

'''def post_user_deleted_signal(sender, instance, **kwargs):
    if instance.is_customer:
        Customer.objects.filter(user=instance).delete()
    if instance.is_manager:
        Manager.objects.filter(user=instance).delete()

post_delete.connect(post_user_deleted_signal, sender=User)
'''