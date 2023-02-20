from django import template
from .cart_template_tags import get_cart_count

register = template.Library()
register.tag('cart_item_count', get_cart_count)