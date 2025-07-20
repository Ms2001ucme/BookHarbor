from django import template

register = template.Library()

@register.filter
def average(queryset, field):
    """
    Calculate the average of a specific field in a queryset.
    Usage: {{ reviews|average:'rating' }}
    """
    values = [getattr(obj, field) for obj in queryset if getattr(obj, field, None) is not None]
    return sum(values) / len(values) if values else 0
