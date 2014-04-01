import os

from django import template
register = template.Library()

@register.filter
def filename(value):
    if value.value() is None:
        return ''
    value[0].value = 'poo'
    return value
    


# EOF