# Generated by Django 3.1.7 on 2021-12-06 04:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0047_merge_20211206_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='auth_token',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
