# Generated by Django 5.0.1 on 2024-02-22 20:44

import Auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('City', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='Profile/', verbose_name='Profil şəkli')),
                ('passport', models.ImageField(blank=True, null=True, upload_to='Passport/', verbose_name='Şəxsiyyət vəsiqəsi')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Ad')),
                ('surname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Soyad')),
                ('position', models.CharField(blank=True, max_length=100, null=True, verbose_name='Vəzifə')),
                ('username', models.CharField(blank=True, max_length=50, null=True, verbose_name='İstifadəçi adı')),
                ('phone', models.CharField(max_length=13, unique=True, verbose_name='Telefon')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-poçt')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Haqqında')),
                ('facebook', models.CharField(blank=True, max_length=225, null=True, verbose_name='Facebook')),
                ('instagram', models.CharField(blank=True, max_length=225, null=True, verbose_name='İnstagram')),
                ('youtube', models.CharField(blank=True, max_length=225, null=True, verbose_name='YouTube')),
                ('twitter', models.CharField(blank=True, max_length=225, null=True, verbose_name='Twitter')),
                ('tiktok', models.CharField(blank=True, max_length=225, null=True, verbose_name='TikTok')),
                ('vimeo', models.CharField(blank=True, max_length=225, null=True, verbose_name='Vimeo')),
                ('pinterest', models.CharField(blank=True, max_length=225, null=True, verbose_name='Pinterest')),
                ('voen', models.CharField(blank=True, max_length=100, null=True, verbose_name='Vöen')),
                ('location', models.CharField(blank=True, max_length=225, null=True, verbose_name='Yaşadığı ünvan')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktiv kimi işarələ')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Agent kimi işarələ')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Admin kimi işarələ')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='City.city', verbose_name='İş ünvanı')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('parent_agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agency_team', to=settings.AUTH_USER_MODEL, verbose_name='Daxil olduğu agentlik')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'istifadəçi',
                'verbose_name_plural': 'İstifadəçilər',
            },
            managers=[
                ('objects', Auth.models.CustomUserManager()),
            ],
        ),
    ]
