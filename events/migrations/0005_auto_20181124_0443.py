# Generated by Django 2.1.2 on 2018-11-24 04:43

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20181120_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_location',
        ),
        migrations.AddField(
            model_name='event',
            name='event_address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_point_location',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]
