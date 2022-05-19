from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import UserProfile

class UserForm(forms.Form):
    first_name =forms.CharField()
    last_name =forms.CharField()
    email=forms.EmailField()

class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','first_name', 'last_name' , 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
	username = forms.CharField(label='Email / Username')

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'name',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'adresse',
            'image',
        )
