# myerpapp/templatetags/contextual_action_tags.py

from django import template
from django.urls import reverse, NoReverseMatch
from django.db import models # Needed for isinstance check
from ..contextual_actions import SECTOR_CONTEXTUAL_ACTIONS
from allifmaalcommonapp.models import CommonTransactionsModel # Ensure this is your app name

register = template.Library()

# Changed from @register.inclusion_tag to @register.simple_tag
# It now returns the dictionary directly to the calling template.
@register.simple_tag(takes_context=True)
def get_contextual_actions_map(context, allifquery, user_var, glblslug): # Renamed function for clarity
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

    print(f"\n--- CONTEXTUAL TAG DEBUG START ---")
    print(f"CONTEXTUAL TAG ---1: Raw cmpnysctr={cmpnysctr_raw!r} (type={type(cmpnysctr_raw)})")
    print(f"CONTEXTUAL TAG ---2: Key used for lookup (cmpnysctr_key)={cmpnysctr_key!r} (type={type(cmpnysctr_key)})")
    print(f"CONTEXTUAL TAG ---3: allifquery_pk={allifquery.pk if allifquery else 'N/A'}")

    if not isinstance(allifquery, CommonTransactionsModel):
        print(f"CONTEXTUAL TAG: ERROR: allifquery is NOT a CommonTransactionsModel instance (it's {type(allifquery)}). Returning empty map.")
        print(f"--- CONTEXTUAL TAG DEBUG END ---\n")
        return {} # Return an empty dict if the object is wrong

    transaction_pk = allifquery.pk # Ensure we have the PK

    actions_data = SECTOR_CONTEXTUAL_ACTIONS.get(cmpnysctr_key, [])
    print(f"CONTEXTUAL TAG: Actions data for {cmpnysctr_key!r}: {actions_data}")

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
            print(f"CONTEXTUAL TAG: Successfully resolved '{action_name}' to URL: {current_url}")

        except NoReverseMatch as e:
            print(f"DEBUG: NoReverseMatch for action '{action_name}' (URL: {action_data['url_name']}): {e}")
            resolved_actions_map[action_name] = {'name': action_name, 'url': '#url_error'}
        except Exception as e:
            print(f"DEBUG: Unexpected error resolving '{action_name}': {e}")
            resolved_actions_map[action_name] = {'name': action_name, 'url': '#general_error'}

    print(f"CONTEXTUAL TAG: Final resolved_actions_map keys: {list(resolved_actions_map.keys())}")
    print(f"--- CONTEXTUAL TAG DEBUG END ---\n")
    return resolved_actions_map # Return the dictionary directly