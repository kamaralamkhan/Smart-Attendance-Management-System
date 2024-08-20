# customfilters.py

from django import template

register = template.Library()

@register.filter(name='present_count')
def present_count(value):
    return value.filter(status='P').count()

@register.filter(name='present_percentage')
def present_percentage(value, arg):
    total_records = value.count()
    present_count = value.filter(status='P').count()
    absent_count = total_records - present_count

    if total_records > 0:
        percentage = (present_count / total_records) * 100
        return f"{percentage:.2f}{arg}"
    else:
        return "N/A"
