# Generated by Django 3.1.7 on 2021-12-08 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0030_delivarables'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedcreators',
            name='delivarables',
            field=models.ManyToManyField(blank=True, null=True, to='discovery.Delivarables'),
        ),
    ]
