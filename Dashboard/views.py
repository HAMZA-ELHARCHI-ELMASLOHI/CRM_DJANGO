from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model

User=get_user_model()
# Create your views here.

@login_required
def home(request):
    return render(request, 'dashboard/dash-base.html')



# Profile views 
class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    template_name ='dashboard/profile.html'
    

class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    pass


# Product views

class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    pass

class ProductListView(LoginRequiredMixin, generic.ListView):
    pass

class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    pass

class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    pass

class ProductUpdateView(LoginRequiredMixin, generic.UpdateView):
    pass

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

