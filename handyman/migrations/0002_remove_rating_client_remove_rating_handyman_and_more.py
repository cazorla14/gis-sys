# Generated by Django 4.2.2 on 2023-06-30 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_remove_booking_client_remove_booking_handyman_and_more'),
        ('handyman', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='client',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='handyman',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='booking',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='handyman',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]
