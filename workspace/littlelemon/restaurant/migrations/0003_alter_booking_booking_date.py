# Generated by Django 5.1.2 on 2024-11-03 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_alter_booking_options_alter_menu_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='Booking_date',
            field=models.DateField(),
        ),
    ]