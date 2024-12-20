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
from .utils import generate_pdf, create_workout_plan, create_diet_plan, recommend_diet_and_workout

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

@login_required
def LoadProfileUserData(request):
    user = request.user

    # Generate workout and diet plan on profile load
    workout_plan = create_workout_plan(user)
    diet_plan = create_diet_plan(user)

    pdf_path = generate_pdf(user)  # Generate and save PDF

    context = {
        'name': user.username,
        'email': user.email,
        'age': user.age,
        'height': user.height,
        'weight': user.weight,
        'gender': user.gender,
        'goal': user.goal,
        'bmi': recommend_diet_and_workout(user)['bmi'],
        'diet_plan': diet_plan,
        'workout_plan': workout_plan,
        'pdf_path': pdf_path
    }

    return render(request, 'Profile.html', context)

@csrf_exempt
@login_required
def update_profile(request):
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

            # Regenerate plans and PDF
            create_workout_plan(user)
            create_diet_plan(user)
            generate_pdf(user)

            return JsonResponse({'message': 'Profile updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def download_workout_plan(request):
    """Serve the user's workout plan PDF for download."""
    user = request.user
    workout_plan = WorkoutPlan.objects.filter(user=user).last()

    if workout_plan and workout_plan.pdf_path:
        pdf_path = os.path.join(settings.MEDIA_ROOT, workout_plan.pdf_path)
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
                return response

    return JsonResponse({'error': 'Workout plan not found or PDF missing.'}, status=404)
