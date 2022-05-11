from django.contrib import admin

from Dashboard.models import   Customer, Manager, Csv

# Register your models here.

admin.site.register(Customer)
admin.site.register(Manager)
admin.site.register(Csv)
