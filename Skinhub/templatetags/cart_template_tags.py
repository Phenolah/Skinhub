from ..models import Order
from django import template

register = template.Library()

@register.filter
def get_cart_count(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(customer=request.user, ordered=False)
        if order.exists():
            order_items = order[0].items.all()
            count = sum([item.number_of_Products for item in order_items])
            return count
        else:
            count = 0
    else:
        count = 0
    return count





