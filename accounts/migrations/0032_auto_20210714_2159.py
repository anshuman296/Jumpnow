# Generated by Django 3.1.7 on 2021-07-14 16:29

import accounts.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20210714_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramdata',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/media/'), upload_to=accounts.models.ig_profile_pic),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/media/'), upload_to='marketer/'),
        ),
    ]
