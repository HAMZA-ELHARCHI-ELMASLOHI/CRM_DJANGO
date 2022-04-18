from django import forms

from .models import Product, Categorie

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'product_image',
            'description',
            'categorie',
        )


class CategorieModelForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = (
            'name',
        )
