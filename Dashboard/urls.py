from django.urls import path

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home, pie_chart, ProductCreateView, ProductDeleteView, ProductUpdateView,
    CategorieCreateView, CategorieDeleteView, CreateOrder, OrdersDeleteView,
    OrdersUpdateView, ProductListView

    )

app_name='dashboard'

urlpatterns = [
    path('', home, name='dash'),
    
    path('pie-chart/', pie_chart, name='pie-chart'),
        
    path('products/', ProductListView.as_view(), name='product-list'),

    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<str:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/<str:pk>/update/', ProductUpdateView.as_view(), name='product-update'),

    path('create-categorie/', CategorieCreateView.as_view(), name='categorie-create'),
    path('<int:pk>/categorie/delete/', CategorieDeleteView.as_view(), name='categorie-delete'),

    path('order/create/', CreateOrder.as_view(), name='order-create'),
    path('order/<int:pk>/delete/', OrdersDeleteView.as_view(), name='order-delete'),
    path('order/<int:pk>/update/', OrdersUpdateView.as_view(), name='order-update'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
