# your_app_name/templatetags/navigation_tags.py

from django import template
from django.urls import reverse, NoReverseMatch # Import NoReverseMatch for better error handling
# Ensure this import path is correct based on where your navigation_links.py is located
#from allifmaalcommonapp.configs.navigation_links import allifmaal_general_links, allifmaal_sector_specific_links 
import logging

logger = logging.getLogger(__name__)

from ..allif_navigation_links import allifmaal_general_links, allifmaal_sector_specific_links,allif_single_access_general_links
register = template.Library()

@register.inclusion_tag('allifmaalcommonapp/includes/allifapp_navigation_links.html', takes_context=True)
def allifapp_render_navigation_links(context, user_var, glblslug):
    """
    Renders navigation links based on the company's sector.
    """
    cmpnysctr = context.get('cmpnysctr', 'General') # Get sector from context, default to 'General'
    
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


@register.simple_tag(takes_context=True)
def allif_get_single_nav_link_url(context, link_name, user_var, glblslug):
    """
    Returns the URL for a single general navigation link by its 'name'.
    Returns '#' if the link is not found or URL cannot be resolved.
    
    Args:
        link_name (str): The 'name' key of the link dictionary to find.
        user_var (str): The username slug.
        glblslug (str): The global company slug.
    """
    for link in allif_single_access_general_links:
        if link.get('name') == link_name: # Use .get() for safer access...
            try:
                # Assuming this link needs user_var and glblslug
                return reverse(link['url_name'], args=[user_var, glblslug])
            except NoReverseMatch:
                logger.warning(f"Could not resolve URL for general link '{link_name}' (URL name: '{link.get('url_name', 'N/A')}'). Check URL patterns.")
                return "#" # Fallback URL
            except KeyError:
                logger.error(f"Link dictionary for '{link_name}' missing 'url_name' key.")
                return "#"
    
    logger.warning(f"General navigation link with name '{link_name}' not found in allif_single_access_general_links.")
    return "#" # Fallback if link name is not found
