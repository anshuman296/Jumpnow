# Generated by Django 3.1.7 on 2021-04-08 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0005_auto_20210408_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='discoveryprofile',
            name='exports_done',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='discoveryprofile',
            name='exports_max',
            field=models.IntegerField(blank=True, default=5, null=True),
        ),
    ]