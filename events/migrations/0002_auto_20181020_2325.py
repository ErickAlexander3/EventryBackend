# Generated by Django 2.1.2 on 2018-10-21 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_date',
        ),
        migrations.AddField(
            model_name='event',
            name='event_end_time',
            field=models.DateTimeField(null=True, verbose_name='start date and time'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_pic',
            field=models.ImageField(default='event_picts/None/no-img.jpg', upload_to='event_pics/'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_price',
            field=models.DecimalField(decimal_places=2, default='0.0', max_digits=7),
        ),
        migrations.AddField(
            model_name='event',
            name='event_qrenabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='event_start_time',
            field=models.DateTimeField(null=True, verbose_name='start date and time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_description',
            field=models.CharField(blank=True, default='New event', max_length=100),
        ),
    ]
