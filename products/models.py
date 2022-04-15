from django.db import models

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=50)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    categorie=models.ForeignKey('Categorie', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    
class Categorie(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name
