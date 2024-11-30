from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required

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
            return redirect('Profile')  
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


@login_required
def Profile(request):
    user = request.user 
    
    if hasattr(user, 'height') and hasattr(user, 'weight') and user.height and user.weight:
        height_m = user.height / 100  
        bmi = round(user.weight / (height_m ** 2), 2)  
    else:
        bmi = "Not available"  
    
    context = {
        'name': user.username,
        'email': user.email,
        'age': user.age,  
        'height': user.height,
        'weight': user.weight,
        'bmi': bmi,  
    }
    return render(request, 'Profile.html', context)


def About(request):
    return render(request,'About.html')