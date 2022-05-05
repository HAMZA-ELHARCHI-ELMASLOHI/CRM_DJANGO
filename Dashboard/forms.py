from django import forms
from shop.models import Product, Order, Categorie, Orderitems

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'product_image',
            'description',
            'categorie',
            'price',
        )


class CategorieModelForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = (
            'name',
        )


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Orderitems
        fields = (
            'product',
        )