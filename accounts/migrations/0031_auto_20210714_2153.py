# Generated by Django 3.1.7 on 2021-07-14 16:23

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_auto_20210714_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramdata',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.ig_profile_pic),
        ),
    ]
