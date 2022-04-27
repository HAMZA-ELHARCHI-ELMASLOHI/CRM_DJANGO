from distutils.command.upload import upload
from email.policy import default
from django.db import models
from account.models import User
from django.db.models.signals import post_save

from django.shortcuts import reverse
# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=50)
    product_image=models.ImageField(default='images/products/product-default.png', upload_to='images/products/')
    description = models.TextField()
    #date_added = models.DateTimeField(auto_now_add=True)
    categorie=models.ForeignKey('Categorie', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("products:product-list", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("products:add-to-cart", kwargs={
            'slug': self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse("products:remove-from-cart", kwargs={
            'slug': self.slug
        })
    def get_delete_from_cart_url(self):
        return reverse("products:delete-from-cart", kwargs={
            'slug': self.slug
        })
    def __str__(self):
        return self.name

    
class Categorie(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):  
            return  " item " + self.product.name

    
    
    
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #created_at = models.DateTimeField(auto_now_add=True)
    #items = models.ManyToManyField(CartItem)

    def get_add_to_cart_url(self):
        return reverse("products:add-to-cart", kwargs={
            'slug': self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse("products:remove-from-cart", kwargs={
            'slug': self.slug
        })
    def get_delete_from_cart_url(self):
        return reverse("products:delete-from-cart", kwargs={
            'slug': self.slug
        })

    @property
    def get_cart_total(self):
        cart=Cart.objects.get(user=self.user)

        orderitems = CartItem.objects.filter(cart=cart)
        total = sum([item.get_total for item in orderitems])
        return total 

    def __str__(self):
            return  self.user.username + '-cart'



	    



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    name=models.CharField(max_length=50)
    #items=models.ManyToManyField(CartItem)
    total_price= models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
            return  self.user.username+str(self.id) + '-order'


class Orderitems(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)

    name=models.CharField(max_length=50)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)



def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User) 


