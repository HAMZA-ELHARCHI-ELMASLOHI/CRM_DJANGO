from multiprocessing import context
from urllib import request
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from account.mixins import ManagerRequiredMixin
from .models import   Customer, Manager, Csv
from django.contrib.auth import get_user_model
from .forms import ProductModelForm, CategorieModelForm, OrderModelForm, CsvModelForm
from shop.models import Product, Order, Categorie, Orderitems
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.db import IntegrityError
from django.http import HttpResponseRedirect

import csv
#User=get_user_model()
# Create your views here.



class Home(ManagerRequiredMixin, generic.View):
    template_name='dashboard/home.html'
    def get(self, *args, **kwargs):
        categorie=Categorie.objects.count()
        products=Product.objects.count()
        orders=Order.objects.filter(is_confirmed=True).count()
        customers=Customer.objects.count()
        context = {
            'categories':categorie,
            'products':products,
            'orders':orders,
            'customers':customers
        }
        return render(self.request, 'dashboard/home.html', context)

class StatisticView(ManagerRequiredMixin, generic.View):
    template_name = "dash-products/home.html"
    
    def get(self, *args, **kwargs):
        categorie=Categorie.objects.count()
        products=Product.objects.count()
        orders=Order.objects.count()
        context = {
            'categories':categorie,
            'products':products,
            'orders':orders
        }
        
        return render(self.request, 'dash-products/home.html', context)


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


class CategorieListView(LoginRequiredMixin, generic.ListView):
    template_name = "dash-categories/categorie-list.html"
    
    def get_queryset(self):
        return Categorie.objects.all()

    context_object_name='categories'

class CategorieCreateView(ManagerRequiredMixin, generic.CreateView):
    template_name = "dash-categories/categorie-create.html"
    form_class = CategorieModelForm

    def get_success_url(self):
        return reverse("dashboard:categorie-list")


class CategorieDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "dash-categories/categorie-delete.html"
    def get_success_url(self):
        return reverse("dashboard:categorie-list")
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

class OrderListView(ManagerRequiredMixin, generic.View):
    
    def get(self, *args, **kwargs):
        customer =Customer.objects.get(user=self.request.user)
        orders=Order.objects.all()

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


class UploadCsv(ManagerRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        uploadform=CsvModelForm()
        return render(self.request, 'dashboard/upload_csv.html', {'uploadform': uploadform})

    def post(self, *args, **kwargs):
        uploadform=CsvModelForm(self.request.POST, self.request.FILES)
        if uploadform.is_valid():
            print('valid')

            csv_file = self.request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return HttpResponseRedirect(reverse("dashboard:product-list"))
            #if file is too large, return
            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponseRedirect(reverse("dashboard:product-list"))

            file_data = csv_file.read().decode("utf-8")		

            lines = file_data.split("\n")
            #loop over the lines and save them in db. If error , store as string and then display
            for i, line in enumerate(lines):	
                if(i==0):
                        pass
                else:					
                    fields = line.split(",")
                    print(fields)
                    name = fields[0]
                    description = fields[1]
                    #categorie = fields[3]
                    categorie=Categorie.objects.get(id=4)
                    price = fields[3]
                    print(name, description, categorie,price)
                    Product.objects.create(name=name, description=description, categorie=categorie,price=price)
    
            return render(self.request, 'dashboard/upload_csv.html', {'uploadform': uploadform})



def updload_csv(request):
    form= CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form=CsvModelForm()
        obj=Csv.objects.all().first()
        with open(obj.file_name.path, 'r') as f:
            reader=csv.reader(f)
            for i, row in enumerate(reader):
                if(i==0):
                    pass
                else:
                    name=row[0]
                    description=row[2]
                    cat=row[3]
                    price=row[4]
                    print(cat)  
                    categorie=Categorie.objects.get(id=4)
                    #print('sss',categorie.id)
                    print(name, description, cat, price)
                    Product.objects.create(name=name, description=description, categorie=categorie,price=price)
                    messages.success(request, ' created successfully')
                    return reverse('dashboard:product-list.html')

    return render(request, 'dashboard/upload_csv.html', {'form': form})


def upload_csv(request):

    if request.method == 'POST':
        form=CsvModelForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')

            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return HttpResponseRedirect(reverse("dashboard:upload-csv"))
            #if file is too large, return
            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponseRedirect(reverse("dashboard:upload-csv"))

            file_data = csv_file.read().decode("utf-8")		

            lines = file_data.split("\n")
            #loop over the lines and save them in db. If error , store as string and then display
            for i, line in enumerate(lines):	
                if(i==0):
                        pass
                else:					
                    print(line)
                    fields = line.split(",")
                    print(fields)
                    #print(fields[1])

                    name = fields[0]
                    description = fields[1]
                    #categorie = fields[3]
                    categorie=Categorie.objects.get(id=4)
                    price = fields[3]
                    print(name, description, categorie,price)
                    Product.objects.create(name=name, description=description, categorie=categorie,price=price)
    else:
        form=CsvModelForm() 
    return render(request, 'dashboard/upload_csv.html', {'form': form})
