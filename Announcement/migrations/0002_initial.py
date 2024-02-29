# Generated by Django 5.0.1 on 2024-02-28 23:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Announcement', '0001_initial'),
        ('Category', '0001_initial'),
        ('City', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='announcementmodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Elan sahibi'),
        ),
        migrations.AddField(
            model_name='announcementmodel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Category.categorymodel', verbose_name='Kateqoriya'),
        ),
        migrations.AddField(
            model_name='announcementmodel',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='City.city', verbose_name='Şəhər'),
        ),
        migrations.AddField(
            model_name='announcementmodel',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='City.region', verbose_name='Rayon'),
        ),
        migrations.AddField(
            model_name='announcementmodel',
            name='zone_for_absheron',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='City.zoneforabsheron', verbose_name='Abşeron->Bölgə'),
        ),
        migrations.AddField(
            model_name='announcementmodel',
            name='zone_for_baku',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='City.zoneforbaku', verbose_name='Bakı->Rayon->Bölgə'),
        ),
        migrations.AddField(
            model_name='announcementpics',
            name='announcement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Announcement.announcementmodel', verbose_name='Elan'),
        ),
    ]
