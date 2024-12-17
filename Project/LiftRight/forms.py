from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # gender = forms.ChoiceField(choices=CustomUser.gender, required=False, widget=forms.Select())

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'age', 'weight', 'height','gender','goal','body_fat_percentage']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
