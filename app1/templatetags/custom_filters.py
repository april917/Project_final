# app1/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    # Ensure 'value' is a form field
    if hasattr(value, 'as_widget'):
        return value.as_widget(attrs={'class': css_class})
    # If not, return the value unchanged (to avoid errors with strings)
    return value
