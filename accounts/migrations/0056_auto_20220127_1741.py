# Generated by Django 3.1.7 on 2022-01-27 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0055_auto_20220127_1353'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='bank_details',
            new_name='BankDetail',
        ),
    ]