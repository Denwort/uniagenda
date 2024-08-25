from django import template
from datetime import datetime

register = template.Library()

@register.filter
def get_height(start_time, end_time):
    duration = end_time - start_time
    minutes = duration.total_seconds() / 60
    return minutes
