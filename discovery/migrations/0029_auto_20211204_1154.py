# Generated by Django 3.1.7 on 2021-12-04 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0028_auto_20211203_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedcreators',
            name='offered_budget',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='assignedcreators',
            name='settled_amount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
