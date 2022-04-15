from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


#Customers views

class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    pass

class CustomerListView(LoginRequiredMixin, generic.ListView):
    pass

class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    pass

class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    pass

class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    pass