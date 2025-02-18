from django.db import models
import django.utils.timezone

# Create your models here.
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField(6)
    time_slot = models.SmallIntegerField(default=10)
    booking_date = models.DateField()
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        
    def __str__(self):
        return f'{self.name} has booked for {self.no_of_guests} guests on {self.booking_date}'
    
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=30, default='')
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(100)
    category_fk = models.ForeignKey(
        'Category', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        default=None
    )
    
    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
    
    def __str__(self):
        return f'{self.title} : {str(self.price)}'
    
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=30, default='')
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return f'{self.name}'