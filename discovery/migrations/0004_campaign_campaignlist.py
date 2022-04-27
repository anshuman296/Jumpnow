# Generated by Django 3.1.7 on 2021-04-08 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210408_0403'),
        ('discovery', '0003_auto_20210323_0033'),
    ]

    operations = [
        migrations.CreateModel(
            name='campaignList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('profiles', models.ManyToManyField(blank=True, to='accounts.SocialMedia')),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('lists', models.ManyToManyField(blank=True, to='discovery.campaignList')),
            ],
        ),
    ]