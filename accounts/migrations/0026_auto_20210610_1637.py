# Generated by Django 3.1.7 on 2021-06-10 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20210610_1636'),
    ]

    operations = [
        migrations.RenameField(
            model_name='youtubeauth',
            old_name='cliend_id',
            new_name='client_id',
        ),
    ]