# Generated by Django 3.2.8 on 2022-04-22 07:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Game_Participant',
            new_name='GameParticipant',
        ),
    ]
