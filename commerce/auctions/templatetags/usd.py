from django import template
from ..models import Bid

register = template.Library()

# Formating
@register.filter
def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

@register.filter
def current_listing_price(listing):
    try:
        max_price = Bid.objects.get(item_id = listing.id, max_bid = True)
        currentPrice = max_price.price
    except:
        currentPrice = listing.starting_bid

    return currentPrice