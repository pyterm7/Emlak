# Generated by Django 5.0.1 on 2024-01-29 20:29

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0002_remove_customuser_is_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Haqqında'),
        ),
    ]