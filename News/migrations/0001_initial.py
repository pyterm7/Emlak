# Generated by Django 5.0.1 on 2024-02-28 23:34

import django.db.models.deletion
import tinymce.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('NewsTag', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='News-covers/', verbose_name='Şəkil')),
                ('title', models.CharField(max_length=255, verbose_name='Başlıq')),
                ('description', tinymce.models.HTMLField(verbose_name='Məzmun')),
                ('is_active', models.BooleanField(default=False, verbose_name='Aktiv')),
                ('slug', models.CharField(blank=True, max_length=255, null=True, verbose_name='SLUG')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Müəllif')),
                ('tags', models.ManyToManyField(blank=True, related_name='tags', to='NewsTag.newstagmodel', verbose_name='Teqlər')),
            ],
            options={
                'verbose_name_plural': 'Xəbərlər',
            },
        ),
        migrations.CreateModel(
            name='LikedNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='İstifadəçi')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='News.newsmodel', verbose_name='Xəbər')),
            ],
            options={
                'verbose_name_plural': 'Bəyənilmiş xəbərlər',
            },
        ),
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
