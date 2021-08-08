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
        # Related Name
        related_name="user"
    )
    # Mandatory 
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=False)
    starting_bid = models.IntegerField(blank=False)
    # Optional
    image = models.URLField(blank=True)
    category = models.TextField(blank=True)


class Bid(models.Model):
    pass

class Comment(models.Model):
    pass
