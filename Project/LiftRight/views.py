from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@pytest.mark.django_db
def RenderSignUpView(request): # 
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

@login_required
def LoadProfileUserData(request):
    user = request.user 
    
    bmi = CalculateBMI(user.height, user.weight)
    
    context = {
        'name': user.username,
        'email': user.email,
        'age': user.age,  
        'height': user.height,
        'weight': user.weight,
        'bmi': bmi,  
    }
    return render(request, 'Profile.html', context)

def RenderAboutPage(request):
    return render(request,'About.html')

def CalculateBMI(height, weight):
    height_m = height / 100  
    bmi = round(weight / (height_m ** 2), 2)
    return bmi  

def download_workout_plan(request):
    # Logic to determine the workout plan based on user data
    bmi = CalculateBMI(request.user.height, request.user.weight)  # Assuming the user has a BMI field in their profile
    if bmi < 18.5:
        filename = 'Muscle_Gain_Workout_Plan.pdf'
    elif bmi > 25:
        filename = 'Fat_Loss_Workout_Plan.pdf'
    else:
        filename = 'Muscle_Gain_Workout_Plan.pdf' 

    # Construct the file path
    file_path = os.path.join('WorkoutPlans', filename)  # Replace 'workout_plans' with the correct directory

    # Read and serve the file as a response
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

@csrf_exempt
@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Access the user directly and update fields
            user = request.user

            if hasattr(user, 'age'):
                user.age = data.get('age', user.age)
            if hasattr(user, 'weight'):
                user.weight = data.get('weight', user.weight)
            if hasattr(user, 'height'):
                user.height = data.get('height', user.height)

            user.save()
            return JsonResponse({'message': 'Profile updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

            