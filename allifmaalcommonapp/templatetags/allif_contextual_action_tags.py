# myerpapp/templatetags/contextual_action_tags.py

from django import template
from django.urls import reverse, NoReverseMatch
from django.db import models # Needed for isinstance check
from ..allif_contextual_action_links import allif_sector_contextual_action_require_pk_links

register = template.Library()
@register.simple_tag(takes_context=True)
def allif_get_contextual_actions_map(context, allifquery, user_var, glblslug): # Renamed function for clarity
    """
    Prepares and returns a dictionary (map) of contextual action links
    for a specific CommonTransactionsModel instance, based on the company's sector.
    This tag does NOT render HTML; it only provides data.
    """
    cmpnysctr_raw = context.get('cmpnysctr', 'General')
    
    if isinstance(cmpnysctr_raw, models.Model) and hasattr(cmpnysctr_raw, '__str__'):
        cmpnysctr_key = str(cmpnysctr_raw)
    else:
        cmpnysctr_key = cmpnysctr_raw

    resolved_actions_map = {}
    transaction_pk = allifquery.pk # Ensure we have the PK
    actions_data = allif_sector_contextual_action_require_pk_links.get(cmpnysctr_key, [])
    for action_data in actions_data:
        action_name = action_data['name']
        current_url = "#error"
        
        try:
            if action_data.get('requires_pk', False):
                url = reverse(action_data['url_name'], args=[transaction_pk, user_var, glblslug])
                current_url = url
            else:
                url = reverse(action_data['url_name'], args=[user_var, glblslug])
                current_url = url

            resolved_actions_map[action_name] = {'name': action_name, 'url': current_url}
           
        except NoReverseMatch as e:
            print(f"DEBUG: NoReverseMatch for action '{action_name}' (URL: {action_data['url_name']}): {e}")
            resolved_actions_map[action_name] = {'name': action_name, 'url': '#url_error'}
        except Exception as e:
            resolved_actions_map[action_name] = {'name': action_name, 'url': '#general_error'}
    return resolved_actions_map # Return the dictionary directly