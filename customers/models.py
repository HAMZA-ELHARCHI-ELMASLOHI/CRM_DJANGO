from django.db import models

# Create your models here.

class Customer(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone_number=models.CharField(max_length=20)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    pass
