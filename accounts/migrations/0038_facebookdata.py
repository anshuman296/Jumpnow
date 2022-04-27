# Generated by Django 3.1.7 on 2021-09-23 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_remove_userprofile_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_data', models.JSONField(blank=True, null=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('social_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facebook', to='accounts.socialmedia')),
            ],
        ),
    ]