from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User

class CustomUserCreationForm(UserCreationForm):
    # gender = forms.ChoiceField(choices=CustomUser.gender, required=False, widget=forms.Select())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'age', 'weight', 'height','body_fat_percentage','gender','goal', 'plan_type','activity_level']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class CalorieCalculatorForm(forms.Form):
    weight = forms.FloatField(label='Weight (kg)')
    height = forms.FloatField(label='Height (cm)')
    age = forms.IntegerField(label='Age')
    activity_level = forms.ChoiceField(
        choices=[
            ('sedentary', 'Sedentary'),
            ('moderate', 'Moderate Activity'),
            ('active', 'Active'),
        ],
        label='Activity Level',
    )
    
class FFMICalculatorForm(forms.Form):
    weight = forms.FloatField(label='Weight (kg)')
    height = forms.FloatField(label='Height (cm)')
    bodyfat = forms.FloatField(label='Body Fat (%)')
    
    