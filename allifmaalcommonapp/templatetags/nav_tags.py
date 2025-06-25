# myerpapp/templatetags/navigation_tags.py

from django import template
from django.urls import reverse
from ..navigation_links import allifmaal_general_links,allifmaal_sector_specific_links

register = template.Library()

@register.inclusion_tag('includes/sector_navigation.html', takes_context=True)
def render_sector_navigation_two(context, user_var, glblslug):
    """
    Renders navigation links, providing them as dictionaries for individual access.
    """
    cmpnysctr = context.get('cmpnysctr', 'Healthcare')

    # Dictionaries to hold the resolved links, accessible by their 'name'
    general_links_map = {}
    sector_links_map = {}

    # --- 1. Resolve General Links and store in a map ---
    for link_data in allifmaal_general_links:
        try:
            url = reverse(link_data['url_name'], args=[user_var, glblslug])
            # Use link['name'] as the key for direct access in template
            general_links_map[link_data['name']] = {'name': link_data['name'], 'url': url}
        except Exception as e:
            #print(f"DEBUG: Could not resolve URL for general link '{link_data['name']}': {e}")
            # Optionally, add a placeholder or skip:
            general_links_map[link_data['name']] = {'name': link_data['name'], 'url': '#error_url'}

    # --- 2. Resolve Sector-Specific Links and store in a map ---
    sector_specific_data = allifmaal_sector_specific_links.get(cmpnysctr, [])

    if not sector_specific_data:
        pass
        #print(f"DEBUG: No specific links found for sector '{cmpnysctr}'.")

    for link_data in sector_specific_data:
        try:
            url = reverse(link_data['url_name'], args=[user_var, glblslug])
            # Use link['name'] as the key for direct access in template
            sector_links_map[link_data['name']] = {'name': link_data['name'], 'url': url}
        except Exception as e:
            #print(f"DEBUG: Could not resolve URL for sector-specific link '{link_data['name']}' in '{cmpnysctr}': {e}")
            # Optionally, add a placeholder or skip:
            sector_links_map[link_data['name']] = {'name': link_data['name'], 'url': '#error_url'}

    # Return the two separate dictionaries to the template
    return {
        'general_links_map': general_links_map,
        'sector_links_map': sector_links_map
    }