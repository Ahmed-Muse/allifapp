from django.shortcuts import render,redirect,HttpResponse
from .allifutils import common_shared_data
from django.contrib.auth.decorators import login_required
from .models import CommonCompanyDetailsModel,CommonApproversModel
from allifmaalusersapp.models import User

from functools import wraps

from django.http import HttpRequest # For type hinting
def allifmaal_admin_supperuser(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        if usernme.is_superuser==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func


def allifmaal_admin(allif_param_func):
    @wraps(allif_param_func)
    def allif_wrapper_func(request, *args, **kwargs):
        result = allif_check_user_attribute_permission(request, 'allifmaal_admin', True, "attribute")
        if result is not None: return result
        return allif_param_func(request,*args,**kwargs)
    return allif_wrapper_func




#########################################################################################3
def unauthenticated_user(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        user_var=request.user.company
        usrslg=request.user.customurlslug
        usr=request.user
        if usr.user_category=="admin":
           
            return redirect('allifmaalcommonapp:commonhrm',allifusr=usrslg,allifslug=user_var)
        elif usr.user_category=="director":
            pass
            
        else:
            return allif_param_func(request,*args,**kwargs)
    return allif_wrapper_func
def allowed_users(allowed_roles=[]):
    def user_delete_permissions(allif_param_func):
        def allif_wrapper_func(request,*args,**kwargs):
            user_var=request.user.company
            usrslg=request.user.customurlslug
            usr=request.user
            print(f"working {allowed_roles}")
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                pass
            else:
                return allif_param_func(request,*args,**kwargs)
        
        return allif_wrapper_func
    return user_delete_permissions
def unrestrictedCRUD(allowed_roles=[]):
    def user_delete_permissions(allif_param_func):
        def allif_wrapper_func(request,*args,**kwargs):
            user_var=request.user.company
            usrslg=request.user.customurlslug
            usr=request.user
            print(f"working {allowed_roles}")
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                pass
            else:
                return allif_param_func(request,*args,**kwargs)
        
        return allif_wrapper_func
    return user_delete_permissions

############ handling view function try block section....
# C:\am\allifapp\allifapperp\allifmaalcommonapp\decorators.py


def allif_view_exception_handler(view_function):
    """
    A decorator to catch exceptions in view functions and render a generic error page.
    
    @wraps(view_function): This is important from the functools module. It preserves the original
    view function's metadata (like its name, docstrings), which is useful for debugging and introspection
    (e.g., request.resolver_match.view_name).

    _wrapped_view(request, *args, **kwargs): This is the inner function that will actually replace your
    original view. It takes the same arguments as a Django view.

    try...except block: This is where the magic happens. It attempts to execute your view_function.
    If any Exception occurs, it catches it, prints an error to the console, prepares the error_context,
    and renders your generic error page.
    """
    @wraps(view_function)
    def _wrapped_view(request: HttpRequest, *args, **kwargs):
        try:
            return view_function(request, *args, **kwargs)
        except Exception as ex:
            print(f"ERROR: Exception caught in view '{view_function.__name__}': {ex}")
            error_context = {
                'error_message': str(ex), # Convert exception to string for display
                'title': "An Error Occurred", # Generic title for error page
                # You might want to pass more context here if needed for debugging/user feedback
                # 'view_name': view_function.__name__, 
            }
            # Ensure the path to your error template is correct
            return render(request, 'allifmaalcommonapp/error/error.html', error_context)
    return _wrapped_view







# C:\am\allifapp\allifapperp\allifmaalcommonapp\decorators.py

# --- Helper for common permission check logic ---
def allif_check_user_attribute_permission(request: HttpRequest, attribute_name: str, expected_value=True, permission_type: str = "attribute"):
    """
    Helper function for decorators that check a boolean attribute or category on request.user.
    """
    if not request.user.is_authenticated:
        return redirect('allifmaalusersapp:userLoginPage') # Redirect to login if not authenticated

    usernme = request.user
    has_permission = False

    if permission_type == "attribute":
        has_permission = getattr(usernme, attribute_name, False) == expected_value
    elif permission_type == "category":
        has_permission = getattr(usernme, 'user_category', None) == expected_value
    elif permission_type == "group":
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name # Assuming one primary group
        has_permission = group == expected_value
    elif permission_type == "in_roles": # For allowed_users/unrestrictedCRUD
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        has_permission = group in expected_value # expected_value is a list of roles
    else:
        print(f"WARNING: Unknown permission_type: {permission_type}")
        return render(request, 'allifmaalcommonapp/permissions/no_permission.html')

    if has_permission:
        return None # Indicate success, wrapped function can proceed
    else:
        return render(request, 'allifmaalcommonapp/permissions/no_permission.html') # Render no permission page

# --- Core/Universal Decorators ---


def logged_in_user_must_have_profile(func):
    """
    Decorator to ensure the logged-in user is authenticated and has a profile.
    """
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('allifmaalusersapp:userLoginPage')

        allif_data = common_shared_data(request) # Get data for profile check
        if allif_data.get("logged_in_user_profile"): # Assuming this key exists in common_shared_data
            return func(request, *args, **kwargs)
        else:
            context={"allifquery":request.user,} # Pass user for template if needed
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
    return wrapper

def subscriber_company_status(func):
    """
    Decorator to check the status of the subscriber company.
    """
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('allifmaalusersapp:userLoginPage')

        try:
            allif_data = common_shared_data(request)
            compslg = request.user.company # Assuming usercompany is a slug
            #main_sbscrbr_entity = CommonCompanyDetailsModel.all_objects.filter(slgfld=compslg).first()
            main_sbscrbr_entity =CommonCompanyDetailsModel.all_objects.filter(company=request.user.company).first()

            if main_sbscrbr_entity is None:
                return redirect('allifmaalusersapp:userLogoutPage') # Company not found, force logout
            else:
                subs_status = main_sbscrbr_entity.status
                if subs_status == "Unblocked": # Assuming 'Unblocked' is the active status
                    return func(request, *args, **kwargs)
                else:
                    context={"allifquery":request.user,}
                    return render(request,'allifmaalcommonapp/permissions/entity_blocked.html',context)
        except Exception as ex:
            print(f"ERROR: subscriber_company_status decorator failed: {ex}")
            error_context={'error_message': str(ex), 'title': "Company Status Error"}
            return render(request,'allifmaalcommonapp/error/error.html',error_context)
    return wrapper

# --- Generalized Permission Decorators ---

def allifmaal_admin_superuser(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result = allif_check_user_attribute_permission(request, 'is_superuser', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_can_do_all(func): # Renamed for clarity
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result = allif_check_user_attribute_permission(request, 'can_do_all', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_can_add(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'can_add', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_can_view(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Removed global ahmed, it's not good practice in decorators
        result =allif_check_user_attribute_permission(request, 'can_view', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_can_edit(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'can_edit', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_can_delete(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'can_delete', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_is_admin(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'admin', "category") # Assuming 'admin' is the category string
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_is_owner_ceo(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        usernme = request.user
        if not usernme.is_authenticated:
            return redirect('allifmaalusersapp:userLoginPage')
        
        if usernme.user_category == "owner" or usernme.user_category == "ceo":
            return func(request, *args, **kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return wrapper

def logged_in_user_is_staff(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'staff', "category")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_is_director(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'director', "category")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_is_general_manager(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'genmanager', "category")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

# --- Access Level Decorators (can also use _check_user_attribute_permission) ---
def logged_in_user_has_universal_delete(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'universal_delete', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_has_divisional_delete(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'divisional_delete', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_has_branches_delete(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'branches_delete', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_has_departmental_delete(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'departmental_delete', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_has_universal_access(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'universal_access', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_has_divisional_access(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'divisional_access', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_has_branches_access(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result =allif_check_user_attribute_permission(request, 'branches_access', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_has_departmental_access(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result = allif_check_user_attribute_permission(request, 'departmental_access', True, "attribute")
        if result is not None: return result
        return func(request, *args, **kwargs)
    return wrapper

def logged_in_user_can_approve(func):
    """
    Checks if the user is authenticated and belongs to an approver group/model.
    """
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('allifmaalusersapp:userLoginPage')
        
        allif_data = common_shared_data(request)
        # Assuming 'logged_in_user_profile' is the profile instance
        if allif_data.get("logged_in_user_profile") and \
           CommonApproversModel.all_objects.filter(approvers=allif_data.get("logged_in_user_profile")).exists():
            return func(request, *args, **kwargs)
        else:
            return render(request, 'allifmaalcommonapp/permissions/no_permission.html')
    return wrapper



# --- Base Combined Decorator (for universal checks) ---
def allif_base_view_wrapper(allif_param_func):
    """
    Combines universal view decorators that apply to almost all views.
    Order of application (outermost first, innermost last):
    1. handle_view_exception (catches all errors)
    2. subscriber_company_status (checks company status)
    3. logged_in_user_must_have_profile (ensures user is authenticated and has a profile)
    """
    # Apply decorators from innermost to outermost
    allif_wrapper_func = allif_view_exception_handler(
                        subscriber_company_status(
                            logged_in_user_must_have_profile(allif_param_func)
                        )
                   )
    return allif_wrapper_func
