# Generated by Django 4.2.2 on 2023-06-30 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_remove_booking_client_remove_booking_handyman_and_more'),
        ('handyman', '0002_remove_rating_client_remove_rating_handyman_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Booking',
        ),
        migrations.DeleteModel(
            name='JobRequest',
        ),
    ]
