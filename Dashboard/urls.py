from django.urls import path

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    Home, Pie_chart, ProductCreateView, ProductDeleteView, ProductUpdateView,
    CategorieCreateView, CategorieDeleteView, CreateOrder, OrdersDeleteView,
    OrdersUpdateView, ProductListView, CustomerListView, CustomerDetailView,
    OrderListView ,OrderDetailView, CategorieDetailView, upload_csv,
    CategorieListView

    )
app_name='dashboard'

urlpatterns = [
    path('', Home.as_view(), name='dash'),
    
    path('pie-chart/', Pie_chart.as_view(), name='pie-chart'),
        
    path('products/', ProductListView.as_view(), name='product-list'),

    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<str:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/<str:pk>/update/', ProductUpdateView.as_view(), name='product-update'),

    path('categories/', CategorieListView.as_view(), name='categorie-list'),

    path('create-categorie/', CategorieCreateView.as_view(), name='categorie-create'),
    path('<int:pk>/categorie/delete/', CategorieDeleteView.as_view(), name='categorie-delete'),
    path('categorie/<str:pk>/', CategorieDetailView.as_view(), name='categorie-detail'),

    path('orders/', OrderListView.as_view(), name='order-list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('order/create/', CreateOrder.as_view(), name='order-create'),
    path('order/<int:pk>/delete/', OrdersDeleteView.as_view(), name='order-delete'),
    path('order/<int:pk>/update/', OrdersUpdateView.as_view(), name='order-update'),


    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),

    path('upload-csv/', upload_csv, name='upload-csv')

]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
