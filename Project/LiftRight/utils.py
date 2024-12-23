from datetime import timedelta
import os
import csv
import random
from io import BytesIO
from urllib import request
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from django.http import HttpResponse
from Settings import settings
from .models import DietPlan, WorkoutPlan, Meal, Exercise
from .factories import Factory

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

def read_exercises_from_csv():
    """Read exercises from the CSV file."""
    exercises = []
    file_path = 'WorkoutPlans/Datasets/exercises_expanded.csv'
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            exercises.append({
                'name': row['name'],
                'target_muscle': row['target_muscle'],
                'sets': int(row['sets']),
                'reps': int(row['reps']),
                'calories_burned': int(row.get('calories_burned', 0)),
            })
    return exercises

def read_food_items_from_csv():
    """Read food items from the CSV file."""
    food_items = []
    file_path = 'WorkoutPlans/Datasets/healthy_foods_expanded.csv'
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Adjust column names based on the actual CSV headers
            food_items.append({
                'food_item': row.get('food_item') or row.get('Food Item'),
                'calories_per_serving': int(row.get('Calories (per 100g)') or row.get('Calories Per 100g', 0)),
            })
    return food_items

# Generate PDF function
def generate_pdf(user, plan_type, weight, height, age, gender, activity_level, goal):
    # Validate inputs
    if not weight or not height or not age:
        raise ValueError("Weight, height, and age must be provided and valid.")

    if gender not in ['male', 'female']:
        raise ValueError("Gender must be 'male' or 'female'.")

    if activity_level not in ['sedentary', 'moderate', 'active']:
        raise ValueError("Activity level must be one of 'sedentary', 'moderate', or 'active'.")
    
    """Generate a PDF for the workout and food plan based on the plan type."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Add a personalized title
    title = Paragraph("Your Personalized Workout and Nutrition Plan", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))
    
# Add goal-based descriptions
    if goal == "gain muscle":
        workout_plan = generate_push_pull_legs()  # Push/Pull/Legs split for muscle gain
        intro_text = (
        "This plan is designed to help you build muscle effectively. "
        "It focuses on progressive overload with a mix of compound and isolation exercises to target all major muscle groups. "
        "Follow this plan consistently and fuel your body with the recommended nutrition for optimal results."
        )
    elif goal == "lose fat":
        workout_plan = generate_full_body_plan()  # Full-Body split for fat loss
        intro_text = (
            "This plan is designed to help you lose fat efficiently while maintaining muscle mass. "
            "It includes full-body workouts to maximize calorie burn and improve overall fitness. "
            "Pair this plan with the provided nutrition guide for a sustainable calorie deficit."
        )
    else:
        raise ValueError("Invalid goal specified")  # Handle unexpected goals

# Add the introduction dynamically
    introduction = Paragraph(intro_text, styles['BodyText'])
    elements.append(introduction)
    elements.append(Spacer(1, 20))

    # Add workout instructions
    instructions = Paragraph(
        "<b>How to Use This Plan:</b><br/>"
        "1. Perform the exercises on the designated days, following the sets and reps outlined.<br/>"
        "2. Rest adequately between sets, typically 1–2 minutes for compound exercises and 30–60 seconds for isolation exercises.<br/>"
        "3. Track your progress weekly and gradually increase weights as you get stronger.<br/>"
        "4. Use the nutrition guide to complement your workout plan and ensure you meet your caloric and macronutrient needs.<br/>",
        styles['BodyText']
    )
    elements.append(instructions)
    elements.append(Spacer(1, 20))

    # Dynamically generate the workout plan
    if plan_type == "full_body":
        workout_plan = generate_full_body_plan()
        days_per_week = 3
    elif plan_type == "upper_lower":
        workout_plan = generate_upper_lower_split()
        days_per_week = 4
    elif plan_type == "push_pull_legs":
        workout_plan = generate_push_pull_legs()
        days_per_week = 6
    else:
        raise ValueError("Invalid plan type")

    # Add the workout plan section
    elements.append(Paragraph("<b>Workout Plan:</b>", styles['Heading2']))
    for day, exercises in workout_plan.items():
        elements.append(Paragraph(f"<u>{day}</u>", styles['Heading3']))
        for exercise in exercises:
            elements.append(Paragraph(
                f"- {exercise['name']}: {exercise['sets']} sets of {exercise['reps']} reps",
                styles['BodyText']
            ))
        elements.append(Spacer(1, 10))
        
    # Add calorie recommendations
    elements.append(Paragraph("<b>Calorie Recommendations:</b>", styles['Heading2']))

    # Calculate BMR and calorie needs
    if gender == 'male':
        bmr = 10 * float(weight) + 6.25 * float(height) - 5 * float(age) + 5
    else:
        bmr = 10 * float(weight) + 6.25 * float(height) - 5 * float(age) - 161

    activity_multiplier = {'sedentary': 1.2, 'moderate': 1.55, 'active': 1.75}
    
    if goal == 'gain muscle':
        calories = round(bmr * activity_multiplier.get(activity_level, 1.2) + 500)
    elif goal == 'lose fat':
        calories = round(bmr * activity_multiplier.get(activity_level, 1.2) - 500)
    else:
        calories = round(bmr * activity_multiplier.get(activity_level, 1.2))  # Default for maintenance

    # Macronutrient calculations
    protein = round(weight * 2)  # 2g of protein per kg
    fats = round(calories * 0.25 / 9)  # 25% of calories from fats
    carbs = round((calories - (protein * 4 + fats * 9)) / 4)

    elements.append(Paragraph(
        f"Based on your data, your estimated daily calorie needs are: <b>{calories} kcal</b>.<br/>"
        f"Suggested macronutrient breakdown:<br/>"
        f"- Protein: {protein}g<br/>"
        f"- Fats: {fats}g<br/>"
        f"- Carbohydrates: {carbs}g<br/>",
        styles['BodyText']
    ))
    elements.append(Spacer(1, 20))

    # Add example foods from CSV
    elements.append(Paragraph("<b>Example Foods:</b>", styles['Heading2']))
    food_items = read_food_items_from_csv()
    for food in food_items[:18]:
        elements.append(Paragraph(
            f"- {food['food_item']}: {food['calories_per_serving']} calories per 100g",
            styles['BodyText']
        ))

    # Add a footer with encouragement
    footer = Paragraph(
        "Stick to your plan, track progress, and make adjustments as needed. Consistency is key!",
        styles['BodyText']
    )
    elements.append(footer)

    # Build the PDF
    doc.build(elements)
    
    
    save_workout_plan(user,goal,workout_plan,days_per_week, 8)
    save_diet_plan(user, goal, calories, protein,fats,carbs,food_items)

    # Return the generated PDF as a response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{plan_type}_workout_plan.pdf"'
    return response

def filter_exercises_by_muscle(exercises, target_muscle):
    """Filter exercises by the target muscle group."""
    return [exercise for exercise in exercises if exercise['target_muscle'].lower() == target_muscle.lower()]

def distribute_exercises(exercises, total_sets, max_sets_per_exercise=4):
    """
    Distribute total sets across multiple exercises for a muscle group.
    Ensures each exercise gets a maximum of `max_sets_per_exercise`.
    """
    distributed_exercises = []
    remaining_sets = total_sets

    for exercise in exercises:
        sets = min(remaining_sets, max_sets_per_exercise)
        distributed_exercises.append({
            "name": exercise['name'],
            "sets": sets,
            "reps": 8  # Default reps, can be adjusted dynamically
        })
        remaining_sets -= sets
        if remaining_sets <= 0:
            break

    return distributed_exercises

def generate_full_body_plan():
    """Generate a 3-day full-body workout plan dynamically."""
    exercises = read_exercises_from_csv()
    plan = {"Day 1": [], "Day 2": [], "Day 3": []}

    target_muscles = ['Quads', 'Chest', 'Back', 'Shoulders', 'Arms', 'Core', 'Hamstrings']
    weekly_sets = 12  # Total weekly sets per muscle group

    for target in target_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, target)
        random.shuffle(muscle_exercises)  # Shuffle to reduce repetition

        # Split weekly sets across 3 days
        sets_per_day = weekly_sets // 3
        for i, day in enumerate(plan.keys()):
            plan[day].extend(distribute_exercises(muscle_exercises, sets_per_day))
    
    return plan

def generate_upper_lower_split():
    """Generate a 4-day Upper/Lower workout split dynamically."""
    exercises = read_exercises_from_csv()
    plan = {"Day 1 (Upper)": [], "Day 2 (Lower)": [], "Day 3 (Upper)": [], "Day 4 (Lower)": []}

    upper_muscles = ['Chest', 'Back', 'Shoulders', 'Arms']
    lower_muscles = ['Quads', 'Hamstrings', 'Glutes', 'Calves']

    weekly_sets_upper = 16  # Total weekly sets for upper body
    weekly_sets_lower = 20  # Total weekly sets for lower body

    # Distribute exercises for upper body
    for muscle in upper_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle)
        random.shuffle(muscle_exercises)
        sets_per_session = weekly_sets_upper // 2  # Split across 2 upper days
        for day in ["Day 1 (Upper)", "Day 3 (Upper)"]:
            plan[day].extend(distribute_exercises(muscle_exercises, sets_per_session))

    # Distribute exercises for lower body
    for muscle in lower_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle)
        random.shuffle(muscle_exercises)
        sets_per_session = weekly_sets_lower // 2  # Split across 2 lower days
        for day in ["Day 2 (Lower)", "Day 4 (Lower)"]:
            plan[day].extend(distribute_exercises(muscle_exercises, sets_per_session))

    return plan

def generate_push_pull_legs():
    """Generate a 6-day Push/Pull/Legs workout split dynamically."""
    exercises = read_exercises_from_csv()
    plan = {
        "Day 1 (Push)": [], "Day 2 (Pull)": [], "Day 3 (Legs)": [],
        "Day 4 (Push)": [], "Day 5 (Pull)": [], "Day 6 (Legs)": []
    }

    push_muscles = ['Chest', 'Shoulders', 'Triceps']
    pull_muscles = ['Back', 'Biceps']
    leg_muscles = ['Quads', 'Hamstrings', 'Glutes', 'Calves']

    weekly_sets = {
        "Push": 15,  # Total weekly sets for push muscles
        "Pull": 15,  # Total weekly sets for pull muscles
        "Legs": 18   # Total weekly sets for legs
    }

    # Distribute exercises for push days
    for muscle in push_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle)
        random.shuffle(muscle_exercises)
        sets_per_day = weekly_sets["Push"] // 2
        for day in ["Day 1 (Push)", "Day 4 (Push)"]:
            plan[day].extend(distribute_exercises(muscle_exercises, sets_per_day))

    # Distribute exercises for pull days
    for muscle in pull_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle)
        random.shuffle(muscle_exercises)
        sets_per_day = weekly_sets["Pull"] // 2
        for day in ["Day 2 (Pull)", "Day 5 (Pull)"]:
            plan[day].extend(distribute_exercises(muscle_exercises, sets_per_day))

    # Distribute exercises for leg days
    for muscle in leg_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle)
        random.shuffle(muscle_exercises)
        sets_per_day = weekly_sets["Legs"] // 2
        for day in ["Day 3 (Legs)", "Day 6 (Legs)"]:
            plan[day].extend(distribute_exercises(muscle_exercises, sets_per_day))

    return plan

def load_exercises_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            Exercise.objects.create(
                name=row['name'],
                target_muscle=row['target_muscle'],
                equipment=row.get('equipment'),
                sets=int(row['sets']),
                reps=int(row['reps']),
                rest_time=row.get('rest_time', '00:01:00')  # Default 1-minute rest
            )

def load_meals_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            Meal.objects.create(
                name=row['meal_name'],
                calories=int(row['calories']),
                protein=float(row['protein']),
                fats=float(row['fats']),
                carbohydrates=float(row['carbohydrates'])
            )

def save_workout_plan(user, goal, plan, days_per_week, duration_weeks):
    """
    Save the workout plan and its exercises.

    Args:
    - user: The user for whom the plan is generated.
    - goal: The user's goal (e.g., "gain muscle", "lose fat").
    - plan: A dictionary containing the day-wise workout split.
    - days_per_week: Number of workout days per week.
    - duration_weeks: Duration of the plan in weeks.
    """
    workout_plan = Factory.create_workout_plan(
        user=user,
        goal=goal,
        days_per_week=days_per_week,
        duration_weeks=duration_weeks,
        exercises=[
            Factory.create_exercise(
                name=exercise_data['name'],
                equipment=None,
                sets=exercise_data.get('sets', 0),
                reps=exercise_data.get('reps', 0),
                rest_time="00:01:00",
            )
            for exercises in plan.values()
            for exercise_data in exercises
        ]
    )

def save_diet_plan(user, goal, calories, protein, fats, carbs, food_items):
    """
    Save the diet plan, its macronutrient breakdown, and link meals.

    Args:
    - user: The user for whom the plan is generated.
    - goal: The user's goal (e.g., "gain muscle", "lose fat").
    - calories: Total daily calorie requirement.
    - protein: Protein intake in grams.
    - fats: Fat intake in grams.
    - carbs: Carbohydrate intake in grams.
    - food_items: A list of example meals.
    """
    diet_plan = Factory.create_diet_plan(
        user=user,
        goal=goal,
        calories=calories,
        protein=protein,
        fats=fats,
        carbohydrates=carbs,
        meals=[
            Factory.create_meal(
                name=food['food_item'],
                calories=food['calories_per_serving'],
                protein=random.uniform(5, 15),
                fats=random.uniform(2, 10),
                carbohydrates=random.uniform(10, 30),
            )
            for food in food_items[:18]
        ]
    )

