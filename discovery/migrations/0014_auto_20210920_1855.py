# Generated by Django 3.1.7 on 2021-09-20 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0013_auto_20210920_1853'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='list_name',
            new_name='campaign_name',
        ),
        migrations.RenameField(
            model_name='campaignlist',
            old_name='name',
            new_name='list_name',
        ),
    ]
