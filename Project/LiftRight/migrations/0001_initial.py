# Generated by Django 5.1.4 on 2024-12-21 18:48

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Exercise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("target_muscle", models.CharField(max_length=255)),
                ("equipment", models.CharField(blank=True, max_length=255, null=True)),
                ("sets", models.PositiveIntegerField()),
                ("reps", models.PositiveIntegerField()),
                (
                    "rest_time",
                    models.DurationField(default=datetime.timedelta(seconds=60)),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Meal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("calories", models.PositiveIntegerField()),
                ("protein", models.DecimalField(decimal_places=2, max_digits=5)),
                ("fats", models.DecimalField(decimal_places=2, max_digits=5)),
                ("carbohydrates", models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "age",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(13)],
                    ),
                ),
                (
                    "weight",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=5,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(30.0),
                            django.core.validators.MaxValueValidator(300.0),
                        ],
                    ),
                ),
                (
                    "height",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=5,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(140.0),
                            django.core.validators.MaxValueValidator(250.0),
                        ],
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("female", "Female"), ("male", "Male")],
                        default="female",
                        max_length=6,
                        null=True,
                    ),
                ),
                (
                    "goal",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("gain muscle", "Gain Muscle"),
                            ("lose fat", "Lose Fat"),
                        ],
                        default="gain muscle",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "body_fat_percentage",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "plan_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("full_body", "3-Day Full Body"),
                            ("upper_lower", "4-Day Upper/Lower"),
                            ("push_pull_legs", "6-Day Push/Pull/Legs"),
                        ],
                        default="full_body",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "activity_level",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("sedentary", "Sedentary"),
                            ("moderate", "Moderate Activity"),
                            ("active", "Active"),
                        ],
                        default="moderate",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="WorkoutPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("goal", models.CharField(max_length=50)),
                ("days_per_week", models.PositiveIntegerField()),
                ("duration_weeks", models.PositiveIntegerField()),
                ("exercises", models.ManyToManyField(to="LiftRight.exercise")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workout_plans",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DietPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("goal", models.CharField(max_length=50)),
                ("calories", models.PositiveIntegerField()),
                ("protein", models.DecimalField(decimal_places=2, max_digits=5)),
                ("fats", models.DecimalField(decimal_places=2, max_digits=5)),
                ("carbohydrates", models.DecimalField(decimal_places=2, max_digits=5)),
                ("meals", models.ManyToManyField(to="LiftRight.meal")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="diet_plans",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
