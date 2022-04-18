from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Categorie, Product
from .forms import ProductModelForm, CategorieModelForm
# Product views

class ProductListView(LoginRequiredMixin, generic.ListView):
    template_name = "products/product-list.html"
    
    def get_queryset(self):
        return Product.objects.all()

    context_object_name='products'

class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "products/product-detail.html"
    
    def get_queryset(self):
        return Product.objects.all()

    context_object_name='products'



class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "products/product-create.html"
    form_class = ProductModelForm

    def get_success_url(self):
        return reverse("products:product-list")


class ProductUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "products/product-update.html"
    form_class = ProductModelForm

    def get_queryset(self):
        return Product.objects.all()
    def get_success_url(self):
        return reverse("products:product-list")



class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "products/product-delete.html"
    def get_success_url(self):
        return reverse("products:product-list")
    def get_queryset(self):
        return Product.objects.all()


# Categories

class CategorieListView(LoginRequiredMixin, generic.ListView):
    template_name = "categories/categorie-list.html"
    
    def get_queryset(self):
        return Categorie.objects.all()

    context_object_name='categories'

class CategorieCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "categories/categorie-create.html"
    form_class = CategorieModelForm

    def get_success_url(self):
        return reverse("products:product-create")


class CategorieDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "categories/categorie-delete.html"
    def get_success_url(self):
        return reverse("products:categorie-create")
    def get_queryset(self):
        return Categorie.objects.all()