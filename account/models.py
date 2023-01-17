from re import template
from django.db import models
from django.contrib.auth.models import AbstractUser 
# Create your models here.
from django.db.models.signals import post_save
from django.utils import timezone



class User(AbstractUser):
    class Types(models.TextChoices):
        MANAGER = "MANAGER", "Manager"
        CUSTOMER = "CUSTOMER", "Customer"

    base_type = Types.CUSTOMER

    type = models.CharField(
        ("Type"), max_length=50, choices=Types.choices, default=base_type
    )

    name = models.CharField(("Name of User"), blank=True, max_length=255)

    @property
    def more(self):
        return self.userprofile

class CustomermodelManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)





class Customer(User):
    base_type = User.Types.CUSTOMER
    objects = CustomermodelManager()

    
    class Meta:
        proxy = True


class ManagermodelManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.MANAGER)




class Manager(User):
    base_type = User.Types.MANAGER
    objects = ManagermodelManager()


    class Meta:
        proxy = True

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    image = models.ImageField(default='images/default.png', upload_to='images/profile')
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