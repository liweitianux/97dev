# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter
def divisible_by(dividend, divisor):
    """
    if 'dividend' can be *exactly* divided by 'divisor',
    return True;
    else, return False.

    input parameters:
    dividend: <type 'int'>
    divisor: <class 'django.utils.safestring.SafeUnicode'>
    """
    if not isinstance(dividend, int):
        raise ValueError(u'Error: dividend="%s" not int type' % dividend)
    try:
        divisor = int(divisor)
    except ValueError, TypeError:
        raise ValueError(u'Error: divisor="%s" cannot convert to int'
                % divisor)
    #
    if dividend % divisor == 0:
        return True
    else:
        return False

