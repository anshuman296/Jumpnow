# Generated by Django 3.1.7 on 2021-12-01 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0052_delete_acceptedcampaign'),
        ('discovery', '0021_auto_20211201_1620'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Assigned_creators',
            new_name='AssignedCreators',
        ),
    ]
