# Generated by Django 5.0.7 on 2024-07-28 22:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_car_hp_alter_car_mealage_alter_car_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='hp',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='mealage',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='seats',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(2)]),
        ),
    ]
