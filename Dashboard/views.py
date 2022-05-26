from multiprocessing import context
from urllib import request
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from account.mixins import ManagerRequiredMixin, AdminRequiredMixin
from .models import    Csv
from django.contrib.auth import get_user_model
from .forms import ProductModelForm, CategorieModelForm, OrderModelForm, CsvModelForm, CustomerModelForm
from shop.models import Product, Order, Categorie, Orderitems
from account.models import UserProfile, Manager, Customer
from account.forms import ProfileModelForm
from django.contrib import messages

from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse

import csv
#User=get_user_model()
# Create your views here.



class Home(ManagerRequiredMixin, generic.View):
    template_name='dashboard/dash-base.html'
    def get(self, *args, **kwargs):
        categorie=Categorie.objects.count()
        products=Product.objects.count()
        orders=Order.objects.filter(is_confirmed=True).count()
        customers=Customer.objects.count()
        profile=UserProfile.objects.get(user=self.request.user)
        labels = []
        data = []

        queryset = Product.objects.order_by('-price')
        for q in queryset:

            labels.append(q.name)
            data.append(int(q.price))
        context = {
            'categories':categorie,
            'products':products,
            'orders':orders,
            'customers':customers,
            'profile':profile,
            'labels': labels,
            'data': data,
        }
        return render(self.request, 'dashboard/dash-base.html', context)

class StatisticView(ManagerRequiredMixin, generic.View):
    template_name = "dash-products/home.html"
    
    def get(self, *args, **kwargs):
        categorie=Categorie.objects.count()
        products=Product.objects.count()
        orders=Order.objects.count()
        labels = []
        data = []

        queryset = Product.objects.order_by('-price')
        for q in queryset:

            labels.append(q.name)
            data.append(int(q.price))
        context = {
            'categories':categorie,
            'products':products,
            'orders':orders,
            'labels': labels,
            'data': data,
        }
        
        return render(self.request, 'dash-products/home.html', context)


class Pie_chart(ManagerRequiredMixin, generic.View):
    def get(self,request):
        labels = []
        data = []

        queryset = Product.objects.order_by('-price')
        for q in queryset:

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
            messages.success(self.request, 'Product deleted successfully')
            return HttpResponseRedirect(success_url)
        except IntegrityError as e:
            messages.warning(self.request, "you can't remove product")
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, 'something went Wrong')
        return self.render_to_response(self.get_context_data(form=form))


class CategorieListView(LoginRequiredMixin, generic.ListView):
    template_name = "dash-categories/categorie-list.html"
    
    def get_queryset(self):
        return Categorie.objects.all()

    context_object_name='categories'

class CategorieCreateView(ManagerRequiredMixin, generic.CreateView):
    template_name = "dash-categories/categorie-create.html"
    form_class = CategorieModelForm

    

    def get_success_url(self):
        messages.success(self.request, 'Categorie created successfully')
        return reverse("dashboard:categorie-list")

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, 'something went Wrong')
        return self.render_to_response(self.get_context_data(form=form))


class CategorieDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "dash-categories/categorie-delete.html"
    
    def get_queryset(self):
        return Categorie.objects.all()

    def get_success_url(self):
        return reverse("dashboard:categorie-list")
    

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, 'Categorie deleted successfully')
            return HttpResponseRedirect(success_url)
        except IntegrityError as e:
            messages.warning(self.request, "you can't remove categorie")
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, 'something went Wrong')
        return self.render_to_response(self.get_context_data(form=form))


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

class OrderListView(ManagerRequiredMixin, generic.View):
    
    def get(self, *args, **kwargs):
        try:
            customer =self.request.user
            orders=Order.objects.all()

            context = {
                'orders': orders,
                'customer':customer
            }
            return render(self.request, 'dash-orders/order-list.html', context)
        except Exception :
            messages.warning(self.request, 'something went Wrong')
            return render(self.request, 'dash-orders/order-list.html')




class CreateOrder(ManagerRequiredMixin,generic.View):
    def get(self, *args, **kwargs):
        try:
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
        except Exception as e:
            messages.warning(self.request, 'something went Wrong')






class OrderDetailView(ManagerRequiredMixin, generic.DetailView):
    template_name = "dash-orders/order-detail.html"

    def get(self, *args, **kwargs):
        try:
            order_id = self.kwargs['pk']
            order=Order.objects.get(id=order_id)
            items=Orderitems.objects.filter(order=order)
            context = {
                'orders':order,
                'items':items
            }
            return render(self.request, 'dash-orders/order-detail.html', context)
        except Exception as e:
            messages.warning(self.request, 'something went Wrong')

    context_object_name='orders'
    


class OrdersUpdateView(ManagerRequiredMixin, generic.UpdateView):
    template_name = "dash-orders/order-update.html"
    form_class = OrderModelForm

    def get_queryset(self):
        return Order.objects.all()
    def get_success_url(self):
        messages.success(self.request, 'order updated successfully')
        return reverse("dashboard:order-list")

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, 'something went Wrong')
        return self.render_to_response(self.get_context_data(form=form))



class OrdersDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "dash-orders/order-delete.html"
    
    def get_queryset(self):
        return Order.objects.all()

    def get_success_url(self):
        return reverse("dashboard:order-list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, 'Order deleted successfully')
            return HttpResponseRedirect(success_url)
        except IntegrityError as e:
            messages.warning(self.request, "you can't remove categorie")
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, 'something went Wrong')
        return self.render_to_response(self.get_context_data(form=form))


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
        customer=Customer.objects.get(id=self.kwargs['pk'])
        orders=Order.objects.filter(user=customer)
        context = {
            'customer':customer,
            'orders':orders
        }
        return render(self.request, 'dash-customer/customer-detail.html', context)

class CustomerUpdateView(ManagerRequiredMixin, generic.UpdateView):
    template_name = "dash-customer/customer-update.html"
    form_class = CustomerModelForm

    def get_queryset(self):
        return Customer.objects.all()
    def get_success_url(self):
        messages.success(self.request, 'customer updated successfully')
        return reverse("dashboard:customer-list")

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, 'something went Wrong')
        return self.render_to_response(self.get_context_data(form=form))



class CustomerDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "dash-customer/customer-delete.html"
    
    def get_queryset(self):
        return Customer.objects.all()

    def get_success_url(self):
        return reverse("dashboard:customer-list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, 'customer deleted successfully')
            return HttpResponseRedirect(success_url)
        except IntegrityError as e:
            messages.warning(self.request, "you can't remove customer")
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, 'something went Wrong')
        return self.render_to_response(self.get_context_data(form=form))

    

class UploadCsv(ManagerRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        uploadform=CsvModelForm()
        return render(self.request, 'dashboard/upload_csv.html', {'uploadform': uploadform})

    def post(self, *args, **kwargs):
        uploadform=CsvModelForm(self.request.POST, self.request.FILES)
        if uploadform.is_valid():
            try:
                csv_file = self.request.FILES["csv_file"]
                if not csv_file.name.endswith('.csv'):
                    messages.warning(self.request,'File is not CSV type')
                    return HttpResponseRedirect(reverse("dashboard:product-list"))
                #if file is too large, return
                if csv_file.multiple_chunks():
                    messages.warning(self.request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                    return HttpResponseRedirect(reverse("dashboard:product-list"))

                file_data = csv_file.read().decode("utf-8")		

                lines = file_data.split("\n")
                #loop over the lines and save them in db. If error , store as string and then display
                for i, line in enumerate(lines):	
                    if(i==0):
                            pass
                    else:					
                        fields = line.split(",")
                        name = fields[0]
                        description = fields[1]
                        #categorie = fields[3]
                        #categorie=Categorie.objects.get(id=4)
                        price = fields[2]
                        #print(name, description, categorie,price)
                        Product.objects.create(name=name, description=description,price=price)
                messages.success(self.request, ' created successfully')
                return HttpResponseRedirect(reverse("dashboard:product-list"))

                return render(self.request, 'dashboard/upload_csv.html', {'uploadform': uploadform})
            except Exception as e:
                messages.warning(self.request, ' Unable to upload')
                return HttpResponseRedirect(reverse("dashboard:product-list"))


class ProfileView(ManagerRequiredMixin, generic.TemplateView):
    template_name='dashboard/profile.html'
    
    def get(self, *args, **kwargs):
        profile=UserProfile.objects.get(user=self.request.user)
        context = {
            'profile':profile
        }
        return render(self.request, 'dashboard/profile.html', context)



class ProfileUpdateView(ManagerRequiredMixin, generic.UpdateView):
    template_name = "dashboard/profile-update.html"
    form_class = ProfileModelForm
    context_object_name='profile'
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("dashboard:profile")


class ExportCsv(ManagerRequiredMixin, generic.View):
    
    def get(self, *args, **kwargs):
        response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="products.csv"'},
    )

        product=Product.objects.all()
        writer = csv.writer(response)
        writer.writerow(['id', 'name', 'product_image', 'description', 'categorie', 'price'])
        for p in product:
            writer.writerow([p.id, p.name, p.product_image, p.description, p.categorie, p.price])

        return response