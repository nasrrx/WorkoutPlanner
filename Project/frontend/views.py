from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Home') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'SignUp.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Home')  
    else:
        form = CustomAuthenticationForm()
    return render(request, 'LogIn.html', {'form': form})


def Home(request):
    # Static data for testing
    height = 170  # Example height in cm
    weight = 70   # Example weight in kg

    
    height_m = height / 100  
    bmi = round(weight / (height_m ** 2), 2) 

    context = {
        'bmi': bmi,
        'height': height,
        'weight': weight,
    }
    return render(request, 'Home.html', context)

def Profile(request):
    return render(request,'Profile.html')