from django.contrib import admin

from .models import Product, Categorie, Cart, CartItem, Order, Orderitems

# Register your models here.
admin.site.register(Product)


admin.site.register(Categorie)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Orderitems)