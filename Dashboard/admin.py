from django.contrib import admin

from Dashboard.models import  Country, City, Customer, Manager

# Register your models here.
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Customer)
admin.site.register(Manager)
