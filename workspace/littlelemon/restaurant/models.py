from django.db import models
import django.utils.timezone

# Create your models here.
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField(6)
    booking_date = models.DateField() # default=django.utils.timezone.now
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        
    def __str__(self):
        return f'{self.name} has booked for {self.no_of_guests} guests on {self.booking_date}'
    
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(5)
    
    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
    
    def __str__(self):
        return f'{self.title} : {str(self.price)}'