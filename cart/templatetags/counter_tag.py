from django import template
from cart.models import  Order

register = template.Library()

@register.filter
def count_item(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].product.count()
    return 0
