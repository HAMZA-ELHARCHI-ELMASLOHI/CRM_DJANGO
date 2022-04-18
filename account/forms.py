from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(forms.Form):
    first_name =forms.CharField()
    last_name =forms.CharField()
    email=forms.EmailField()

class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','first_name', 'last_name' , 'email', 'password1', 'password2']