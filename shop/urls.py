from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    CategorieCreateView,  ProductListView, ProductDetailView, ProductCreateView, ProductDeleteView, ProductUpdateView,
     CategorieDeleteView, CategorieListView, CartItemsView,add_to_cart, delete_from_cart,Shop_home,
    remove_from_cart, CartView, OrdersCreateView, OrdersDeleteView, OrdersDetailView, OrdersListView
    ,CreateOrder, CategorieDetailView, render_pdf_view, ProfileView, ProfileUpdateView
    )

app_name='shop'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('', Shop_home.as_view(), name='shop-home'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('product/<str:pk>/', ProductDetailView.as_view(), name='product-detail'),
    #path('products/create/', ProductCreateView.as_view(), name='product-create'),
    #path('products/<str:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    #path('products/<str:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    
    #categorie
    path('categories/', CategorieListView.as_view(), name='categorie-list'),
    path('categorie/<str:pk>/', CategorieDetailView.as_view(), name='categorie-detail'),
    #path('create-categorie/', CategorieCreateView.as_view(), name='categorie-create'),
    #path('<int:pk>/categorie/delete/', CategorieDeleteView.as_view(), name='categorie-delete'),

    # cart
    #path('cart/', CartItemsView.as_view(), name='cart'),
    path('cart/', CartView.as_view(), name='cart'),

    path('products/add-to-cart/<str:id>/', add_to_cart, name='add-to-cart'),
    path('cart/add-to-cart/<str:id>/', add_to_cart, name='add-to-cart'),
    path('cart/remove-from-cart/<str:id>/', remove_from_cart, name='remove-from-cart'),

    path('delete-from-cart/<str:id>/', delete_from_cart, name='delete-from-cart'),


    # orders
    path('order/', OrdersListView.as_view(), name='order-list'),
    path('order/<int:pk>/', OrdersDetailView.as_view(), name='order-detail'),
    path('order/create/', OrdersCreateView.as_view(), name='order-create'),
    path('order/<int:pk>/delete/', OrdersDeleteView.as_view(), name='order-delete'),
    #path('order/<int:pk>/update/', OrdersUpdateView.as_view(), name='order-update'),

    #order pdf invoice

    path('order/invoice/<int:pk>', render_pdf_view, name='order-invoice')

]

