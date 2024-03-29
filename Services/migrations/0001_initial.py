# Generated by Django 5.0.1 on 2024-02-28 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225, verbose_name='Başlıq')),
                ('description', models.TextField(verbose_name='Açıqlama')),
                ('icon', models.CharField(max_length=50, verbose_name='İkon')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Xidmətlərimiz',
            },
        ),
    ]
