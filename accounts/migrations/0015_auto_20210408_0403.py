# Generated by Django 3.1.7 on 2021-04-07 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20210308_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsocialmedia',
            name='celebrity',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='socialmedia',
            name='celebrity',
            field=models.BooleanField(default=False),
        ),
    ]
