# Generated by Django 3.1.7 on 2021-12-01 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0023_auto_20211201_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='assigned_creators',
            field=models.ManyToManyField(blank=True, to='discovery.AssignedCreators'),
        ),
    ]
