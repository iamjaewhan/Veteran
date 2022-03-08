# Generated by Django 3.2.8 on 2022-03-08 12:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 8, 12, 10, 29, 792060, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='game',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 8, 12, 10, 27, 840060, tzinfo=utc)),
        ),
    ]
