# Generated by Django 5.0.7 on 2024-07-30 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_image_idcar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='garage',
            new_name='gar',
        ),
    ]
