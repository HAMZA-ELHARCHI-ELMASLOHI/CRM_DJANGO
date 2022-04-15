from django.urls import path

from django.urls import path

from .views import (
    home, ProfileDetailView, ProfileUpdateView,
    ProductUpdateView,ProductCreateView, ProductListView, ProductDeleteView, ProductDetailView,
    CustomerCreateView, CustomerDeleteView, CustomerDetailView, CustomerListView, CustomerUpdateView
    )

app_name='Dashboard'

urlpatterns = [
    path('', home),
    path('profile/', ProfileDetailView.as_view(), name='profile'),

]