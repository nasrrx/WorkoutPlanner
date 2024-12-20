import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.conf import settings
from .models import WorkoutPlan, Exercise, DietPlan

# Utility functions

def calculate_bmi(height, weight, age, gender):
    """Calculate BMI considering age, weight, height, and gender."""
    height_m = height / 100  # Convert height to meters
    base_bmi = weight / (height_m ** 2)

    # Adjust BMI based on age and gender
    if gender == 'male':
        age_adjustment = 0.1 * (age / 10)
    else:  # female
        age_adjustment = 0.15 * (age / 10)

    adjusted_bmi = base_bmi + age_adjustment
    return round(adjusted_bmi, 2)

def recommend_diet_and_workout(user):
    """Determine the appropriate diet and workout plan based on BMI and goals."""
    bmi = calculate_bmi(user.height, user.weight, user.age, user.gender)
    recommendations = {
        "diet_plan": None,
        "workout_plan": None,
        "guidelines": [],
        "bmi": bmi
    }

    if bmi > 25:
        if user.body_fat_percentage and user.body_fat_percentage > 20:
            recommendations["diet_plan"] = "Weight Loss Diet Plan"
            recommendations["workout_plan"] = "Cardio 4 hours per week"
            recommendations["guidelines"].extend([
                "Include walking, cycling, or swimming as cardio activities.",
                "Focus on a calorie deficit with a high-protein diet."
            ])
    elif bmi < 18:
        recommendations["diet_plan"] = "Weight Gain Diet Plan"
        recommendations["workout_plan"] = "Intense Weight Lifting"
        recommendations["guidelines"].extend([
            "Focus on compound exercises like squats, bench press, and deadlifts.",
            "Eat in a calorie surplus with high-protein and carb intake."
        ])
    else:
        recommendations["diet_plan"] = f"{user.goal.capitalize()} Diet Plan"
        recommendations["workout_plan"] = f"{user.goal.capitalize()} Workout Plan"
        recommendations["guidelines"].append("Follow a balanced approach aligned with your goals.")

    return recommendations

def generate_pdf(user):
    """Generate a PDF report for the user's workout and diet plan and save it in the MEDIA directory."""
    recommendations = recommend_diet_and_workout(user)
    relative_path = f"WorkoutPlans/{user.username}_plan.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    # Ensure directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"Workout and Diet Plan for {user.username}")

    # BMI and Basic Info
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"BMI: {recommendations['bmi']}")
    c.drawString(100, 700, f"Goal: {user.goal}")

    # Diet Plan
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 670, "Diet Plan:")
    c.setFont("Helvetica", 12)
    c.drawString(120, 650, recommendations["diet_plan"])

    # Guidelines
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 620, "Guidelines:")
    c.setFont("Helvetica", 12)
    y = 600
    for guideline in recommendations["guidelines"]:
        c.drawString(120, y, f"- {guideline}")
        y -= 20

    # Workout Plan
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y - 20, "Workout Plan:")
    c.setFont("Helvetica", 12)
    y -= 40
    c.drawString(120, y, recommendations["workout_plan"])

    # Save PDF
    c.save()

    # Save relative path to the workout plan
    workout_plan = WorkoutPlan.objects.filter(user=user).last()
    if workout_plan:
        workout_plan.pdf_path = relative_path
        workout_plan.save()

    return relative_path

def create_workout_plan(user):
    """Create a workout plan based on recommendations."""
    recommendations = recommend_diet_and_workout(user)
    workout_plan = WorkoutPlan.objects.create(
        user=user,
        goal=recommendations["workout_plan"],
        days_per_week=5 if "Weight Lifting" in recommendations["workout_plan"] else 3,
        duration_weeks=8
    )
    return workout_plan

def create_diet_plan(user):
    """Create a diet plan based on recommendations."""
    recommendations = recommend_diet_and_workout(user)
    return {
        "diet_plan": recommendations["diet_plan"],
        "guidelines": recommendations["guidelines"]
    }