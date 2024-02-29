# Generated by Django 5.0.1 on 2024-02-28 23:34

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_description', models.TextField(verbose_name='Meta açıqlama')),
                ('meta_keywords', models.TextField(verbose_name='Meta açar sözlər')),
                ('image', models.ImageField(blank=True, null=True, upload_to='About/', verbose_name='Haqqımızda səhifəsi üçün şəkil')),
                ('experience_year', models.SmallIntegerField(verbose_name='Təcrübə ili')),
                ('title', models.CharField(max_length=50, verbose_name='Başlıq')),
                ('subtitle', models.CharField(max_length=50, verbose_name='Alt başlıq')),
                ('location', models.CharField(max_length=225, verbose_name='Ünvan')),
                ('description', tinymce.models.HTMLField(verbose_name='Haqqımızda məlumat')),
                ('short_description', models.TextField(verbose_name='Qısa məlumat')),
                ('phone', models.CharField(max_length=20, verbose_name='Telefon 1')),
                ('phone_2', models.CharField(max_length=20, verbose_name='Telefon 2')),
                ('email', models.EmailField(max_length=254, verbose_name='E-poçt 1')),
                ('email_2', models.EmailField(max_length=254, verbose_name='E-poçt 2')),
                ('usage_ruler', tinymce.models.HTMLField(verbose_name='İstifadə qaydası')),
                ('terms_and_conditions', tinymce.models.HTMLField(verbose_name='Qaydalar və şərtlər')),
                ('facebook', models.CharField(blank=True, max_length=225, null=True, verbose_name='Facebook')),
                ('instagram', models.CharField(blank=True, max_length=225, null=True, verbose_name='İnstagram')),
                ('youtube', models.CharField(blank=True, max_length=225, null=True, verbose_name='YouTube')),
                ('twitter', models.CharField(blank=True, max_length=225, null=True, verbose_name='Twitter')),
                ('tiktok', models.CharField(blank=True, max_length=225, null=True, verbose_name='TikTok')),
                ('vimeo', models.CharField(blank=True, max_length=225, null=True, verbose_name='Vimeo')),
                ('pinterest', models.CharField(blank=True, max_length=225, null=True, verbose_name='Pinterest')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Haqqımızda',
            },
        ),
    ]
