# your_app_name/templatetags/navigation_tags.py

from django import template
from django.urls import reverse
from ..navigation_links import allifmaal_general_links, allifmaal_sector_specific_links

register = template.Library()

@register.inclusion_tag('includes/sector_navigation.html', takes_context=True)
def render_sector_navigation(context, user_var, glblslug):
    """
    Renders navigation links based on the company's sector.
    """
    cmpnysctr = context.get('cmpnysctr', 'Healthcare') # Get sector from context, default to 'General'

    # Start with general links
    allifmaal_custom_links = []
    for link in allifmaal_general_links:
        try:
            # Generate URL. If it needs user_var and glblslug:
            url = reverse(link['url_name'], args=[user_var, glblslug])
            allifmaal_custom_links.append({'name': link['name'], 'url': url})
        except Exception as e:
            pass
            # Handle URL resolution errors gracefully, e.g., log them
            #print(f"Warning: Could not resolve URL for general link '{link['name']}': {e}")
            # Optionally, skip this link or provide a fallback URL
            # nav_links.append({'name': link['name'], 'url': '#'})


    # Add sector-specific links
    sector_links_data = allifmaal_sector_specific_links.get(cmpnysctr, []) # Get links for the current sector, or empty list

    if not sector_links_data:
        # Fallback if no specific links for the sector, or use a 'Default' category
        sector_links_data =allifmaal_sector_specific_links.get('Default', [])
        if sector_links_data:
            pass
            #print(f"No specific links for sector '{cmpnysctr}', using default links.")
        else:
            pass
            #print(f"No specific links or default links found for sector '{cmpnysctr}'.")


    for link in sector_links_data:
        try:
            # Generate URL. Assuming sector-specific URLs also need user_var and glblslug:
            url = reverse(link['url_name'], args=[user_var, glblslug])
            allifmaal_custom_links.append({'name': link['name'], 'url': url})
        except Exception as e:
            pass
            #print(f"Warning: Could not resolve URL for sector '{cmpnysctr}' link '{link['name']}': {e}")
            # Optionally, skip this link or provide a fallback URL
            # nav_links.append({'name': link['name'], 'url': '#'})

    return {'allif_custom_links':allifmaal_custom_links}
