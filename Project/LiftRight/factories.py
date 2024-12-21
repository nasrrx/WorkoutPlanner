from datetime import timedelta
from django.contrib.auth import get_user_model
from LiftRight.models import Exercise, Meal, DietPlan, WorkoutPlan

User = get_user_model()


class Factory:
    @staticmethod
    def create_user(username, email, password, **kwargs):
        """
        Factory method to create a User.
        Additional kwargs can include fields like age, height, weight, etc.
        """
        return User.objects.create_user(username=username, email=email, password=password, **kwargs)


    @staticmethod
    def update_user(user, data):
        """
        Factory method to update a User.
        """
        user.plan_type = data.get('plan_type', user.plan_type)
        user.age = data.get('age', user.age)
        user.weight = data.get('weight', user.weight)
        user.height = data.get('height', user.height)
        user.gender = data.get('gender', user.gender)
        user.goal = data.get('goal', user.goal)
        user.body_fat_percentage = data.get('body_fat_percentage', user.body_fat_percentage)
        user.activity_level = data.get('activity_level', user.activity_level)
        user.save()
        return user

    @staticmethod
    def create_exercise(name, equipment=None, sets=0, reps=0, rest_time="00:01:00"):
        """
        Factory method to create an Exercise.
        Converts rest_time to a timedelta object.
        """
        rest_time_duration = timedelta(minutes=int(rest_time.split(":")[1]))
        return Exercise.objects.create(
            name=name,
            equipment=equipment,
            sets=sets,
            reps=reps,
            rest_time=rest_time_duration,
        )

    @staticmethod
    def create_meal(name, calories=0, protein=0.0, fats=0.0, carbohydrates=0.0):
        """
        Factory method to create a Meal.
        """
        return Meal.objects.create(
            name=name,
            calories=calories,
            protein=protein,
            fats=fats,
            carbohydrates=carbohydrates,
        )

    @staticmethod
    def create_diet_plan(user, goal, calories, protein, fats, carbohydrates, meals=None):
        """
        Factory method to create a DietPlan.
        Meals can be provided as a list of Meal objects.
        """
        diet_plan = DietPlan.objects.create(
            user=user,
            goal=goal,
            calories=calories,
            protein=protein,
            fats=fats,
            carbohydrates=carbohydrates,
        )
        if meals:
            diet_plan.meals.set(meals)
        return diet_plan

    @staticmethod
    def create_workout_plan(user, goal, days_per_week, duration_weeks, exercises=None):
        """
        Factory method to create a WorkoutPlan.
        Exercises can be provided as a list of Exercise objects.
        """
        workout_plan = WorkoutPlan.objects.create(
            user=user,
            goal=goal,
            days_per_week=days_per_week,
            duration_weeks=duration_weeks,
        )
        if exercises:
            workout_plan.exercises.set(exercises)
        return workout_plan
