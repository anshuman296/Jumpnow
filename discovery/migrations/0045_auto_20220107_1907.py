# Generated by Django 3.1.7 on 2022-01-07 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0044_deliverables_confirmation_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('content_url', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='deliverables',
            name='content_review',
            field=models.ManyToManyField(blank=True, null=True, to='discovery.Content'),
        ),
    ]