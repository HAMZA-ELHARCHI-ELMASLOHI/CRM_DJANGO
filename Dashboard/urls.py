from django.urls import path

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    Home, ProductListView, ProductCreateView, ProductDeleteView, ProductUpdateView,ProductDetailView,
    CategorieListView, CategorieDetailView, CategorieCreateView, CategorieDeleteView, 
    OrderListView , OrdersDeleteView, OrdersUpdateView,OrderDetailView,  
    CustomerListView, CustomerDetailView,CustomerDeleteView, CustomerUpdateView,
    ProfileView, ProfileUpdateView, ExportCsv,UploadCsv,
    
    )

from shop.views import render_pdf_view
app_name='dashboard'

urlpatterns = [
    path('', Home.as_view(), name='dash'),
    
    #path('pie-chart/', Pie_chart.as_view(), name='pie-chart'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),

    path('products/', ProductListView.as_view(), name='product-list'),

    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/<str:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<str:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/<str:pk>/update/', ProductUpdateView.as_view(), name='product-update'),

    path('categories/', CategorieListView.as_view(), name='categorie-list'),

    path('create-categorie/', CategorieCreateView.as_view(), name='categorie-create'),
    path('<int:pk>/categorie/delete/', CategorieDeleteView.as_view(), name='categorie-delete'),
    path('categorie/<str:pk>/', CategorieDetailView.as_view(), name='categorie-detail'),

    path('orders/', OrderListView.as_view(), name='order-list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    #path('order/create/', CreateOrder.as_view(), name='order-create'),
    path('order/<int:pk>/delete/', OrdersDeleteView.as_view(), name='order-delete'),
    path('order/<int:pk>/update/', OrdersUpdateView.as_view(), name='order-update'),


    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('customer/<str:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),
    path('customer/<str:pk>/update/', CustomerUpdateView.as_view(), name='customer-update'),

    path('upload-csv/', UploadCsv.as_view(), name='upload-csv'),
    path('export-csv/', ExportCsv.as_view(), name='export-csv'),

    path('order/invoice/<int:pk>', render_pdf_view, name='order-invoice')

]

