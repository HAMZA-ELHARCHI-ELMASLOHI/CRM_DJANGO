from django import forms
from shop.models import Product, Order, Categorie, Orderitems, Customer
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

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=(
            '__all__'
        )
class CsvModelForm(forms.Form):    
    csv_file=forms.FileField()