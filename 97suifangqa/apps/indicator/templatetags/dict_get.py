# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter
def dict_get(dict, key):
    """
    filter to get the value of key in the dict:
    return dict[key]
    """
    return dict.get(key)

