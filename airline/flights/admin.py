from django.contrib import admin

from .models import Flights, Airport, Passengers

# Register your models here.
admin.site.register(Airport)
admin.site.register(Flights)
admin.site.register(Passengers)