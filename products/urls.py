from django.urls import path
from .views import (
    CategorieCreateView,  ProductListView, ProductDetailView, ProductCreateView, ProductDeleteView, ProductUpdateView,
     CategorieDeleteView, CategorieListView, CartItemsView,add_to_cart, delete_from_cart,
    remove_from_cart, CartView
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


]