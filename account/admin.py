from django.contrib import admin

# Register your models here.
from .models import User, UserProfile, ManagerMore, Customer, Manager

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(ManagerMore)
admin.site.register(Manager)
admin.site.register(Customer)
