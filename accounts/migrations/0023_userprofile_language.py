# Generated by Django 3.1.7 on 2021-05-23 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20210523_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='language',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]