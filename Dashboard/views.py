from multiprocessing import context
from urllib import request
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from account.mixins import ManagerRequiredMixin
from .models import   Customer, Manager
from django.contrib.auth import get_user_model
from .forms import ProductModelForm, CategorieModelForm, OrderModelForm
from shop.models import Product, Order, Categorie, Orderitems
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.db import IntegrityError
from django.http import HttpResponseRedirect

#User=get_user_model()
# Create your views here.



class Home(ManagerRequiredMixin, generic.TemplateView):
    template_name='dashboard/dash-base.html'

class Pie_chart(ManagerRequiredMixin, generic.View):
    def get(self,request):
        labels = []
        data = []

        queryset = Product.objects.order_by('-price')
        for q in queryset:
            print(q.name)
            print(q.price)

            labels.append(q.name)
            data.append(int(q.price))

        return render(request, 'dashboard/pie_chart.html', {
            'labels': labels,
            'data': data,
        })

class ProductListView(ManagerRequiredMixin, generic.ListView):
    template_name = "dash-products/product-list.html"
    
    def get(self, *args, **kwargs):
        categorie=Categorie.objects.all()
        products=Product.objects.all()
        context = {
            'categories':categorie,
            'products':products
        }
        return render(self.request, 'dash-products/product-list.html', context)

class ProductCreateView( ManagerRequiredMixin, generic.CreateView):
    template_name = "dash-products/product-create.html"
    form_class = ProductModelForm

    def get_success_url(self):
        messages.success(self.request, ' created successfully')
        return reverse("dashboard:product-list")
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, 'something went Wrong')
        return self.render_to_response(self.get_context_data(form=form))
        



class ProductUpdateView(ManagerRequiredMixin, generic.UpdateView):
    template_name = "dash-products/product-update.html"
    form_class = ProductModelForm

    def get_queryset(self):
        return Product.objects.all()
    def get_success_url(self):
        messages.success(self.request, ' updated successfully')
        return reverse("dashboard:product-list")

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, 'something went Wrong')
        return self.render_to_response(self.get_context_data(form=form))



class ProductDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "dash-products/product-delete.html"
    def get_success_url(self):
        return reverse("dashboard:product-list")
    def get_queryset(self):
        return Product.objects.all()
        
    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, ' deleted successfully')
            return HttpResponseRedirect(success_url)
        except IntegrityError as e:
            messages.warning(self.request, "you can't remove product")
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, 'something went Wrong')
        return self.render_to_response(self.get_context_data(form=form))


class CategorieCreateView(ManagerRequiredMixin, generic.CreateView):
    template_name = "dash-categories/categorie-create.html"
    form_class = CategorieModelForm

    def get_success_url(self)  :
        return reverse("dashboard:product-create")


class CategorieDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "dash-categories/categorie-delete.html"
    def get_success_url(self):
        return reverse("dashboard:categorie-create")
    def get_queryset(self):
        return Categorie.objects.all()

class CategorieDetailView(ManagerRequiredMixin, generic.DetailView):
    template_name = "dash-categories/categorie-detail.html"
    
    def get(self, *args, **kwargs):
        categorie_id = self.kwargs['pk']
        categorie=Categorie.objects.get(id=categorie_id)
        items=Product.objects.filter(categorie=categorie)
        context = {
            'categorie':categorie,
            'items':items
        }
        return render(self.request, 'dash-categories/categorie-detail.html', context)

class OrderListView(ManagerRequiredMixin, generic.ListView):
    
    def get(self, *args, **kwargs):
        customer =Customer.objects.get(user=self.request.user)
        orders=Order.objects.filter(customer=customer)

        context = {
            'orders': orders,
            'customer':customer
        }
        return render(self.request, 'dash-orders/order-list.html', context)


class CreateOrder(ManagerRequiredMixin,generic.View):
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





class OrderDetailView(ManagerRequiredMixin, generic.DetailView):
    template_name = "dash-orders/order-detail.html"

    def get(self, *args, **kwargs):
        order_id = self.kwargs['pk']
        order=Order.objects.get(id=order_id)
        items=Orderitems.objects.filter(order=order)
        context = {
            'orders':order,
            'items':items
        }
        return render(self.request, 'dash-orders/order-detail.html', context)


    context_object_name='orders'
    


class OrdersUpdateView(ManagerRequiredMixin, generic.UpdateView):
    template_name = "dash-orders/order-update.html"
    form_class = OrderModelForm

    def get_queryset(self):
        return Order.objects.all()
    def get_success_url(self):
        return reverse("dashboard:order-list")



class OrdersDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "dash-orders/order-delete.html"
    def get_success_url(self):
        return reverse("shop:order-list")
    def get_queryset(self):
        return Order.objects.all()


class CustomerListView(ManagerRequiredMixin, generic.ListView):
    template_name = "dash-customer/customer-list.html"
    
    def get(self, *args, **kwargs):
        customers=Customer.objects.all()
        context = {
            'customers':customers,
        }
        return render(self.request, 'dash-customer/customer-list.html', context)


class CustomerDetailView(ManagerRequiredMixin, generic.DetailView):
    template_name = "dash-customer/customer-detail.html"
    
    def get(self, *args, **kwargs):
        customer_id = self.kwargs['pk']
        customer=Customer.objects.get(id=customer_id)
        orders=Order.objects.filter(customer=customer)
        context = {
            'customer':customer,
            'orders':orders
        }
        return render(self.request, 'dash-customer/customer-detail.html', context)


def upload_csv(request):
    pass