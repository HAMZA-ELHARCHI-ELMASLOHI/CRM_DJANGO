from django.contrib import admin

# Register your models here.
from .models import User, UserProfile, ManagerMore, Customer, Manager

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Manager)
admin.site.register(Customer)

admin.site.site_header  =  "Admin Dashboard"  
admin.site.site_url='/dashboard/'