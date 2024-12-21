from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


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
    gender = models.CharField(max_length=6, choices=[('female', 'Female'), ('male', 'Male')],default='female', null=True, blank=True)
    goal = models.CharField(
        max_length=50,
        choices=[
            ('gain muscle', 'Gain Muscle'),
            ('lose fat', 'Lose Fat'),
        ],
        default='gain muscle',
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


    diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE, related_name="meals")
    meal_time = models.CharField(max_length=50, choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('snack', 'Snack')])
    calories = models.PositiveIntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Meal ({self.meal_time}) in {self.diet_plan}"