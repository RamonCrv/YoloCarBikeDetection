# Generated by Django 4.0.4 on 2022-05-15 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_detections'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='detections',
            table='detections',
        ),
        migrations.AlterModelTable(
            name='trains',
            table='trains',
        ),
    ]
