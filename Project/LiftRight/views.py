from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse, HttpResponse
from .forms import CalorieCalculatorForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import User, WorkoutPlan
import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .utils import generate_pdf, calculate_bmi, read_exercises_from_csv, read_food_items_from_csv
from django.http import JsonResponse


def RenderSignUpView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'SignUp.html', {'form': form})

def RenderLoginView(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'LogIn.html', {'form': form})

def RenderHomePage(request):
    return render(request, 'Home.html')

def RenderAboutPage(request):
    return render(request, 'About.html')
    
@login_required
def LoadProfileUserData(request):
    user = request.user
    
    context = {
        'name': user.username,
        'email': user.email,
        'age': user.age,
        'height': user.height,
        'weight': user.weight,
        'gender': user.gender,
        'goal': user.goal,
        'body_fat_percentage': user.body_fat_percentage,
        'plan_type': user.get_plan_type_display,
        'bmi': calculate_bmi(user.height, user.weight, user.age, user.gender)
    }

    return render(request, 'Profile.html', context)

@csrf_exempt
@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user

            # Update user data, including plan_type
            user.plan_type = data.get('plan_type', user.plan_type)
            user.age = data.get('age', user.age)
            user.weight = data.get('weight', user.weight)
            user.height = data.get('height', user.height)
            user.gender = data.get('gender', user.gender)
            user.goal = data.get('goal', user.goal)
            user.body_fat_percentage = data.get('body_fat_percentage', user.body_fat_percentage)
            user.save()

            return JsonResponse({'message': 'Profile updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def download_workout_plan(request):
    # Get the current user
    user = request.user

    # Use the user's plan type as the default
    plan_type = user.plan_type if user.plan_type else 'full_body'

    # Read food items from the CSV file
    food_items = read_food_items_from_csv()

    # Generate the PDF with the selected plan type
    return generate_pdf(plan_type, food_items)

# def find_gyms(request):
#     return render(request, 'Gyms.html')

# def get_nearby_gyms(request):
#     lat = request.GET.get('lat')
#     lng = request.GET.get('lng')

#     if not lat or not lng:
#         return JsonResponse({"error": "Invalid coordinates"}, status=400)

#     # Use Nominatim API (OpenStreetMap) for nearby gym search
#     url = f"https://nominatim.openstreetmap.org/search?format=json&q=gym&limit=10&bounded=1&viewbox={float(lng)-0.05},{float(lat)+0.05},{float(lng)+0.05},{float(lat)-0.05}"
#     response = requests.get(url)

#     if response.status_code != 200:
#         return JsonResponse({"error": "Failed to fetch gyms"}, status=500)

#     gyms = response.json()
#     results = [
#         {
#             "name": gym.get('display_name', 'Unknown Gym'),
#             "lat": gym.get('lat'),
#             "lon": gym.get('lon'),
#             "address": gym.get('display_name', 'Unknown Address')
#         } for gym in gyms
#     ]
#     return JsonResponse({"gyms": results})


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('LogIn') 



def calorie_calculator(request):
    if request.method == 'POST':
        form = CalorieCalculatorForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            activity_level = form.cleaned_data['activity_level']

            # Basic BMR calculation
            bmr = 10 * weight + 6.25 * height - 5 * age
            if activity_level == 'sedentary':
                calories = bmr * 1.2
            elif activity_level == 'moderate':
                calories = bmr * 1.55
            else:
                calories = bmr * 1.75

            return render(request, 'calorie_result.html', {'calories': round(calories)})

    else:
        form = CalorieCalculatorForm()
    return render(request, 'calorie_calculator.html', {'form': form})