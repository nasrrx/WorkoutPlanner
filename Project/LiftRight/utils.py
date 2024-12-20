import os
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.conf import settings
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import render
from .models import WorkoutPlan, Exercise, DietPlan


# Utility functions

def calculate_bmi(height, weight, age, gender):
    """Calculate BMI considering age, weight, height, and gender."""
    height_m = height / 100  # Convert height to meters
    base_bmi = weight / (height_m ** 2)

    # Adjust BMI based on age and gender
    if gender == 'male':
        age_adjustment = float(0.1 * (age / 10))
    else:  # female
        age_adjustment = float(0.15 * (age / 10))

    adjusted_bmi = float(base_bmi) + float(age_adjustment)
    
    return float(round(adjusted_bmi, 2))

def generate_full_body_plan():
    """Generate a 3-day full-body workout plan from the dataset."""
    exercises = read_exercises_from_csv()
    # Example logic for Full Body (adjust days and muscles as needed)
    plan = {
        "Day 1": [ex for ex in exercises if ex['name'] in ['Squat', 'Bench Press', 'Deadlift']],
        "Day 2": [ex for ex in exercises if ex['name'] in ['Pull-Up', 'Overhead Press', 'Lunges']],
        "Day 3": [ex for ex in exercises if ex['name'] in ['Barbell Row', 'Plank', 'Push-Up']],
    }
    return plan

def generate_upper_lower_split():
    """Generate a 4-day Upper/Lower workout split."""
    exercises = read_exercises_from_csv()
    plan = {
        "Day 1 (Upper)": [ex for ex in exercises if ex['Target Muscle'] in ['Chest', 'Back', 'Shoulders', 'Arms']],
        "Day 2 (Lower)": [ex for ex in exercises if ex['Target Muscle'] in ['Legs']],
        "Day 3 (Upper)": [ex for ex in exercises if ex['Target Muscle'] in ['Chest', 'Back', 'Shoulders', 'Arms']],
        "Day 4 (Lower)": [ex for ex in exercises if ex['Target Muscle'] in ['Legs']],
    }
    return plan

def generate_push_pull_legs():
    """Generate a 6-day Push/Pull/Legs workout split."""
    exercises = read_exercises_from_csv()
    plan = {
        "Day 1 (Push)": [ex for ex in exercises if ex['Target Muscle'] in ['Chest', 'Shoulders', 'Triceps']],
        "Day 2 (Pull)": [ex for ex in exercises if ex['Target Muscle'] in ['Back', 'Biceps']],
        "Day 3 (Legs)": [ex for ex in exercises if ex['Target Muscle'] in ['Legs']],
        "Day 4 (Push)": [ex for ex in exercises if ex['Target Muscle'] in ['Chest', 'Shoulders', 'Triceps']],
        "Day 5 (Pull)": [ex for ex in exercises if ex['Target Muscle'] in ['Back', 'Biceps']],
        "Day 6 (Legs)": [ex for ex in exercises if ex['Target Muscle'] in ['Legs']],
    }
    return plan

# Read exercises from CSV
def read_exercises_from_csv():
    exercises = []
    with open('C:/Users/nasrr/Desktop/Workout Planner/WorkoutPlanner/Project/WorkoutPlans/Datasets/exercises_expanded.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            exercises.append({
                'name': row['Exercise'],  # Match the column name
                'sets': int(row['Sets']),
                'reps': int(row['Reps']),
                'calories_burned': 0,  # Add calculation if needed
            })
    return exercises

# Read food items from CSV

    food_items = []
    with open('WorkoutPlans/Datasets/healthy_foods_expanded.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            food_items.append({
                'food_item': row['food_item'],
                'calories_per_serving': int(row['calories_per_serving']),
            })
    return food_items

def read_food_items_from_csv():
    food_items = []
    with open('C:/Users/nasrr/Desktop/Workout Planner/WorkoutPlanner/Project/WorkoutPlans/Datasets/healthy_foods_expanded.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            food_items.append({
                'food_item': row['Food Item'],  # Match the column name
                'calories_per_serving': int(row['Calories (per 100g)']),  # Match column name
            })
    return food_items

# Generate PDF function
def generate_pdf(exercises, food_items):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Title
    c.setFont("Helvetica", 16)
    c.drawString(100, 750, "Workout Plan and Food Plan")

    # Exercises section
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Exercises:")
    y_position = 700
    for exercise in exercises:
        text = f"{exercise['name']} - {exercise['sets']} sets of {exercise['reps']} reps, Burned {exercise['calories_burned']} calories"
        c.drawString(100, y_position, text)
        y_position -= 20

    # Food Items section
    c.setFont("Helvetica", 12)
    c.drawString(100, y_position - 20, "Food Items and Calories:")
    y_position -= 40
    for food in food_items:
        c.drawString(100, y_position, f"{food['food_item']}: {food['calories_per_serving']} calories per serving")
        y_position -= 20

    # Save the PDF to the buffer
    c.save()

    # Create a response to return the PDF file
    buffer.seek(0)
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="workout_and_food_plan.pdf"'
    response.write(buffer.getvalue())
    return response

# Django view to call the generate_pdf function
def generate_workout_and_food_pdf(request):
    # Read exercises and food items from CSV files
    exercises = read_exercises_from_csv()
    food_items = read_food_items_from_csv()

    # Generate the PDF with the read data
    return generate_pdf(exercises, food_items)

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Title
    c.setFont("Helvetica", 16)
    c.drawString(100, 750, "Workout Plan and Diet Plan")

    # Exercises section
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Exercises:")
    y_position = 700
    for exercise in exercises:
        text = f"{exercise['name']} - {exercise.get('sets', '')} sets"
        if "reps" in exercise:
            text += f" of {exercise.get('reps', '')} reps"
        elif "seconds" in exercise:
            text += f" of {exercise.get('seconds', '')} seconds"
        c.drawString(100, y_position, text)
        y_position -= 20

    # Diet Plan section
    c.setFont("Helvetica", 12)
    c.drawString(100, y_position - 20, "Diet Plan:")
    y_position -= 40
    for meal in diet_plans:
        c.drawString(100, y_position, f"{meal['meal']}: {meal['food']}")
        y_position -= 20

    # Save the PDF to the buffer
    c.save()

    # Create a response to return the PDF file
    buffer.seek(0)
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="workout_and_diet_plan.pdf"'
    response.write(buffer.getvalue())
    return response
    """Create a diet plan based on recommendations."""
    recommendations = recommend_diet_and_workout(user)
    return {
        "diet_plan": recommendations["diet_plan"],
        "guidelines": recommendations["guidelines"]
    }