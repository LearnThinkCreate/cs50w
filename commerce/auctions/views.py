from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Wishlist, Comment
from .helpers import *

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
    page = ListingPage(request, listing_id)
    return page.renderPage()

@login_required
def bid(request, listing_id):
    page = ListingPage(request, listing_id)
    if page.method == "POST": 
        form = BidForm(page.request.POST)
        if form.is_valid():
            buyer = page.user
            # Getting the curent price of the Item
            old_bid = Bid.objects.get(item_id = page.listing_id, max_bid = True)
            old_bid.max_bid = False
            old_bid.save()
            
            bid_price = form.cleaned_data["bid"]
            
            if bid_price <= page.currentPrice():
                return page.renderPage(request)

            # Adding a new bid 
            new_bid = Bid(item=page.getListing(), price=bid_price, max_bid=True)
            # Saving the bid
            new_bid.save()
            # Adding a buyer
            buyer.bids.add(new_bid)
    
            # Returning the user back to View the item
            return HttpResponseRedirect(reverse('index'))

        # The form was not valid
        return page.renderPage()

@login_required
def comment(request, listing_id):
    page = ListingPage(request, listing_id)
    if page.method == "POST":
        form=CommentForm(page.request.POST)
        if form.is_valid():
            newComment = Comment(
                listing = page.getListing(),
                comment = form.cleaned_data["comment"]
            )

            newComment.save()
            newComment.user.add(page.user)
            newComment.save()

            return page.renderPage()

        # Form is invalid
        return page.renderPage()
        
@login_required
def closeAuction(request, listing_id):
    page = ListingPage(request, listing_id)
    if page.method== "POST":
        listing = page.getListing()
        listing.active = False
        listing.save()

        return HttpResponseRedirect(reverse('index'))


@login_required
def addWishlist(request, listing_id):
    page = ListingPage(request, listing_id)
    if page.method == "POST":
        wishlist = page.getWishlist()
        wishlist.user.add(page.user)
        wishlist.save()
        return page.renderPage()

@login_required
def removeWishlist(request, listing_id):
    page = ListingPage(request, listing_id)
    if page.method == "POST":
        wishlist = page.getWishlist()
        wishlist.delete(page.user)
        wishlist.save
        return page.renderPage()