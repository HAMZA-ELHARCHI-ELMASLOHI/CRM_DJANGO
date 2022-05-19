from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Categorie, Product, Cart, CartItem, Order, Orderitems
from .forms import ProductModelForm, CategorieModelForm, OrderModelForm, OrderForm

from account.models import UserProfile
from account.forms import ProfileModelForm
# Product views

from account.mixins import ManagerRequiredMixin, CustomerRequiredMixin
from django.http import JsonResponse, FileResponse
import json

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from django.http import HttpResponse

from Dashboard.models import Customer
from django.contrib import messages



from .filters import ProductFilter


class Shop_home(LoginRequiredMixin, generic.TemplateView):
    template_name = "shop_home.html"


class ProfileView(CustomerRequiredMixin, generic.TemplateView):
    
    def get(self, *args, **kwargs):
        profile=UserProfile.objects.get(user=self.request.user)
        context = {
            'profile':profile
        }
        return render(self.request, 'profile.html', context)



class ProfileUpdateView(CustomerRequiredMixin, generic.UpdateView):
    template_name = "profile-update.html"
    form_class = ProfileModelForm
    context_object_name='profile'
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("shop:profile")

class ProductListView(CustomerRequiredMixin, generic.ListView):
    template_name = "products/product-list.html"
    
    def get(self, *args, **kwargs):
        categorie=Categorie.objects.all()
        products=Product.objects.all()
        productFilter=ProductFilter(self.request.GET, queryset=products)
        products=productFilter.qs
        context = {
            'categories':categorie,
            'products':products,
            'productFilter':productFilter
        }
        return render(self.request, 'products/product-list.html', context)
    

    
    

    context_object_name='products'

class ProductDetailView(CustomerRequiredMixin, generic.DetailView):
    template_name = "products/product-detail.html"
    
    def get_queryset(self):
        return Product.objects.all()

    context_object_name='products'



class ProductCreateView(ManagerRequiredMixin, generic.CreateView):
    template_name = "products/product-create.html"
    form_class = ProductModelForm

    def get_success_url(self):
        return reverse("shop:product-list")


class ProductUpdateView(ManagerRequiredMixin, generic.UpdateView):
    template_name = "products/product-update.html"
    form_class = ProductModelForm

    def get_queryset(self):
        return Product.objects.all()
    def get_success_url(self):
        return reverse("shop:product-list")



class ProductDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "products/product-delete.html"
    def get_success_url(self):
        return reverse("shop:product-list")
    def get_queryset(self):
        return Product.objects.all()




# Categories

class CategorieListView(CustomerRequiredMixin, generic.ListView):
    template_name = "categories/categorie-list.html"
    
    def get_queryset(self):
        return Categorie.objects.all()

    context_object_name='categories'


class CategorieDetailView(CustomerRequiredMixin, generic.DetailView):
    template_name = "categories/categorie-detail.html"
    
    def get(self, *args, **kwargs):
        categorie_id = self.kwargs['pk']
        categorie=Categorie.objects.get(id=categorie_id)
        items=Product.objects.filter(categorie=categorie)
        context = {
            'categorie':categorie,
            'items':items
        }
        return render(self.request, 'categories/categorie-detail.html', context)

class CategorieCreateView(ManagerRequiredMixin, generic.CreateView):
    template_name = "categories/categorie-create.html"
    form_class = CategorieModelForm

    def get_success_url(self):
        return reverse("shop:product-create")


class CategorieDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "categories/categorie-delete.html"
    def get_success_url(self):
        return reverse("shop:categorie-create")
    def get_queryset(self):
        return Categorie.objects.all()


# Cart



class CartItemsView(CustomerRequiredMixin,generic.ListView):
    model = CartItem
    context_object_name='items'
    def get_queryset(self):
        customer=Customer.objects.get(user=request.user)
        cart=Cart.objects.get(customer=customer)
        #price=cart.get_cart_total

        return CartItem.objects.filter(user=self.request.user)


    template_name='cart/cart.html'

class CartView(CustomerRequiredMixin, generic.View):
    def get(self, *args, **kwargs):

        customer=Customer.objects.get(user=self.request.user)
        cart=Cart.objects.get(customer=customer)
        items=CartItem.objects.filter(cart=cart).order_by('-quantity')
        context = {
            'cart': cart,
            'items':items
        }
        return render(self.request, 'cart/cart.html', context)










def add_to_cart(request, id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' :
        id = json.load(request)['id']
        item = get_object_or_404(Product, id=id)
        customer=Customer.objects.get(user=request.user)
        cart=Cart.objects.get(customer=customer)

        cart_item, created = CartItem.objects.get_or_create(
                product=item,
                cart=cart, 
            )
        cart_item.quantity= (cart_item.quantity +1)
        cart_item.save()
        #messages.success(request, "This item was added to Cart.")
        return JsonResponse({'quantity':cart_item.quantity, 'price': cart_item.get_total, 'cart_total':cart.get_cart_total}, status=200, safe=False )

def remove_from_cart(request, id):
    #print(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' :
        id = json.load(request)['id']
        item = get_object_or_404(Product, id=id)
        customer=Customer.objects.get(user=request.user)
        cart=Cart.objects.get(customer=customer)

        cart_item, created = CartItem.objects.get_or_create(
                product=item,
                cart=cart, 
            )
        if(cart_item.quantity>0):
            cart_item.quantity= (cart_item.quantity -1)
            cart_item.save()
        else:
            delete_from_cart(request, id)
        #messages.success(request, "This item quantity was updated.")
        return JsonResponse({'quantity':cart_item.quantity, 'price': cart_item.get_total,'cart_total':cart.get_cart_total}, status=200, safe=False )


def delete_from_cart(request, id):
    item = get_object_or_404(Product, id=id)
    cart_item = CartItem.objects.filter(product=item).delete()
    messages.success(request, "This item was deleted successfuly.")
    return redirect("shop:product-list")


#Orders

class OrdersListView(CustomerRequiredMixin,generic.View):
    
    def get(self, *args, **kwargs):
        customer =Customer.objects.get(user=self.request.user)
        orders=Order.objects.filter(customer=customer)

        context = {
            'orders': orders,
            'customer':customer
        }
        return render(self.request, 'orders/order-list.html', context)

    





class OrdersDetailView(CustomerRequiredMixin, generic.DetailView):
    template_name = "orders/order-detail.html"

    def get(self, *args, **kwargs):
        order_id = self.kwargs['pk']
        order=Order.objects.get(id=order_id)
        items=Orderitems.objects.filter(order=order)
        context = {
            'orders':order,
            'items':items
        }
        return render(self.request, 'orders/order-detail.html', context)


    context_object_name='orders'



class CreateOrder(CustomerRequiredMixin, generic.CreateView):
    template_name = "categories/categorie-create.html"
    form_class = OrderForm

    

    def get(self, *args, **kwargs):
        customer=Customer.objects.get(user=self.request.user)
        cart=Cart.objects.get(customer=customer)
        items=CartItem.objects.filter(cart=cart)
    
        total_price=cart.get_cart_total
        context = {
            'items':items,
            'cart':cart
        }
        
        order = Order.objects.create(
                customer=customer,
                total_price=total_price,
                
            )
        

        for item in items:
            Orderitems.objects.create(order=order,name=item.product.name ,product=item.product, price=item.get_total, quantity=item.quantity)
        order.save()

        return render(self.request,  'cart/cart.html', context)

class OrdersCreateView(CustomerRequiredMixin, generic.FormView):
    template_name = "orders/order-create.html"
    form_class = OrderForm
    

    def post(self, request, *args, **kwargs):
        customer=Customer.objects.get(user=self.request.user)
        cart=Cart.objects.get(customer=customer)
        items=CartItem.objects.filter(cart=cart)
    
        total_price=cart.get_cart_total
        
        form = self.get_form()
        if form.is_valid():
            Adresse = form.cleaned_data['Adresse']
            zipcode = form.cleaned_data['zipcode']

            context = {
            'items':items,
            'cart':cart
             }
            order = Order.objects.create(
                customer=customer,
                total_price=total_price,
                Adresse=Adresse,
                zipcode=zipcode
                
            )
            for item in items:
                Orderitems.objects.create(order=order,name=item.product.name ,product=item.product, price=item.get_total, quantity=item.quantity)
            order.save()

            return render(self.request,  'cart/cart.html', context)
        else:
            print(subject)

    '''        
    def get(self, *args, **kwargs):
        customer=Customer.objects.get(user=self.request.user)
        cart=Cart.objects.get(customer=customer)
        items=CartItem.objects.filter(cart=cart)
    
        total_price=cart.get_cart_total
        context = {
            'items':items,
            'cart':cart
        }
        
        order = Order.objects.create(
                customer=customer,
                total_price=total_price,
                
            )
        

        for item in items:
            Orderitems.objects.create(order=order,name=item.product.name ,product=item.product, price=item.get_total, quantity=item.quantity)
        order.save()

        return render(self.request,  'cart/cart.html', context)'''

    

    


class OrdersUpdateView(ManagerRequiredMixin, generic.UpdateView):
    template_name = "orders/order-update.html"
    form_class = OrderModelForm

    def get_queryset(self):
        return Order.objects.all()
    def get_success_url(self):
        return reverse("shop:order-list")



class OrdersDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "orders/order-delete.html"
    def get_success_url(self):
        return reverse("shop:order-list")
    def get_queryset(self):
        return Order.objects.all()


class pdf(CustomerRequiredMixin, generic.DetailView):
    template_name = "orders/order-detail.html"

    def get(self, *args, **kwargs):
        order_id = self.kwargs['pk']
        order=Order.objects.get(id=order_id)
        items=Orderitems.objects.filter(order=order)
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 100, f"Hello{order.name} {order.total_price} ")

        p.showPage()
        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


def render_pdf_view(request, *args, **kwargs):
    order_id = kwargs['pk']
    order=Order.objects.get(id=order_id)
    items=Orderitems.objects.filter(order=order)
    customer =Customer.objects.get(user=request.user)

    template_path = 'orders/invoice.html'
    context = {'orders': order, 'items':items, 'customer':customer}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #download
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #display
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
