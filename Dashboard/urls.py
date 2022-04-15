from django.urls import path

from django.urls import path

from .views import (
    home, ProfileDetailView, ProfileUpdateView,
    )

app_name='Dashboard'

urlpatterns = [
    path('', home),
    path('profile/', ProfileDetailView.as_view(), name='profile'),

]