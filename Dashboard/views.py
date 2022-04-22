from multiprocessing import context
from urllib import request
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from .forms import ProfileModelForm
from django.contrib.auth import get_user_model


#User=get_user_model()
# Create your views here.

@login_required
def home(request):
    return render(request, 'dashboard/dash-base.html')



# Profile views 


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    template_name ='dashboard/profile.html' 
    context_object_name='userprofile'

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    

class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "dashboard/profile-update.html"
    form_class = ProfileModelForm

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("Dashboard:dash")



