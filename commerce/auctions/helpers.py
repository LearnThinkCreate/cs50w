from typing import ItemsView
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.core.exceptions import ValidationError
from django.forms.widgets import NumberInput
from django.utils.translation import gettext_lazy as _
from .models import Bid, Comment, Listing, User, Wishlist
from django.shortcuts import render

# Forms
class ListingForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=64,
        required=True,
        widget=forms.TextInput(attrs={
             'class':'form-control col-md-12'
        }))

    startingbid = forms.IntegerField(
        label="Starting Bid",
        required=True,
        widget=forms.TextInput(attrs={
            "class":"form-control"
        })
    )

    description = forms.CharField(
        label="Description",
        required=True,
        widget=forms.Textarea(attrs={
            "rows":"10",
            "cols":"10",
            "class":"form-control form-control-lg",
            "style":"top:2rem"
        })
    )

    image = forms.URLField(
        required=False,
        label="Image",
        widget=forms.URLInput(attrs={
            "class":"form-control",
            'placeholder':"URL"
        })
    )

    category = forms.CharField(
        label="Category",
        required=False,
        widget=forms.TextInput(attrs={
             "class":"form-control"
        }
        )
    )

class BidForm(forms.Form):
    bid = forms.DecimalField(
        max_digits=11,
        decimal_places=2,
        label="",
        localize=True,
        widget=forms.NumberInput(attrs={"placeholder":"Bid"})
    )

class CommentForm(forms.Form):
    comment = forms.CharField(
        label="comment",
        disabled=False,
        required=True,
        widget=forms.TextInput(attrs={
                "rows":"10", 
                "cols":"10",
                'class':"form-control form-control-lg",
                'style':"top:2rem; margin:5px"
        })
    )

class Page():
        def __init__(self, request) -> None:
            super().__init__()
            self.user = request.user
            self.request = request
            self.method = request.method

        def getUsername(self):
            return self.user.username



class ListingPage(Page):
    def __init__(self, request, listing_id) -> None:
        super().__init__(request)
        self. listing_id = listing_id

    def validWishlist(self):
        try:
            self.user.wishlist.get(listing_id = self.listing_id)
            return True
        except:
            return False

    def getListing(self):
        return Listing.objects.get(pk=self.listing_id)

    def currentPrice(self):
        if Bid.objects.filter(item_id = self.listing_id, max_bid = True):
            return Bid.objects.get(item_id = self.listing_id, max_bid = True).price
        return self.getListing.starting_bid

    def getWishlist(self):
        return Wishlist.objects.filter(listing_id=self.listing_id)

    def getArgs(self):
        return   {
        "listing":self.getListing,
        "currentPrice": self.currentPrice(),
        "bidForm":BidForm(),
        "wishlist":self.validWishlist()
    }
    def renderPage(self):
        return render(self.request, "auctions/viewListing.html", self.getArgs())