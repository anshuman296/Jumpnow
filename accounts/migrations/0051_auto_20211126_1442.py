# Generated by Django 3.1.7 on 2021-11-26 09:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discovery', '0020_auto_20211124_1750'),
        ('accounts', '0050_accepted_campaign'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Accepted_campaign',
            new_name='AcceptedCampaign',
        ),
    ]
