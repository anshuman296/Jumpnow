# Generated by Django 3.1.7 on 2021-05-22 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20210522_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='address_line_1',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
