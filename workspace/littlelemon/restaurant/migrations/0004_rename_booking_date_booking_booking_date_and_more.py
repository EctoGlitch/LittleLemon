# Generated by Django 5.1.2 on 2024-11-03 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_alter_booking_booking_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='Booking_date',
            new_name='booking_date',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='ID',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='No_of_guests',
            new_name='no_of_guests',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='ID',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='Inventory',
            new_name='inventory',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='Price',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='Title',
            new_name='title',
        ),
    ]