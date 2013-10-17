from django import template

register = template.Library()

@register.filter(name='total')
def total(list):
    """
    Template tag that count total price for
    the list of given seats.
    """
    return sum([seat.price_category.price for seat in list])

