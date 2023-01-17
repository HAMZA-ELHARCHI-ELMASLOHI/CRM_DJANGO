from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .views import ProfileDetailView, ProfileUpdateView

app_name='account'

urlpatterns = [

    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),

    path('<int:pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),
]

