# Generated by Django 5.0.7 on 2024-08-09 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_brand_name_alter_garage_name_alter_image_idcar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='caption',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
