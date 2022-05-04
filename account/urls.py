from django.urls import path


from .views import home_page , ProfileDetailView, ProfileUpdateView

app_name='account'

urlpatterns = [
    path('', home_page),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),

    path('<int:pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),
]