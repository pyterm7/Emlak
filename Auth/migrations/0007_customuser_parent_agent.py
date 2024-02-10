# Generated by Django 5.0.1 on 2024-02-10 12:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0006_customuser_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='parent_agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agency_team', to=settings.AUTH_USER_MODEL, verbose_name='Daxil olduğu agentlik'),
        ),
    ]