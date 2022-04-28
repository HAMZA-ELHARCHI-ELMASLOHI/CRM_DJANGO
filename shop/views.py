from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Categorie, Product, Cart, CartItem, Order, Orderitems
from .forms import ProductModelForm, CategorieModelForm, OrderModelForm

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import Image
# Product views

from account.mixins import ManagerRequiredMixin
from django.http import JsonResponse, FileResponse
import json

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

class CategorieListView(ManagerRequiredMixin, generic.ListView):
    template_name = "categories/categorie-list.html"
    
    def get_queryset(self):
        return Categorie.objects.all()

    context_object_name='categories'

class CategorieCreateView(ManagerRequiredMixin, generic.CreateView):
    template_name = "categories/categorie-create.html"
    form_class = CategorieModelForm

    def get_success_url(self):
        return reverse("shop:product-create")


class CategorieDeleteView(ManagerRequiredMixin, generic.DeleteView):
    template_name = "categories/categorie-delete.html"
    def get_success_url(self):
        return reverse("shop:categorie-create")
    def get_queryset(self):
        return Categorie.objects.all()


# Cart



class CartItemsView(generic.ListView):
    model = CartItem
    context_object_name='items'
    def get_queryset(self):
        cart=Cart.objects.get(user=self.request.user)
        #price=cart.get_cart_total

        return CartItem.objects.filter(user=self.request.user)


    template_name='cart/cart.html'

class CartView(generic.View):
    def get(self, *args, **kwargs):
        cart=Cart.objects.get(user=self.request.user)
        items=CartItem.objects.filter(cart=cart)
        context = {
            'cart': cart,
            'items':items
        }
        return render(self.request, 'cart/cart.html', context)










def add_to_cart(request, slug):
    #print(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' :
        slug = json.load(request)['slug']
        item = get_object_or_404(Product, slug=slug)
        cart=Cart.objects.get(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
                product=item,
                cart=cart, 
            )
        cart_item.quantity= (cart_item.quantity +1)
        cart_item.save()
        #messages.info(request, "This item quantity was updated.")
        return JsonResponse({'quantity':cart_item.quantity}, status=200, safe=False )

def remove_from_cart(request, slug):
    #print(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' :
        slug = json.load(request)['slug']
        item = get_object_or_404(Product, slug=slug)
        cart=Cart.objects.get(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
                product=item,
                cart=cart, 
            )
        if(cart_item.quantity>0):
            cart_item.quantity= (cart_item.quantity -1)
            cart_item.save()
        else:
            delete_from_cart(request, slug)
        #messages.info(request, "This item quantity was updated.")
        return JsonResponse({'quantity':cart_item.quantity}, status=200, safe=False )


def delete_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    print(item)
    cart_item = CartItem.objects.filter(product=item).delete()
    print(cart_item)
    #messages.info(request, "This item quantity was updated.")
    return redirect("shop:product-list")


#Orders

class OrdersListView(LoginRequiredMixin, generic.ListView):
    template_name = "orders/order-list.html"
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    

    context_object_name='orders'

class OrdersDetailView(LoginRequiredMixin, generic.DetailView):
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
    template_name = "orders/order-create.html"
    form_class = OrderModelForm

    def get_success_url(self):
        return reverse("shop:order-list")


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


class pdf(LoginRequiredMixin, generic.DetailView):
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
