# Generated by Django 3.1.7 on 2021-06-28 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engage', '0007_auto_20210628_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='paid_for',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gig',
            name='settled',
            field=models.BooleanField(default=False),
        ),
    ]