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
                'calories_per_serving': int(row.get('calories_per_serving') or row.get('Calories Per Serving', 0)),
            })
    return food_items

# Generate PDF function
def generate_pdf(plan_type, food_items):
   
    """Generate a PDF for the workout and food plan based on the plan type."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Add a personalized title
    title = Paragraph("Your Personalized Workout and Nutrition Plan", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    goalNew = "gain muscle"
    
# Add goal-based descriptions
    if goalNew == "gain muscle":
        workout_plan = generate_push_pull_legs()  # Push/Pull/Legs split for muscle gain
        intro_text = (
        "This plan is designed to help you build muscle effectively. "
        "It focuses on progressive overload with a mix of compound and isolation exercises to target all major muscle groups. "
        "Follow this plan consistently and fuel your body with the recommended nutrition for optimal results."
        )
    elif goalNew == "lose fat":
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
    elif plan_type == "upper_lower":
        workout_plan = generate_upper_lower_split()
    elif plan_type == "push_pull_legs":
        workout_plan = generate_push_pull_legs()
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

    # Add the nutrition guide
    elements.append(Paragraph("<b>Nutrition Guide:</b>", styles['Heading2']))
    for food in food_items:
        elements.append(Paragraph(
            f"- {food['food_item']}: {food['calories_per_serving']} calories per serving",
            styles['BodyText']
        ))
    elements.append(Spacer(1, 20))

    # Add a footer with encouragement
    footer = Paragraph(
        "Remember: Consistency is the key to success. Stick to your plan, track your progress, and adjust as needed. "
        "You’ve got this!",
        styles['BodyText']
    )
    elements.append(footer)

    # Build the PDF
    doc.build(elements)

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

    plan = {
        "Day 1": [],
        "Day 2": [],
        "Day 3": []
    }

    target_muscles = ['Quads', 'Chest', 'Back', 'Shoulders', 'Arms', 'Core', 'Hamstrings']
    weekly_sets = 12  # Example: Total weekly sets per muscle group

    for target in target_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, target)
        if not muscle_exercises:
            continue

        # Shuffle exercises to add variety across days
        random.shuffle(muscle_exercises)

        # Split weekly sets across 3 days
        sets_per_day = weekly_sets // 3
        for i, day in enumerate(plan.keys()):
            plan[day].extend(distribute_exercises(muscle_exercises, sets_per_day))

    return plan

def generate_upper_lower_split():
    """Generate a 4-day Upper/Lower workout split dynamically."""
    exercises = read_exercises_from_csv()

    plan = {
        "Day 1 (Upper)": [],
        "Day 2 (Lower)": [],
        "Day 3 (Upper)": [],
        "Day 4 (Lower)": []
    }

    upper_muscles = ['Chest', 'Back', 'Shoulders', 'Arms']
    lower_muscles = ['Quads', 'Hamstrings', 'Glutes', 'Calves']

    weekly_sets_upper = 16  # Total weekly sets for upper body
    weekly_sets_lower = 20  # Total weekly sets for lower body

    # Distribute exercises for upper body
    for muscle_group in upper_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle_group)
        if not muscle_exercises:
            continue

        sets_per_session = weekly_sets_upper // 2
        for i, day in enumerate(["Day 1 (Upper)", "Day 3 (Upper)"]):
            plan[day].extend(distribute_exercises(muscle_exercises, sets_per_session))

    # Distribute exercises for lower body
    for muscle_group in lower_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle_group)
        if not muscle_exercises:
            continue

        sets_per_session = weekly_sets_lower // 2
        for i, day in enumerate(["Day 2 (Lower)", "Day 4 (Lower)"]):
            plan[day].extend(distribute_exercises(muscle_exercises, sets_per_session))

    return plan

def generate_push_pull_legs():
    """Generate a 6-day Push/Pull/Legs workout split dynamically."""
    exercises = read_exercises_from_csv()

    plan = {
        "Day 1 (Push)": [],
        "Day 2 (Pull)": [],
        "Day 3 (Legs)": [],
        "Day 4 (Push)": [],
        "Day 5 (Pull)": [],
        "Day 6 (Legs)": []
    }

    push_muscles = ['Chest', 'Shoulders', 'Triceps']
    pull_muscles = ['Back', 'Biceps']
    leg_muscles = ['Quads', 'Hamstrings', 'Glutes', 'Calves']  # Add all lower body muscles

    weekly_sets = {
        "Push": 15,
        "Pull": 15,
        "Legs": 18
    }

    # Distribute exercises for push days
    for muscle_group in push_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle_group)
        sets_per_day = weekly_sets["Push"] // 2
        for i, day in enumerate(["Day 1 (Push)", "Day 4 (Push)"]):
            plan[day].extend(distribute_exercises(muscle_exercises, sets_per_day))

    # Distribute exercises for pull days
    for muscle_group in pull_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle_group)
        sets_per_day = weekly_sets["Pull"] // 2
        for i, day in enumerate(["Day 2 (Pull)", "Day 5 (Pull)"]):
            plan[day].extend(distribute_exercises(muscle_exercises, sets_per_day))

    # Distribute exercises for leg days
    for muscle_group in leg_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle_group)
        sets_per_day = weekly_sets["Legs"] // 2
        for i, day in enumerate(["Day 3 (Legs)", "Day 6 (Legs)"]):
            plan[day].extend(distribute_exercises(muscle_exercises, sets_per_day))

    return plan
    """Generate a 6-day Push/Pull/Legs workout split dynamically."""
    exercises = read_exercises_from_csv()

    plan = {
        "Day 1 (Push)": [],
        "Day 2 (Pull)": [],
        "Day 3 (Legs)": [],
        "Day 4 (Push)": [],
        "Day 5 (Pull)": [],
        "Day 6 (Legs)": []
    }

    push_muscles = ['Chest', 'Shoulders', 'Triceps']
    pull_muscles = ['Back', 'Biceps']
    leg_muscles = ['Legs', 'Calves']

    weekly_sets = {
        "Push": 15,  # Total sets for push muscles per week
        "Pull": 15,  # Total sets for pull muscles per week
        "Legs": 18   # Total sets for legs per week
    }

    for muscle_group in push_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle_group)
        sets_per_day = weekly_sets["Push"] // 2
        for i, day in enumerate(["Day 1 (Push)", "Day 4 (Push)"]):
            if i < len(muscle_exercises):
                plan[day].append({
                    "name": muscle_exercises[i]['name'],
                    "sets": sets_per_day,
                    "reps": 8
                })

    for muscle_group in pull_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle_group)
        sets_per_day = weekly_sets["Pull"] // 2
        for i, day in enumerate(["Day 2 (Pull)", "Day 5 (Pull)"]):
            if i < len(muscle_exercises):
                plan[day].append({
                    "name": muscle_exercises[i]['name'],
                    "sets": sets_per_day,
                    "reps": 8
                })

    for muscle_group in leg_muscles:
        muscle_exercises = filter_exercises_by_muscle(exercises, muscle_group)
        sets_per_day = weekly_sets["Legs"] // 2
        for i, day in enumerate(["Day 3 (Legs)", "Day 6 (Legs)"]):
            if i < len(muscle_exercises):
                plan[day].append({
                    "name": muscle_exercises[i]['name'],
                    "sets": sets_per_day,
                    "reps": 8
                })

    return plan
