# Generated by Django 3.1.7 on 2021-12-11 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0031_assignedcreators_delivarables'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivarables',
            name='type',
        ),
        migrations.AddField(
            model_name='delivarables',
            name='platform',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='delivarables',
            name='deliverable',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
