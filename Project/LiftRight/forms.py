from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUserCreationForm(UserCreationForm):
    # gender = forms.ChoiceField(choices=CustomUser.gender, required=False, widget=forms.Select())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'age', 'weight', 'height','gender','goal','body_fat_percentage', 'plan_type', 'activity_level']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class CalorieCalculatorForm(forms.Form):
    weight = forms.FloatField(
        label='Weight (kg)',
        validators=[MinValueValidator(20, "Weight must be at least 20 kg"), MaxValueValidator(300, "Weight cannot exceed 300 kg")],
        help_text="Enter your weight in kilograms."
    )
    height = forms.FloatField(
        label='Height (cm)',
        validators=[MinValueValidator(100, "Height must be at least 100 cm"), MaxValueValidator(250, "Height cannot exceed 250 cm")],
        help_text="Enter your height in centimeters."
    )
    age = forms.IntegerField(
        label='Age',
        validators=[MinValueValidator(10, "Age must be at least 10 years"), MaxValueValidator(120, "Age cannot exceed 120 years")],
        help_text="Enter your age."
    )
    activity_level = forms.ChoiceField(
        choices=[
            ('sedentary', 'Sedentary'),
            ('moderate', 'Moderate Activity'),
            ('active', 'Active'),
        ],
        label='Activity Level',
        help_text="Select your activity level."
    )