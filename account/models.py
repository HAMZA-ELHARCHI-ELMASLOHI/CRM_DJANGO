from re import template
from django.db import models
from django.contrib.auth.models import AbstractUser 
# Create your models here.
from django.db.models.signals import post_save
from django.utils import timezone

'''class User(AbstractUser):
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
'''
###############################

class User(AbstractUser):
    class Types(models.TextChoices):
        MANAGER = "MANAGER", "Manager"
        CUSTOMER = "CUSTOMER", "Customer"

    base_type = Types.CUSTOMER

    # What type of user are we?
    type = models.CharField(
        ("Type"), max_length=50, choices=Types.choices, default=base_type
    )

    # First Name and Last Name Do Not Cover Name Patterns
    # Around the Globe.
    name = models.CharField(("Name of User"), blank=True, max_length=255)

    
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.type = self.base_type
    #     return super().save(*args, **kwargs)

    @property
    def more(self):
        return self.userprofile

class CustomermodelManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)


class CustomerMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gadgets = models.TextField()


class Customer(User):
    base_type = User.Types.CUSTOMER
    objects = CustomermodelManager()

    
    class Meta:
        proxy = True

    


class ManagermodelManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.MANAGER)

class ManagerMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    year = models.IntegerField()


class Manager(User):
    base_type = User.Types.MANAGER
    objects = ManagermodelManager()

    @property
    def more(self):
        return self.managermore

    class Meta:
        proxy = True

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