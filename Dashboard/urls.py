from django.urls import path

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home, ProfileDetailView, ProfileUpdateView
    )

app_name='Dashboard'

urlpatterns = [
    path('', home, name='dash'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),

    path('<int:pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),


]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
