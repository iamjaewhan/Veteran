# Generated by Django 3.2.8 on 2021-11-26 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0001_initial'),
        ('Account', '0003_auto_20211125_1700'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('reviewer', 'reviewee', 'game')},
        ),
    ]