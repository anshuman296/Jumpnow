# Generated by Django 3.1.7 on 2021-12-15 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0037_auto_20211214_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedcreators',
            name='settled',
            field=models.BooleanField(default=False),
        ),
    ]
