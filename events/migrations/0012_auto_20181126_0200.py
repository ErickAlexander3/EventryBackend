# Generated by Django 2.1.2 on 2018-11-26 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20181125_0843'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('-creation_date',)},
        ),
        migrations.AddField(
            model_name='event',
            name='room_id',
            field=models.CharField(max_length=150, null=True),
        ),
    ]