# Generated by Django 3.1.7 on 2021-11-26 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0020_auto_20211124_1750'),
        ('dashboard', '0007_auto_20211126_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignedcampaign',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_campaign', to='discovery.campaign'),
        ),
    ]
