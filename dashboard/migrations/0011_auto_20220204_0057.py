# Generated by Django 3.1.7 on 2022-02-03 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_delete_assignedcampaign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquiry',
            name='user_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]