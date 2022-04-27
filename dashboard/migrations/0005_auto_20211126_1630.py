# Generated by Django 3.1.7 on 2021-11-26 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0020_auto_20211124_1750'),
        ('dashboard', '0004_auto_20211126_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptedcampaign',
            name='assigned_campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='discovery.campaign'),
        ),
    ]