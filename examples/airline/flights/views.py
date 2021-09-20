# Django imports
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Model classes
from .models import Flights, Passengers


# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flights.objects.all()
    })

def flight(request, flight_id):
    flight = Flights.objects.get(id=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers":flight.passengers.all(),
        # Adding passengers who are not on this flight
        "non_passengers": Passengers.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    if request.method == "POST":
        # Getting the flight
        flight = Flights.objects.get(pk=flight_id)
        # Getting the passenger from the form
        passenger_id = int(request.POST["passenger"])
        passenger = Passengers.objects.get(pk=passenger_id)
        # Adding a passenger to a flight
        passenger.flights.add(flight)
        # Sending the user to the flight page

        return HttpResponseRedirect(reverse("flights:flight", args=(flight.id, )))