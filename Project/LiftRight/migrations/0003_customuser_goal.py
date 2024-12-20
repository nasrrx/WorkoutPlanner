# Generated by Django 5.1.3 on 2024-12-17 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LiftRight", "0002_customuser_gender"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="goal",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True
            ),
        ),
    ]