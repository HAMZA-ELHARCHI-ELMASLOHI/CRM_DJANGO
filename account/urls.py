from django.urls import path


from .views import home_page

app_name='account'

urlpatterns = [
    path('', home_page)
]