# Generated by Django 3.1.7 on 2021-03-22 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0002_discoveryprofile_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discoveryprofile',
            name='max_searches',
        ),
        migrations.AddField(
            model_name='discoveryprofile',
            name='subscription_searches',
            field=models.IntegerField(default=0),
        ),
    ]