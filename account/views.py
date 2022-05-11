from audioop import reverse
from django.shortcuts import render, reverse
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, ProfileModelForm
from .models import UserProfile

# Create your views here.

def home_page(request):
    return render(request, 'account/home_page.html')

class SignUpView(generic.CreateView):
    template_name='registration/signup.html'

    form_class=CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


# Profile views 


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    template_name ='account/profile.html' 
    context_object_name='userprofile'

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    

class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "account/profile-update.html"
    form_class = ProfileModelForm

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("shop:product-list")

