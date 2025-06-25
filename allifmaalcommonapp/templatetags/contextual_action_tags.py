# myerpapp/templatetags/contextual_action_tags.py
# myerpapp/templatetags/contextual_action_tags.py

from django import template
from django.urls import reverse, NoReverseMatch
from django.db import models # <--- ADD THIS IMPORT LINE

from allifmaalcommonapp.models import CommonTransactionsModel # Ensure this is your app name

register = template.Library()

# ... rest of your code for render_contextual_actions function ...
from django import template
from django.urls import reverse, NoReverseMatch
from ..contextual_actions import SECTOR_CONTEXTUAL_ACTIONS
from allifmaalcommonapp.models import CommonTransactionsModel, CommonCompanyDetailsModel # <-- Also import CommonCompanyDetailsModel for the cmpnysctr type check
                                                                                       # And ensure allifmaalcommonapp is correctly configured in INSTALLED_APPS

register = template.Library()

@register.inclusion_tag('includes/sector_contextual_actions.html', takes_context=True)
def render_contextual_actions(context, allifquery, user_var, glblslug):
    # Get cmpnysctr. It might be a string from the context processor, or potentially a model instance.
    cmpnysctr_raw = context.get('cmpnysctr', 'Healthcare')
    
    # --- CRUCIAL FIX HERE: Convert cmpnysctr to its string representation ---
    if isinstance(cmpnysctr_raw, models.Model) and hasattr(cmpnysctr_raw, '__str__'):
        cmpnysctr_key = str(cmpnysctr_raw)
    else:
        cmpnysctr_key = cmpnysctr_raw # Assume it's already a string if not a model instance

    resolved_actions_map = {}

    print(f"\n--- CONTEXTUAL TAG DEBUG START ---")
    print(f"CONTEXTUAL TAG ---1: Raw cmpnysctr={cmpnysctr_raw!r} (type={type(cmpnysctr_raw)})")
    print(f"CONTEXTUAL TAG ---2: Key used for lookup (cmpnysctr_key)={cmpnysctr_key!r} (type={type(cmpnysctr_key)})") # Verify this
    print(f"CONTEXTUAL TAG ---3: allifquery_pk={allifquery.pk if allifquery else 'N/A'}")

    if not isinstance(allifquery, CommonTransactionsModel):
        print(f"CONTEXTUAL TAG: ERROR: allifquery is NOT a CommonTransactionsModel instance (it's {type(allifquery)}). Returning empty map.")
        print(f"--- CONTEXTUAL TAG DEBUG END ---\n")
        return {'contextual_actions_map': {}}

    # Get actions for the current sector using the string key
    actions_data = SECTOR_CONTEXTUAL_ACTIONS.get(cmpnysctr_key, []) # <-- USE cmpnysctr_key HERE
    print(f"CONTEXTUAL TAG: Actions data for {cmpnysctr_key!r}: {actions_data}") # Print the key being used


    for action_data in actions_data:
        action_name = action_data['name']
        current_url = "#error"
        
        try:
            if action_data.get('requires_pk', False):
                url = reverse(action_data['url_name'], args=[allifquery.pk, user_var, glblslug])
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
    return {'contextual_actions_map': resolved_actions_map}