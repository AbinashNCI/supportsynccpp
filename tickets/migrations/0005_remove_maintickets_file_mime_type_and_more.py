# Generated by Django 4.2.11 on 2024-04-19 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_maintickets_file_mime_type_maintickets_file_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintickets',
            name='file_mime_type',
        ),
        migrations.RemoveField(
            model_name='maintickets',
            name='file_name',
        ),
    ]
