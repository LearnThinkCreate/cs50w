from django.contrib import admin
from .models import User, Listing

# Admin display Classes
class ListingAdmin(admin.ModelAdmin):
    list_display = ("owner", "title", "starting_bid")

# Register your models here.

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)