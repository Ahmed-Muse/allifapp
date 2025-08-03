
import threading
from django.apps import apps
from django.db import models # New import for exception handling
from django.urls import set_urlconf
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import CommonCompanyDetailsModel
# This middleware will check for subdomains and set the current company.
class CompanySubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Get the main domain from settings, e.g., 'allifapp.com'
        self.public_domain = settings.PUBLIC_DOMAIN

    def __call__(self, request):
        # Extract the host and remove the port if it exists (e.g., 'localhost:8000')
        host = request.get_host().split(':')[0].lower()
        
        # Check if the domain is a subdomain of the main public domain
        if host.endswith(f".{self.public_domain}"):
            # Get the slug from the subdomain part (e.g., 'muse-hospital' from 'muse-hospital.allifapp.com')
            subdomain_slug = host.split('.')[0]

            # Try to find the company with that slug
            try:
                company = get_object_or_404(CommonCompanyDetailsModel, slgfld=subdomain_slug)
                # Attach the company object to the request for easy access in views
                request.tenant_company = company
                
            except CommonCompanyDetailsModel.DoesNotExist:
                # If no company is found for the subdomain, return a 404.
                # You could also redirect to a public page or a custom error page here.
                # For this solution, we'll raise an error to indicate the subdomain is not registered.
                return self.get_response(request) # You can adjust this to a custom error page

        else:
            # This is the "normal" (non-tenant) part of your application.
            # We don't attach a company to the request.
            request.tenant_company = None

        response = self.get_response(request)
        return response
