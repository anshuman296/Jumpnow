# Generated by Django 3.1.7 on 2022-01-26 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0053_merge_20211215_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='bank_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('pan_no', models.CharField(blank=True, max_length=10, null=True)),
                ('gst_no', models.CharField(blank=True, max_length=15, null=True)),
                ('account_type', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('account_no', models.CharField(blank=True, max_length=100, null=True)),
                ('account_no_ver', models.CharField(blank=True, max_length=100, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank_details',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.bank_details'),
        ),
    ]
