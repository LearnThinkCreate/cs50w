from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("viewListing/<int:listing_id>", views.viewListing, name="viewListing"),
    path("viewListing/<int:listing_id>/Close_Auction", views.closeAuction, name="closeAuction"),
    path("viewListing/<int:listing_id>/Bids", views.bid, name='bid'),
    path("viewListing/<int:listing_id>/addWishlist", views.addWishlist, name='addWishlist'),
    path("viewListing/<int:listing_id>/removeWishlist", views.removeWishlist, name='removeWishlist'),
    path("viewListing/<int:listing_id>/comment", views.comment, name='comment')
]
