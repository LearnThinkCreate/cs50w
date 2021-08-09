from django import db
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    # User Data
    owner = models.ForeignKey(
        # Passing in the User Model
        User,
        on_delete=models.CASCADE,
        # Related Name that can be used by User object
        related_name="listings",
        db_index=True
    )

    # Metadata
    active = models.BooleanField(db_index=True)

    # Mandatory user input
    title = models.CharField(max_length=64, blank=False, db_index=True)
    description = models.TextField(blank=False)
    starting_bid = models.IntegerField(blank=False, db_index=True)
    # Optional user input
    image = models.URLField(blank=True)
    category = models.TextField(blank=True)


class Bid(models.Model):
    # What's being bid - Many bids can be on one item 
    item = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        # Name for reference in the listing table
        related_name="bids",
        # Field that's indexed
        db_index=True
    )
    # The price of that bid
    price = models.DecimalField(
        blank=False,
        decimal_places=2,
        max_digits=11)
    # The user who made that bid
    bidder = models.ManyToManyField(
        # Table that this field is related to
        User,
        blank=True,
        # Related name in the User table
        related_name="bids"
    )
    # Distinguishes if this bid is the highest bid
    max_bid = models.BooleanField(blank=True, db_index=True)

class Comment(models.Model):
    pass
