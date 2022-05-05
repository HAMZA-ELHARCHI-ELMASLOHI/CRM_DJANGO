from distutils.command.upload import upload
from email.policy import default
from django.db import models
from account.models import User
from Dashboard.models import Customer
from django.db.models.signals import post_save
import uuid
from django.shortcuts import reverse
from django.core.mail import send_mail
# Create your models here.

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=50)
    product_image=models.ImageField(default='images/products/product-default.png', upload_to='images/products/')
    description = models.TextField()
    #date_added = models.DateTimeField(auto_now_add=True)
    categorie=models.ForeignKey('Categorie', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("shop:product-list", kwargs={
            'id': self.id
        })

    def get_add_to_cart_url(self):
        return reverse("shop:add-to-cart", kwargs={
            'id': self.id
        })
    def get_remove_from_cart_url(self):
        return reverse("shop:remove-from-cart", kwargs={
            'id': self.id
        })
    def get_delete_from_cart_url(self):
        return reverse("shop:delete-from-cart", kwargs={
            'id': self.id
        })
    def __str__(self):
        return self.name


    
class Categorie(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
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
        return reverse("shop:add-to-cart", kwargs={
            'id': self.id
        })
    def get_remove_from_cart_url(self):
        return reverse("shop:remove-from-cart", kwargs={
            'id': self.id
        })
    def get_delete_from_cart_url(self):
        return reverse("shop:delete-from-cart", kwargs={
            'id': self.id
        })

    @property
    def get_cart_total(self):
        cart=Cart.objects.get(user=self.user)

        orderitems = CartItem.objects.filter(cart=cart)
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_total_items(self):
        cart=Cart.objects.get(user=self.user)

        orderitems = CartItem.objects.filter(cart=cart)
        total = sum([item.quantity for item in orderitems])
        return total 

    def __str__(self):
            return  self.user.username + '-cart'



	    



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,default='1')
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
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def unit_price(self):

        total = self.price/ self.quantity
        return total 

    def __str__(self):
        return str(self.id)



def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User) 


def order_created_signal(sender, instance, created, **kwargs):
    if created:
        print('listner work ')
        #send_mail('a odrer has been created', 'see on website', 'hamza', recipient_list)


post_save.connect(order_created_signal, sender=Order) 