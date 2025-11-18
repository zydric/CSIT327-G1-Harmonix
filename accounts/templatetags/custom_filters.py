from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Splits the value by the specified argument.
    If the value is None or empty, returns an empty list.
    """
    if not value:
        return []
    return [x.strip() for x in value.split(arg) if x.strip()]