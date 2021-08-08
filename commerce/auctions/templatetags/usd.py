from django import template

register = template.Library()

# Formating
@register.filter
def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"