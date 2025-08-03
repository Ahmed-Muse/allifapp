# allifapperp/hosts.py
from django.conf import settings
from django_hosts import patterns, host

# This file maps hostnames to URL configurations.

# Define the patterns for your different subdomains.
# The patterns are evaluated in order, so the more specific patterns should come first.
host_patterns = patterns(
    '',
    # The default 'public' host. This will be used for your main domain
    # and its common aliases (www, localhost, etc.).
    # It points to the 'allifapperp.urls.public' URL configuration.
    host(r'|www|localhost|127|allifapp.com', 'allifapperp.urls.public', name='public'),
    
    # The 'company' host, which will handle any subdomain that is not the public host.
    # The `company_slug` is a regular expression capture group that will be passed
    # as an argument to the URLconf. It points to 'allifapperp.urls.company'.
    # This pattern is more explicit and reliable than a simple wildcard.
    host(r'(?P<company_slug>[\w-]+)', 'allifapperp.urls.company', name='company'),
    
    # Note: I have removed the redundant patterns for 'www' and the general 'wildcard'
    # as they were either duplicates of the 'public' or 'company' patterns.
)
