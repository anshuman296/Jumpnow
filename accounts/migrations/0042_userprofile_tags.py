# Generated by Django 3.1.7 on 2021-10-25 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0041_auto_20211025_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='tags',
            field=models.CharField(blank=True, choices=[('F', 'Fashion'), ('S', 'SPORTS'), ('O', 'Other')], max_length=100, null=True),
        ),
    ]
