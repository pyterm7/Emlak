# Generated by Django 5.0.1 on 2024-02-22 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('City', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Rayonlar',
            },
        ),
    ]
