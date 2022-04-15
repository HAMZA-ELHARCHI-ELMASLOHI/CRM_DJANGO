from django.contrib import admin

from Dashboard.models import UserProfile, Customer, Products

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(Products)