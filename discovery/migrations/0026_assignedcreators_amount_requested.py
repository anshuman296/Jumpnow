# Generated by Django 3.1.7 on 2021-12-03 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0025_auto_20211201_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedcreators',
            name='amount_requested',
            field=models.BooleanField(default=False),
        ),
    ]
