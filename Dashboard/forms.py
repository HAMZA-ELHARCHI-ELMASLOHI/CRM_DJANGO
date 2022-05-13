from django import forms
from shop.models import Product, Order, Categorie, Orderitems
from .models import Csv

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
        model = Order
        fields = (
            'is_confirmed',
        )


class CsvModelForm(forms.Form):    
    csv_file=forms.FileField()
        