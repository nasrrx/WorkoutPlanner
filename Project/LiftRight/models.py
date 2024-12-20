from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True,validators=[MinValueValidator(13)]
    )
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=[('female', 'Female'), ('male', 'Male')], null=True, blank=True)
    goal = models.CharField(max_length=50, 
        choices=[('gain muscle', 'Gain Muscle'),
            ('lose fat', 'Lose Fat'),
            ('body decomposition', 'Body Decomposition'),
            ('endurance', 'Endurance'),
            ('strength', 'Strength')],null=True,blank=True)
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
   