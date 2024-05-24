from django import template

import math
register = template.Library()

@register.simple_tag
def discount_calculation(price, discount):
    if discount is None or discount is 0:
        return price
    sellprice = price
    # print(type(discount))
    # print(discount)
    sellprice = price - (price * discount/100)
    # print(sellprice)
    return math.floor(sellprice)
    # return sellprice