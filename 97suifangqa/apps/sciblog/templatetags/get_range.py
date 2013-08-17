from django import template

register = template.Library()
@register.filter
def get_range(count, start = 0):
	return range(start, start + count)

