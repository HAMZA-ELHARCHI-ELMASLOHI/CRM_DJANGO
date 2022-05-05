from multiprocessing import context
from urllib import request
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  City
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from account.mixins import ManagerRequiredMixin
from .forms import ProductModelForm, CategorieModelForm, OrderModelForm
from shop.models import Product, Order, Categorie

#User=get_user_model()
# Create your views here.

@login_required
def home(request):
    return render(request, 'dashboard/dash-base.html')

def pie_chart(request):
    labels = []
    data = []

    queryset = City.objects.order_by('-population')[:5]
    for city in queryset:
        labels.append(city.name)
        data.append(city.population)

    return render(request, 'dashboard/pie_chart.html', {
        'labels': labels,
        'data': data,
    })


class ProductListView(LoginRequiredMixin, generic.ListView):
    template_name = "dash-products/product-list.html"
    
    def get(self, *args, **kwargs):
        categorie=Categorie.objects.all()
        products=Product.objects.all()
        context = {
            'categories':categorie,
            'products':products
        }
        return render(self.request, 'dash-products/product-list.html', context)

class ProductCreateView(ManagerRequiredMixin, generic.CreateView):
    template_name = "dash-products/product-create.html"
    form_class = ProductModelForm

    def get_success_url(self):
        return reverse("dashboard:product-list")


class ProductUpdateView(ManagerRequiredMixin, generic.UpdateView):
    template_name = "dash-products/product-update.html"
    form_class = ProductModelForm

    def get_queryset(self):
        return Product.objects.all()
    def get_success_url(self):
        return reverse("dashboard:product-list")



class ProductDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "dash-products/product-delete.html"
    def get_success_url(self):
        return reverse("dashboard:product-list")
    def get_queryset(self):
        return Product.objects.all()

class CategorieCreateView(ManagerRequiredMixin, generic.CreateView):
    template_name = "dash-categories/categorie-create.html"
    form_class = CategorieModelForm

    def get_success_url(self):
        return reverse("dashboard:product-create")


class CategorieDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "dash-categories/categorie-delete.html"
    def get_success_url(self):
        return reverse("dashboard:categorie-create")
    def get_queryset(self):
        return Categorie.objects.all()

class CreateOrder(generic.View):
    def get(self, *args, **kwargs):
        cart=Cart.objects.get(user=self.request.user)
        items=CartItem.objects.filter(cart=cart)
        total_price=cart.get_cart_total
        context = {
            'items':items
        }
        order, created = Order.objects.get_or_create(
                name=self.__str__() ,
                user=self.request.user,
                total_price=total_price
            )
        

        for item in items:
            Orderitems.objects.create(order=order,name=item.product.name ,product=item.product, price=item.get_total, quantity=item.quantity)
        order.save()

        return render(self.request,  'products/product-list.html', context)

class OrdersCreateView(ManagerRequiredMixin, generic.CreateView):
    template_name = "dash-orders/order-create.html"
    form_class = OrderModelForm

    def get_success_url(self):
        return reverse("shop:order-list")

    


class OrdersUpdateView(ManagerRequiredMixin, generic.UpdateView):
    template_name = "dash-orders/order-update.html"
    form_class = OrderModelForm

    def get_queryset(self):
        return Order.objects.all()
    def get_success_url(self):
        return reverse("shop:order-list")



class OrdersDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "dash-orders/order-delete.html"
    def get_success_url(self):
        return reverse("shop:order-list")
    def get_queryset(self):
        return Order.objects.all()


