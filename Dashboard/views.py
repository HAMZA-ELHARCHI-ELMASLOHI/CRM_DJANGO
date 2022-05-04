from multiprocessing import context
from urllib import request
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  City
from django.contrib.auth import get_user_model


#User=get_user_model()
# Create your views here.

@login_required
def home(request):
    return render(request, 'dashboard/dash-base.html')








def pie_chart(request):
    labels = []
    data = []

    queryset = City.objects.order_by('-population')[:5]
    for city in queryset:
        labels.append(city.name)
        data.append(city.population)

    return render(request, 'dashboard/pie_chart.html', {
        'labels': labels,
        'data': data,
    })