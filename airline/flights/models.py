from django.db import models

# Create your models here.
# Each object is a table that django will create for us 

class Airport(models.Model):
    # variables are columns
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    # Magic Method for printing 
    def __str__(self):
        return f"{self.city} ({self.code})"

class Flights(models.Model):
    origin = models.ForeignKey(
        # Foreign Key Model
        Airport, 
        # When a foreign key is deleted so are all rows that refrence it
        on_delete=models.CASCADE,
        # Name that can be used when refrences origin from the Airport model
        related_name="departures"
        )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="arrivals"
    )
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"