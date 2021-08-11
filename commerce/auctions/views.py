from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Wishlist, Comment
from .helpers import ListingForm, BidForm

def current_listing_price(listing):
    try:
        Bid.objects.get(item_id = listing.id, max_bid = True)
        old_bid = Bid.objects.get(item_id = listing.id, max_bid = True)
        old_bid.max_bid = False
        currentPrice = old_bid.price
    except:
        currentPrice = listing.starting_bid

    return currentPrice

def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings":listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def createListing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            # Creating a new listing model object if the form is valid
            newListing = Listing(
                owner = request.user,
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                starting_bid = form.cleaned_data['startingbid'],
                image = form.cleaned_data['image'],
                category = form.cleaned_data['category'],
                active = True
            )

            # Saving the new listing to the database
            newListing.save()

            # Returning the user to active listings 
            return HttpResponseRedirect(reverse("index"))
            

        # Form is not valid
        return render(request, "auctions/createListing.html", {
            "form":form
        })
    return render(request, "auctions/createListing.html", {
        "form":ListingForm()
    })


def viewListing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    try:
        request.user.wishlist.get(listing_id = listing_id)
        wishlist = True
    except:
        wishlist = False
    if Bid.objects.filter(item_id = listing.id, max_bid = True):
        maxBid = Bid.objects.get(item_id = listing.id, max_bid = True)
        currentPrice = maxBid.price
    else:
        currentPrice = listing.starting_bid
    return render(request, "auctions/viewListing.html", {
        "listing":Listing.objects.get(pk=listing_id),
        "currentPrice":currentPrice,
        "bidForm":BidForm(),
        "wishlist":wishlist
    })

def bid(request, listing_id):
    if request.method == "POST": 
        form = BidForm(request.POST)
        if form.is_valid():
            buyer = request.user
            # Getting the list item
            listing = Listing.objects.get(pk=listing_id)
            # Getting the curent price of the Item
            try:
                Bid.objects.get(item_id = listing.id, max_bid = True)
                old_bid = Bid.objects.get(item_id = listing.id, max_bid = True)
                old_bid.max_bid = False
                currentPrice = old_bid.price
            except:
                currentPrice = listing.starting_bid
            
            bid_price = form.cleaned_data["bid"]
            
            if bid_price <= currentPrice:
                return render(request, "auctions/viewListing.html", {
                    "listing":Listing.objects.get(pk=listing_id),
                    "currentPrice":currentPrice,
                    "bidForm":BidForm()
                    })

            # Adding a new bid 
            new_bid = Bid(item=listing, price=bid_price, max_bid=True)
            # Saving teh bid
            new_bid.save()
            # Adding a buyer
            buyer.bids.add(new_bid)
            # Saving the information about the old max 
            old_bid.save()
            
            # REturning the user back to View the item
            return HttpResponseRedirect(reverse('index'))

        # The form was not valid
        return render(request, "auctions/viewListing.html", {
                "listing":Listing.objects.get(pk=listing_id),
                "currentPrice":10,
                "bidForm":BidForm(),
                "wishlist":Wishlist.objects.get(listing_id=listing_id, )
                })

def closeAuction(request, listing_id):
        # Performign a SQL query to get the wishlist ID 
    wishlist_id = Listing.objects.raw(f'Select distinct(id) from auctions_wishlist where listing_id = {listing_id}')[0].id
    if request.method == "POST":
        pass

def addWishlist(request, listing_id):
    wishlist_id = Listing.objects.raw(f'Select distinct(id) from auctions_wishlist where listing_id = {listing_id}')[0].id
    if request.method == "POST":
        pass

def removeWishlist(request, listing_id):
    wishlist_id = Listing.objects.raw(f'Select distinct(id) from auctions_wishlist where listing_id = {listing_id}')[0].id
    if request.method == "POST":
        pass