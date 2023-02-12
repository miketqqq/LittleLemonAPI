from django.db import models

# Create your models here.
# Create your models here.
class Booking(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=255, db_index=True)
    no_of_guests = models.IntegerField()
    booking_date = models.DateField()

    def __str__(self):
        return self.name
    
class Menu(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()

    def __str__(self):
        return f'{self.title} : {str(self.price)}'
    
    def __repr__(self):
        return f'{self.title} : {str(self.price)}'