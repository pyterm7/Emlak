# Generated by Django 5.0.1 on 2024-01-29 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='E-poçt')),
                ('subject', models.CharField(max_length=100, verbose_name='Mövzu')),
                ('message', models.TextField(verbose_name='Mesaj')),
                ('ip_address', models.CharField(max_length=30, verbose_name='İP ünvan')),
                ('show', models.BooleanField(default=False, verbose_name='Bu mesaj saytda görünsün')),
                ('answer', models.BooleanField(default=False, verbose_name='Baxıldı və cavablandırıldı kimi işarələ')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Əlaqə mesajları',
            },
        ),
    ]