from django import forms

from .models import Product, Categorie, Order, Orderitems

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
            'Adresse',
            'zipcode'
        )

    
'''class OrderForm(forms.Form):
    class Meta:
        model = Order
        fields = (
            'Adresse',
            'zipcode'
        )'''

class OrderForm(forms.Form):
    Adresse = forms.CharField(label='adresse ', max_length=100)
    zipcode =forms.IntegerField(label='Zip code')
    costumer_phone=forms.IntegerField(label='costumer_phone')