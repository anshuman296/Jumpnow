# Generated by Django 3.1.7 on 2021-03-07 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20210308_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltwitterdata',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='twitterdata',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
