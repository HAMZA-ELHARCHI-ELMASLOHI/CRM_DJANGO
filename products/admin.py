from django.contrib import admin

from .models import Product, Categorie, Cart, CartItem

# Register your models here.
admin.site.register(Product)


admin.site.register(Categorie)
admin.site.register(Cart)
admin.site.register(CartItem)