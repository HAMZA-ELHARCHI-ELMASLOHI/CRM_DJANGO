from django.urls import path

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home, pie_chart
    )

app_name='Dashboard'

urlpatterns = [
    path('', home, name='dash'),
    
    path('pie-chart/', pie_chart, name='pie-chart'),



]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
