from django.db import models
import django.utils.timezone

# Create your models here.
class Booking(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    No_of_guests = models.IntegerField(6)
    Booking_date = models.DateField() # default=django.utils.timezone.now
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        
    def __str__(self):
        return f'{self.Name} has booked for {self.No_of_guests} guests on {self.Booking_date}'
    
class Menu(models.Model):
    ID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Inventory = models.IntegerField(5)
    
    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
    
    def __str__(self):
        return self.Title