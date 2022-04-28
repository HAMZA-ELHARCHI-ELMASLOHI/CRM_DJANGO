from django.urls import path
from .views import (
    CategorieCreateView,  ProductListView, ProductDetailView, ProductCreateView, ProductDeleteView, ProductUpdateView,
     CategorieDeleteView, CategorieListView, CartItemsView,add_to_cart, delete_from_cart,
    remove_from_cart, CartView, OrdersCreateView, OrdersDeleteView, OrdersDetailView, OrdersListView, OrdersUpdateView
    ,CreateOrder, pdf
    )

app_name='products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('p/<slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    
    #categorie
    path('categories/', CategorieListView.as_view(), name='categorie-list'),
    path('create-categorie/', CategorieCreateView.as_view(), name='categorie-create'),
    path('<int:pk>/categorie/delete/', CategorieDeleteView.as_view(), name='categorie-delete'),

    # cart
    #path('cart/', CartItemsView.as_view(), name='cart'),
    path('cart/', CartView.as_view(), name='cart'),

    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('cart/add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('cart/remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),

    path('delete-from-cart/<slug>/', delete_from_cart, name='delete-from-cart'),


    # orders
    path('order/', OrdersListView.as_view(), name='order-list'),
    path('order/<int:pk>/', OrdersDetailView.as_view(), name='order-detail'),
    path('order/create/', CreateOrder.as_view(), name='order-create'),
    path('order/<int:pk>/delete/', OrdersDeleteView.as_view(), name='order-delete'),
    path('order/<int:pk>/update/', OrdersUpdateView.as_view(), name='order-update'),

    #order pdf invoice

    path('order/invoice/<int:pk>', pdf.as_view(), name='order-invoice')

]