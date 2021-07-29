from django.db import models

# Create your models here.
# Each object is a table that django will create for us 
class Flights(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()
    