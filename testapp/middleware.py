from django.conf import settings
from .models import set_current_company, Company

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        company = None
        # Example: Get company from a session variable after login/selection
        company_id = request.session.get('active_company_id')
        if company_id:
            try:
                company = Company.all_objects.get(id=company_id, is_active=True)
            except Company.DoesNotExist:
                pass
        
        # You might also get the company from a URL slug or subdomain for public-facing parts
        # For this ERP, session/user-based selection is more common.

        set_current_company(company) # Set for CompanyScopedManager
        request.company = company    # Attach to request for direct access in views

        response = self.get_response(request)
        set_current_company(None) # Clean up
        return response

# In your_project_name/settings.py:
# MIDDLEWARE = [
#     ...
#     'apps.core.middleware.TenantMiddleware',
#     ...
# ]