from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import JsonResponse, HttpResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import User, WorkoutPlan
import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .utils import generate_pdf, calculate_bmi, read_exercises_from_csv, read_food_items_from_csv

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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user

            # Update user data
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
    """Generate and serve the user's workout plan as a PDF."""
    try:
        return generate_pdf(request.user)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    """Generate and serve a PDF with exercises and food items."""
    try:
        # Read exercises and food items
        exercises = read_exercises_from_csv()
        food_items = read_food_items_from_csv()

        # Generate the PDF
        response = generate_pdf(exercises, food_items)
        return response
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    try:
        # Read exercises and food items
        exercises = read_exercises_from_csv()
        food_items = read_food_items_from_csv()

        # Generate the PDF
        response = generate_pdf(exercises, food_items)
        return response
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
