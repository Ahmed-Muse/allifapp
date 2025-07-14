# allifmaalcommonapp/templatetags/form_filters.py
from django import template

register = template.Library()

@register.filter
def get_form_field(form, field_name):
    """Returns a form field by its name."""
    # This handles both Django Form objects and potentially dicts if you pass a dict
    return form.get(field_name) if isinstance(form, dict) else form[field_name]