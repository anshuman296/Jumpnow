# Generated by Django 3.1.7 on 2021-06-10 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_auto_20210610_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalyoutubedata',
            name='channel_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='youtubedata',
            name='channel_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
