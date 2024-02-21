# Generated by Django 5.0.1 on 2024-02-20 00:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=255, verbose_name='Şərh')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Müəllif')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='News.newsmodel', verbose_name='Xəbər')),
            ],
            options={
                'verbose_name_plural': 'Şərhlər',
            },
        ),
    ]