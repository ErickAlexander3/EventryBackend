# Generated by Django 2.1.2 on 2018-11-26 06:49

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20181126_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_pic',
            field=models.ImageField(null=True, upload_to=events.models.path_and_rename),
        ),
    ]
