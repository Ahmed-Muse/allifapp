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



#_thread_locals = threading.local()

#def get_current_company():
    #"""
   # Retrieves the company ID (the primary key, an integer) from the 
    #thread-local storage.
    #"""
    #return getattr(_thread_locals, 'company', None)

#class AllifmaalTenantMiddleware:
    #"""
    #Middleware to set the current company ID on each request.
    #This now correctly handles a string-based link between the User and Company.
    #"""
    #def __init__(self, get_response):
        #self.get_response = get_response

    #def __call__(self, request):
        # The company ID is not yet set.
       # _thread_locals.company = None
        
        # We need the model, but we must import it lazily to avoid circular imports.
        # This is exactly what you had before, and it's still the correct approach.
        #try:
            #CommonCompanyDetailsModel = apps.get_model('allifmaalcommonapp', 'CommonCompanyDetailsModel')
        #except LookupError:
           # CommonCompanyDetailsModel = None

        #if request.user.is_authenticated and CommonCompanyDetailsModel:
            # We now get the company SLUG from the user, not the company object.
            #company_slug = request.user.usercompany
            
            # Use the slug to find the company's primary key (id).
            #if company_slug:
                #try:
                   # company = CommonCompanyDetailsModel.all_objects.get(slgfld=company_slug)
                    # The company object is found, so we set the thread-local variable
                    # with its primary key (id).
                    #_thread_locals.company = company.id
                #xcept (CommonCompanyDetailsModel.DoesNotExist, models.ObjectDoesNotExist):
                    # This handles cases where the slug exists on the user but
                    # there's no corresponding company in the database.
                    #print(f"Warning: User {request.user.email} has company slug '{company_slug}' but no matching company was found.")
                    #pass
            # If `request.user.usercompany` is an empty string or None, the
            # `if company_slug:` block is skipped, and the thread-local remains None.
        
        #response = self.get_response(request)
        #_thread_locals.company = None

        #return response
