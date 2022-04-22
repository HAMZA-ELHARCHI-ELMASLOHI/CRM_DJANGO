from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Categorie, Product, Cart, CartItem
from .forms import ProductModelForm, CategorieModelForm
# Product views

from account.mixins import ManagerRequiredMixin


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



class ProductCreateView(ManagerRequiredMixin, generic.CreateView):
    template_name = "products/product-create.html"
    form_class = ProductModelForm

    def get_success_url(self):
        return reverse("products:product-list")


class ProductUpdateView(ManagerRequiredMixin, generic.UpdateView):
    template_name = "products/product-update.html"
    form_class = ProductModelForm

    def get_queryset(self):
        return Product.objects.all()
    def get_success_url(self):
        return reverse("products:product-list")



class ProductDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "products/product-delete.html"
    def get_success_url(self):
        return reverse("products:product-list")
    def get_queryset(self):
        return Product.objects.all()


# Categories

class CategorieListView(ManagerRequiredMixin, generic.ListView):
    template_name = "categories/categorie-list.html"
    
    def get_queryset(self):
        return Categorie.objects.all()

    context_object_name='categories'

class CategorieCreateView(ManagerRequiredMixin, generic.CreateView):
    template_name = "categories/categorie-create.html"
    form_class = CategorieModelForm

    def get_success_url(self):
        return reverse("products:product-create")


class CategorieDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "categories/categorie-delete.html"
    def get_success_url(self):
        return reverse("products:categorie-create")
    def get_queryset(self):
        return Categorie.objects.all()


# Cart



class CartItemsView(generic.ListView):
    model = CartItem
    context_object_name='items'
    def get_queryset(self):
        cart=Cart.objects.get(user=self.request.user)
        return CartItem.objects.filter(user=self.request.user)

    template_name='cart/cart.html'


class CartItemsCreateView(ManagerRequiredMixin, generic.CreateView):
    template_name = "products/product-list.html"

    def get_queryset(self):
        cart=Cart.objects.get(user=self.request.user)
        product=Product.objects.get(name=self.request.name)
        return CartItem.objects.create(product=product, quantity=1, user=self.request.user)
    


class CartItemsDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "categories/categorie-delete.html"
    def get_success_url(self):
        return reverse("products:categorie-create")
    def get_queryset(self):
        return Categorie.objects.all()





def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    print(item)
    cart_item = CartItem.objects.create(
            product=item,
            user=request.user, 
        )
    
    cart_item.save()
    #messages.info(request, "This item quantity was updated.")
    return redirect("products:cart")

def delete_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    print(item)
    cart_item = CartItem.objects.filter(product=item).delete()
    print(cart_item)
    #messages.info(request, "This item quantity was updated.")
    return redirect("products:product-list")