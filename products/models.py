from distutils.command.upload import upload
from email.policy import default
from django.db import models
from account.models import User

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=50)
    product_image=models.ImageField(default='images/products/product-default.png', upload_to='images/products/')
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    categorie=models.ForeignKey('Categorie', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
class Categorie(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
