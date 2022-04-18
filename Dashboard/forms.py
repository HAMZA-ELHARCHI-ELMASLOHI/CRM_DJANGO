from django import forms

from .models import UserProfile

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'name',
            'email',
            'age',
            'image',
        )
