from django import template
from ..views import generate_link

register = template.Library()

@register.filter
def generate_link(link):
    return generate_link(link)