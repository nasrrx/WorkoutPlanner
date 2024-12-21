from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Updated User model with relationships to WorkoutPlan and DietPlan
class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True,validators=[MinValueValidator(13)])
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[
            MinValueValidator(30.0),  
            MaxValueValidator(300.0) 
        ])
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[
            MinValueValidator(140.0),  
            MaxValueValidator(250.0)  
        ])
    gender = models.CharField(max_length=6, choices=[('female', 'Female'), ('male', 'Male')], null=True, blank=True)
    goal = models.CharField(
        max_length=50,
        choices=[
            ('gain muscle', 'Gain Muscle'),
            ('lose fat', 'Lose Fat'),
        ],
        null=True,
        blank=True
    )
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    plan_type = models.CharField(
        max_length=50,
        choices=[
            ('full_body', '3-Day Full Body'),
            ('upper_lower', '4-Day Upper/Lower'),
            ('push_pull_legs', '6-Day Push/Pull/Legs'),
        ],
        default='full_body',  
        null=True,
        blank=True
    )
    activity_level = models.CharField(
        max_length=50,
        choices=[
            ('sedentary', 'Sedentary'),
            ('moderate', 'Moderate Activity'),
            ('active', 'Active'),
        ],
        default='moderate',  
        null=True,
        blank=True
    )

# Exercise model
class Exercise(models.Model):
    name = models.CharField(max_length=255)
    target_muscle = models.CharField(max_length=255)
    equipment = models.CharField(max_length=255, null=True, blank=True)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    rest_time = models.DurationField()

    def __str__(self):
        return self.name

# WorkoutPlan model
class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workout_plans")
    goal = models.CharField(max_length=50)
    days_per_week = models.PositiveIntegerField()
    duration_weeks = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return f"Workout Plan for {self.user.username} - {self.goal}"

# DietPlan model
class DietPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diet_plans")
    goal = models.CharField(max_length=50)
    calories = models.PositiveIntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diet Plan for {self.user.username} - {self.goal}"

# Meals model
class Meal(models.Model):
    diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE, related_name="meals")
    meal_time = models.CharField(max_length=50, choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('snack', 'Snack')])
    calories = models.PositiveIntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Meal ({self.meal_time}) in {self.diet_plan}"