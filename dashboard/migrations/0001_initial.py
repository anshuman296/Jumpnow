# Generated by Django 3.1.7 on 2021-10-12 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(blank=True, choices=[('C', 'Creator'), ('M', 'Brand')], max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]