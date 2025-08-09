# allifmaalcommonapp/middleware.py

import threading
from django.apps import apps
from django.db import models # New import for exception handling

# allifmaalcommonapp/middleware.py

import threading

_thread_locals = threading.local()

def get_current_company():
    """
    Retrieves the company ID (the primary key, an integer) from the 
    thread-local storage. This is called by your custom manager.
    """
    return getattr(_thread_locals, 'company', None)

class AllifmaalTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # The company ID is not yet set.
        _thread_locals.company = None
        
        if request.user.is_authenticated:
            try:
                # This is the new, simple, and direct way to get the ID
                # It works because `request.user.company` is now a ForeignKey object
                _thread_locals.company = request.user.company.id
            except AttributeError:
                # This handles the case where the user is logged in but has no
                # company assigned yet. The thread-local will remain None.
                pass
        
        response = self.get_response(request)
        _thread_locals.company = None

        return response