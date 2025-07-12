# C:\am\allifapp\allifapperp\allifmaalcommonapp\utils.py

# C:\am\allifapp\allifapperp\allifmaalcommonapp\utils.py
from django import forms # Import forms for type hinting if needed
from django.db.models import QuerySet # Import QuerySet for type hinting

from django.db.models import QuerySet, Model # Import Model
from django.http import HttpRequest

from typing import Optional # Import Optional for type hinting
from .models import *
from allifmaalshaafiapp.models import *
from django.db.models import QuerySet, Model, Q # Ensure Q is imported for complex lookups

from django.shortcuts import render,redirect,get_object_or_404
from .allifutils import common_shared_data
from django.urls import reverse
from django.http import Http404

from .models import CommonPurchaseOrdersModel, CommonPurchaseOrderItemsModel

# Define sort mappings and default sort fields for different models here.
# Use a clear identifier (e.g., model name in lowercase) as the key.
MODEL_SORT_CONFIGS = {
    'commonexpensesmodel': { # Key should be consistent, e.g., model._meta.model_name
        'sort_mapping': {
            "Name Ascending": "name",
            "Name Descending": "-name",
            "Quantity Ascending": "quantity",
            "Quantity Descending": "-quantity",
            "Amount Ascending": "amount",
            "Amount Descending": "-amount",
            "Created At Ascending": "date",
            "Created At Descending": "-date",
            "Status Ascending": "status",
            "Status Descending": "-status",
            "Supplier Name Ascending": "supplier__name", 
            "Supplier Name Descending": "-supplier__name",
        },
        'default_sort_field': '-date',
        'default_ui_label': 'Created At Descending', # A default label for initial load
    },
    
    'commoncurrenciesmodel': { # Key should be consistent, e.g., model._meta.model_name
        'sort_mapping': {
            "Name Ascending": "name",
            "Name Descending": "-name",
            "Description Ascending": "description",
            "Description Descending": "-description",
           
        },
        'default_sort_field': '-date',
        'default_ui_label': 'Created At Descending', # A default label for initial load
    },
    
    'commontasksmodel': {
        'sort_mapping': {
            "Task Name Ascending": "name",
            "Task Name Descending": "-name",
            "Date Ascending": "date",
            "Date Descending": "-date",
            "Priority Ascending": "priority",
            "Priority Descending": "-priority",
            "Status Ascending": "status",
            "Status Descending": "-status",
            "Created At Ascending": "date",
            "Created At Descending": "-date",
        },
        'default_sort_field': '-date',
        'default_ui_label': 'Date Descending',
    },
    'triagesmodel': { # Assuming TriagesModel exists and is named this way
        'sort_mapping': {
            "Medical File Ascending": "medical_file",
            "Medical File Descending": "-medical_file",
            "Created At Ascending": "date",
            "Created At Descending": "-date",
            "Pain Level Ascending": "pain_level",
            "Pain Level Descending": "-pain_level",
            "Weight Ascending": "weight",
            "Weight Descending": "-weight",
            "Height Ascending": "height",
            "Height Descending": "-height",
            
             "Temperature Ascending": "temperature",
            "Temperature Descending": "-temperature",
        },
        'default_sort_field': '-date',
        'default_ui_label': 'Created At Descending',
    }
    # Add other model sort configurations here
}

allif_delete_models_class_map= {
    'CommonSectorsModel': CommonSectorsModel,
    'CommonCompanyScopeModel': CommonCompanyScopeModel,
    'CommonTaxParametersModel': CommonTaxParametersModel,
    'CommonExpensesModel': CommonExpensesModel,
    'CommonTasksModel': CommonTasksModel,
    'CommonBanksModel': CommonBanksModel,
    'TriagesModel': TriagesModel, 
    'CommonCurrenciesModel': CommonCurrenciesModel, 
    'CommonSupplierPaymentsModel': CommonSupplierPaymentsModel,
    'CommonCustomerPaymentsModel': CommonCustomerPaymentsModel,
    'CommonPaymentTermsModel': CommonPaymentTermsModel,
}

def allif_filtered_and_sorted_queryset(request: HttpRequest,model_class: type[Model], allif_data: dict,explicit_scope: Optional[str] = None) -> QuerySet:
    """
    Applies common filtering (company, scope, access levels) and sorting to a queryset.
    Retrieves sort_mapping and default_sort_field from MODEL_SORT_CONFIGS.

    Args:
        request (HttpRequest): The HttpRequest object.
        model_class (type[models.Model]): The Django Model class to query (e.g., CommonExpensesModel).
        allif_data (dict): Dictionary containing user access levels and company ID.
        explicit_scope (Optional[str]): If provided ('active', 'all', 'archived'),
                                        this will override the 'scope' from request.GET.

    Returns:
        QuerySet: The filtered and sorted QuerySet.
    """
    company_id = allif_data.get("main_sbscrbr_entity")

    model_identifier = model_class._meta.model_name 
    sort_config = MODEL_SORT_CONFIGS.get(model_identifier, {})
    sort_mapping = sort_config.get('sort_mapping', {})
    default_sort_field = sort_config.get('default_sort_field', '-starts')
    default_ui_label = sort_config.get('default_ui_label', 'Default Sort')

    """
    do the data filtering here based on the company and other parameters like divisions, branches departments etc.
    """
    # --- Determine the effective scope ---
    # Prioritize explicit_scope, then request.GET.get('scope'), then default to 'active'
    scope = explicit_scope if explicit_scope is not None else request.GET.get('archived', 'active') 
    # above... if explicit_scope is specified, then use it, else, show all both active and archived data
    
    # Initialize queryset based on scope
    if scope == 'all' and hasattr(model_class, 'all_objects'):
        queryset = model_class.all_objects.all()
    elif scope == 'archived' and hasattr(model_class.objects, 'archived'):
        queryset = model_class.objects.archived()
    else: # Default to 'active' or standard manager
        queryset = model_class.objects.all() 

    # --- Apply company filter ---
    if hasattr(model_class, 'company') and company_id:
        queryset = queryset.filter(company=company_id)
    else:
        pass 
    
    # --- Apply access level filtering (division, branch, department) ---
    if allif_data.get("logged_in_user_has_universal_access"):
        pass 
    elif allif_data.get("logged_in_user_has_divisional_access"):
        if hasattr(model_class, 'division'):
            queryset = queryset.filter(division=allif_data.get("logged_user_division"))
        else:
            queryset = model_class.objects.none()
    elif allif_data.get("logged_in_user_has_branches_access"):
        if hasattr(model_class, 'division') and hasattr(model_class, 'branch'):
            queryset = queryset.filter(
                division=allif_data.get("logged_user_division"),
                branch=allif_data.get("logged_user_branch")
            )
        else:
            queryset = model_class.objects.none()
    elif allif_data.get("logged_in_user_has_departmental_access"):
        if hasattr(model_class, 'division') and hasattr(model_class, 'branch') and hasattr(model_class, 'department'):
            queryset = queryset.filter(
                division=allif_data.get("logged_user_division"),
                branch=allif_data.get("logged_user_branch"),
                department=allif_data.get("logged_user_department")
            )
        else:
            queryset = model_class.objects.none()
    else:
        queryset = model_class.objects.none()

    # --- Determine and apply sorting based on POST data (from your form) ---
    selected_ui_label = request.POST.get('sort_option') 
    
    if not selected_ui_label: 
        selected_ui_label = request.GET.get('sort_ui_label')

    sort_field = sort_mapping.get(selected_ui_label, default_sort_field)
    
    if not selected_ui_label or selected_ui_label not in sort_mapping:
        selected_ui_label = default_ui_label

    queryset = queryset.order_by(sort_field)

    queryset.current_sort_ui_label = selected_ui_label
    queryset.sort_options = sort_mapping.items() 
    queryset.current_scope = scope # This will reflect the *actual* scope used (explicit or from GET)

    return queryset



# --- NEW UTILITY FUNCTION FOR FORM QUERYSET INITIALIZATION ---
def allif_initialize_form_select_querysets(form_instance: forms.Form, allifmaalparameter: str, field_model_map: dict):
    """
    Initializes querysets for Select/ModelChoiceFields in a form based on a parameter.
    ...Explanation of allif_initialize_form_select_querysets:

    form_instance: The actual form object being initialized (self from your __init__ method).

    allifmaalparameter: Your allifmaalparameter (likely the company ID).

    field_model_map: This is the key. It's a dictionary that tells the function which form field corresponds to which Django Model.

    Example: {'items': CommonStocksModel, 'trans_number': CommonTransactionsModel}

    Logic:

    If allifmaalparameter exists, it iterates through the field_model_map and sets the queryset for each field to Model.objects.filter(company=allifmaalparameter).

    If allifmaalparameter does not exist, it sets the queryset for each field to Model.objects.none().

    It includes checks (if field_name in form_instance.fields and isinstance(...)) to make it more robust, ensuring it only tries to set querysets on valid ModelChoiceFields that actually exist in the form.

    Args:
        form_instance (forms.Form): The instance of the Django form.
        allifmaalparameter (str): The parameter (e.g., company ID) to filter by.
        field_model_map (dict): A dictionary where keys are field names (strings)
                                and values are the Django Model classes (e.g., CommonStocksModel).
                                Example: {'items': CommonStocksModel, 'trans_number': CommonTransactionsModel}
    """
    if allifmaalparameter:
        for field_name, model_class in field_model_map.items():
            if field_name in form_instance.fields:
                # Check if the field is indeed a ModelChoiceField or similar
                if isinstance(form_instance.fields[field_name], (forms.ModelChoiceField, forms.ModelMultipleChoiceField)):
                    form_instance.fields[field_name].queryset = model_class.objects.filter(company=allifmaalparameter)
                else:
                    print(f"WARNING: Field '{field_name}' in form is not a ModelChoiceField/ModelMultipleChoiceField. Skipping queryset initialization.")
            else:
                print(f"WARNING: Field '{field_name}' not found in form fields. Skipping queryset initialization.")
    else:
        for field_name, model_class in field_model_map.items():
            if field_name in form_instance.fields:
                if isinstance(form_instance.fields[field_name], (forms.ModelChoiceField, forms.ModelMultipleChoiceField)):
                    form_instance.fields[field_name].queryset = model_class.objects.none()
            # No need for else here, if field not in form_instance.fields, it's already skipped


# --- NEW: Generic Form Submission and Save Logic Function ---
#@logged_in_user_must_have_profile
#@logged_in_user_can_view
def allif_common_form_submission_and_save(request,form_class: type[forms.ModelForm],title_text: str, 
    success_redirect_url_name: str, # for the redirection url
    template_path: str,# function specific template
    
    # New optional parameter for custom pre-save logic
    pre_save_callback: Optional[callable] = None, # argument. This callback will be a function that
    # the calling view provides to perform any model-specific assignments before the object is saved.
    
    
    # New optional parameter for initial data (for GET request forms)
    initial_data: Optional[dict] = None,
    # New optional parameter for extra form arguments (for form __init__)
    extra_form_args: Optional[list] = None
    ):
    
    """
    Helper function to encapsulate the common logic for processing form submissions
    and saving new items, including custom pre-save assignments.

    Args:
        request (HttpRequest): The HttpRequest object.
        form_class (type[forms.ModelForm]): The specific ModelForm class to use.
        title_text (str): The title for the page.
        success_redirect_url_name (str): The Django URL name to redirect to on successful form submission.
        template_path (str): The path to the template to render.
        pre_save_callback (callable, optional): A function (obj, request, allif_data) -> None
                                                that performs model-specific assignments before obj.save().
        initial_data (dict, optional): Initial data for the form on GET request.
        extra_form_args (list, optional): Additional positional arguments to pass to form_class.__init__.
    """
    allif_data = common_shared_data(request)
    company_id = allif_data.get("main_sbscrbr_entity").id

    # Prepare form arguments for __init__
    form_args = [company_id] # Default first argument for your forms
    if extra_form_args:
        form_args.extend(extra_form_args)

    if request.method == 'POST':
        form = form_class(*form_args, request.POST) 
        if form.is_valid():
            obj = form.save(commit=False)
            
            # --- Assign common fields from allif_data (fetching FK instances) ---
            # These fields are expected to be on CommonBaseModel and inherited by 'obj'
            
            # Company
            if hasattr(obj, 'company') and company_id:
                try:
                    obj.company = get_object_or_404(CommonCompanyDetailsModel, pk=company_id)
                except Http404: # More specific exception for get_object_or_404
                    print(f"WARNING: Company with ID {company_id} not found for {obj.__class__.__name__}.")
                    obj.company = None 
                except Exception as e:
                    print(f"ERROR: Failed to retrieve company with ID {company_id}: {e}")
                    obj.company = None
            else:
                pass
            # Division
            if hasattr(obj, 'division') and allif_data.get("logged_user_division").id:
                try:
                    obj.division = get_object_or_404(CommonDivisionsModel, pk=allif_data.get("logged_user_division").id)
                except Http404:
                    print(f"WARNING: Division with ID {allif_data.get('logged_user_division').id} not found for {obj.__class__.__name__}.")
                    obj.division = None
                except Exception as e:
                    print(f"ERROR: Failed to retrieve division with ID {allif_data.get('logged_user_division').id}: {e}")
                    obj.division = None
            else:
                pass
            # Branch
            if hasattr(obj, 'branch') and allif_data.get("logged_user_branch").id:
                try:
                    obj.branch = get_object_or_404(CommonBranchesModel, pk=allif_data.get("logged_user_branch").id)
                except Http404:
                    print(f"WARNING: Branch with ID {allif_data.get('logged_user_branch').id} not found for {obj.__class__.__name__}.")
                    obj.branch = None
                except Exception as e:
                    print(f"ERROR: Failed to retrieve branch with ID {allif_data.get('logged_user_branch').id}: {e}")
                    obj.branch = None
            else:
                pass
            # Department
            if hasattr(obj, 'department') and allif_data.get("logged_user_department").id:
                try:
                    obj.department = get_object_or_404(CommonDepartmentsModel, pk=allif_data.get("logged_user_department").id)
                except Http404:
                    print(f"WARNING: Department with ID {allif_data.get('logged_user_department').id} not found for {obj.__class__.__name__}.")
                    obj.department = None
                except Exception as e:
                    print(f"ERROR: Failed to retrieve department with ID {allif_data.get('logged_user_department').id}: {e}")
                    obj.department = None
            
            if hasattr(obj, 'operation_year') and allif_data.get("logged_user_operation_year").id:
                try:
                    obj.operation_year = get_object_or_404(CommonOperationYearsModel, pk=allif_data.get("logged_user_operation_year").id)
                except Http404:
                    print(f"WARNING: Operation year with ID {allif_data.get('logged_user_operation_year').id} not found for {obj.__class__.__name__}.")
                    obj.operation_year = None
                except Exception as e:
                    print(f"ERROR: Failed to retrieve operation year with ID {allif_data.get('logged_user_operation_year').id}: {e}")
                    obj.operation_year = None
                    
            if hasattr(obj, 'operation_term') and allif_data.get("logged_user_operation_term").id:
                try:
                    obj.operation_term = get_object_or_404(CommonOperationYearTermsModel, pk=allif_data.get("logged_user_operation_term").id)
                except Http404:
                    print(f"WARNING: Operation term with ID {allif_data.get('logged_user_operation_term').id} not found for {obj.__class__.__name__}.")
                    obj.operation_term = None
                except Exception as e:
                    print(f"ERROR: Failed to retrieve operation term with ID {allif_data.get('logged_user_operation_term').id}: {e}")
                    obj.operation_term = None
                    
                    
            # Owner (assuming 'usernmeslg' in allif_data is the User object)
            if hasattr(obj, 'owner') and allif_data.get("usernmeslg"):
                try:
                    obj.owner=allif_data.get("usernmeslg") # This should be the User object
                except Http404:
                    print(f"WARNING: User {allif_data.get("usernmeslg")} not found for {obj.__class__.__name__}.")
                    obj.owner = None
                except Exception as e:
                    print(f"ERROR: Failed to retrieve User {allif_data.get("usernmeslg")}: {e}")
                    obj.owner = None
            else:
                pass
            # --- Execute custom pre-save callback if provided ---
            if pre_save_callback:
                try:
                    pre_save_callback(obj, request, allif_data)
                except Exception as e:
                    print(f"ERROR: Pre-save callback failed for {obj.__class__.__name__}: {e}")
                    # You might want to add a user-facing error message here
                    form.add_error(None, f"An internal error occurred during custom processing: {e}")
                    # Re-render the form with errors
                    context = {
                        "form": form,
                        "title": title_text,
                        "user_var": allif_data.get("usrslg"),
                        "glblslug": allif_data.get("compslg"),
                        "error_message": form.errors, # Pass form errors
                    }
                    return render(request, template_path, context)

            else:
                pass
            obj.save() # Finally save the object after all assignments
            
            # Redirect to the specified list URL with user and company slugs
            return redirect(
                reverse(f'allifmaalcommonapp:{success_redirect_url_name}', 
                        kwargs={'allifusr': allif_data.get("usrslg"), 'allifslug': allif_data.get("compslg")})
            )
        else:
            # Form is invalid, render with errors
            error_message = form.errors
            allifcontext = {"error_message": error_message, "title": title_text}
            return render(request, 'allifmaalcommonapp/error/form-error.html', allifcontext)
    else:
        # GET request, initialize empty form
        form = form_class(*form_args, initial=initial_data)

    context = {
        "form": form,
        "title": title_text,
        "user_var": allif_data.get("usrslg"), 
        "glblslug": allif_data.get("compslg"), 
    }
    return render(request, template_path, context)



# --- NEW: Generic Edit Item LOGIC Function ---
def allif_common_form_edit_and_save(request, 
    pk: int, # Primary key of the object to edit
    form_class: type[forms.ModelForm], 
    title_text: str, 
    success_redirect_url_name: str, 
    template_path: str,
    pre_save_callback: Optional[callable] = None,
    extra_form_args: Optional[list] = None,
    extra_context: Optional[dict] = None # For passing additional context to template
):
    """
    Helper function to encapsulate the common logic for processing form submissions
    and saving updates to existing items.

    Args:
        request (HttpRequest): The HttpRequest object.
        pk (int): Primary key of the object to be edited.
        form_class (type[forms.ModelForm]): The specific ModelForm class to use.
        title_text (str): The title for the page.
        success_redirect_url_name (str): The Django URL name to redirect to on successful form submission.
        template_path (str): The path to the template to render.
        pre_save_callback (callable, optional): A function (obj, request, allif_data) -> None
                                                that performs model-specific assignments before obj.save().
        extra_form_args (list, optional): Additional positional arguments to pass to form_class.__init__.
        extra_context (dict, optional): Additional context variables to pass to the template.
    """
    allif_data = common_shared_data(request)
    company_id = allif_data.get("main_sbscrbr_entity").id

    # Determine the model class from the form's Meta
    model_class = form_class.Meta.model
    if not model_class:
        raise ValueError(f"Form {form_class.__name__} does not have a model defined in its Meta class.")

    # Retrieve the object to be updated using all_objects to bypass default managers
    # and get_object_or_404 for robust error handling.
    allifquery = get_object_or_404(model_class.all_objects, pk=pk)
   
    # --- Authorization Check (Crucial for multi-tenant/access control) ---
    # This is a placeholder. Implement your actual granular authorization logic here.
    if hasattr(allifquery, 'company')==100000:# you can remove this condition... just place  holder...
        raise Http404("Unauthorized: Item does not belong to your company or access denied.")
   
    # Add more granular checks (division, branch, department) if necessary,
    # similar to what you have in get_filtered_and_sorted_queryset.
   
    # Prepare form arguments for __init__ (company_id is typically the first)
    form_args = [company_id] 
    if extra_form_args:
        form_args.extend(extra_form_args)

    if request.method == 'POST':
        form = form_class(*form_args, request.POST, instance=allifquery) 
        if form.is_valid():
            obj = form.save(commit=False) # obj is now item_instance with updated data

            # --- Assign common 'updated_by' field ---
            if hasattr(obj, 'updated_by') and allif_data.get("usernmeslg"):
                obj.updated_by = allif_data.get("usernmeslg") # This should be the User object

            # --- Execute custom pre-save callback if provided ---
            if pre_save_callback:
                try:
                    pre_save_callback(obj, request, allif_data)
                except Exception as e:
                    print(f"ERROR: Pre-save callback failed for {obj.__class__.__name__} (edit): {e}")
                    form.add_error(None, f"An internal error occurred during custom processing: {e}")
                    context = {
                        "form": form, "title": title_text, "allifquery": allifquery,
                        "user_var": allif_data.get("usrslg"), "glblslug": allif_data.get("compslg"),
                        "error_message": form.errors,
                        **(extra_context or {})
                    }
                    return render(request, template_path, context)

            obj.save() # Save the updated object
            
            return redirect(
                reverse(f'allifmaalcommonapp:{success_redirect_url_name}', 
                        kwargs={'allifusr': allif_data.get("usrslg"), 'allifslug': allif_data.get("compslg")})
            )
        else:
            # Form is invalid, render with errors
            error_message = form.errors
            allifcontext = {
                "error_message": error_message, 
                "title": title_text, 
                "allifquery": allifquery, # Pass instance back for error rendering
                "user_var": allif_data.get("usrslg"), 
                "glblslug": allif_data.get("compslg"),
            }
            allifcontext.update(extra_context or {})
            return render(request, 'allifmaalcommonapp/error/form-error.html', allifcontext)
    else:
        # GET request, initialize form with instance data
        form = form_class(*form_args, instance=allifquery)

    context = {
        "form": form,
        "title": title_text,
        "allifquery":allifquery, # Pass the instance to the template for display
        "user_var": allif_data.get("usrslg"), 
        "glblslug": allif_data.get("compslg"), 
        **(extra_context or {})
    }
    return render(request, template_path, context)





# --- NEW: Generic Edit Item LOGIC Function ---
def allif_delete_confirm(request,pk: int,model_name: str,title_text: str, template_path: str):
    
    allif_data = common_shared_data(request)
    #model_class = model_name.model
    if not model_name:
        raise ValueError(f"Form {model_name.__name__} does not have a model defined in its Meta class.")

    allifquery = get_object_or_404(model_name.all_objects, pk=pk)
   
    context = {
        
        "title": title_text,
        "allifquery":allifquery, # Pass the instance to the template for display
        "user_var": allif_data.get("usrslg"), 
        "glblslug": allif_data.get("compslg"), 
        
    }
    return render(request, template_path, context)

def allif_delete_hanlder(request: HttpRequest,model_name: str,pk: int,success_redirect_url_name: str,):
    allif_data = common_shared_data(request)
    user_slug = allif_data.get("usrslg")
    company_slug = allif_data.get("compslg")
    model_class = allif_delete_models_class_map.get(model_name)
    if not model_class:
        raise Http404(f"Model '{model_name}' not found in mapping.")

    item = get_object_or_404(model_class.all_objects, pk=pk)

    item.delete()
    return redirect(reverse(f'allifmaalcommonapp:{success_redirect_url_name}',kwargs={'allifusr': user_slug, 'allifslug': company_slug}))









# --- NEW: Search Configuration Map ---
# Define which fields are searchable for each model
allif_search_config_mapping = {
    'CommonStocksModel': ['description__icontains', 'partNumber__icontains'],
    'CommonCurrenciesModel': ['name__icontains', 'description__icontains'],
    'CommonExpensesModel': ['description__icontains', 'amount__icontains', 'supplier__name__icontains'], # Example
    'CommonTasksModel': ['name__icontains', 'description__icontains'], # Example
    'TriagesModel': ['medical_file__icontains', 'pain_level__icontains'], # Example
    # Add configurations for other models as needed
}


# --- NEW: Centralized Search Handler ---
def allif_search_handler(
    request: HttpRequest,
    model_name: str,
    search_fields_key: str, # Key to look up in SEARCH_CONFIGS
    template_path: str,
    search_input_name: str = 'allifsearchcommonfieldname', # Name of the search input field
    extra_context: Optional[dict] = None
) -> HttpRequest:
    """
    Handles generic search functionality for various models.
    """
    allif_data = common_shared_data(request)
    user_slug = allif_data.get("usrslg")
    company_slug = allif_data.get("compslg")
    company_id = allif_data.get("main_sbscrbr_entity")

    title = "Search Results"
    searched_data = []
    search_term = None

    if request.method == 'POST':
        search_term = request.POST.get(search_input_name, '').strip()
    elif request.method == 'GET': # Allow GET for initial display or direct search URLs
        search_term = request.GET.get(search_input_name, '').strip()

    if search_term:
        model_class = allif_delete_models_class_map.get(model_name)
        if not model_class:
            print(f"ERROR: Search - Model '{model_name}' not found in allif_delete_models_class_map.")
            raise Http404(f"Model '{model_name}' not found for search.")

        search_fields =allif_search_config_mapping.get(search_fields_key)
        if not search_fields:
            print(f"ERROR: Search - No search fields configured for key '{search_fields_key}' in allif_search_config_mapping.")
            raise ValueError(f"Search configuration missing for '{search_fields_key}'.")

        # Build dynamic Q objects for search
        q_objects = Q()
        for field in search_fields:
            # Assumes field names include lookup like 'description__icontains'
            q_objects |= Q(**{field: search_term})

        # Apply the search query and company filter
        queryset = model_class.objects.filter(q_objects)
        if hasattr(model_class, 'company') and company_id:
            queryset = queryset.filter(company=company_id)
        
        # Apply multi-tenancy access filters (division, branch, department)
        # This reuses logic from get_filtered_and_sorted_queryset if applicable
        if allif_data.get("logged_in_user_has_universal_access"):
            pass 
        elif allif_data.get("logged_in_user_has_divisional_access"):
            if hasattr(model_class, 'division'):
                queryset = queryset.filter(division=allif_data.get("logged_user_division"))
            else:
                queryset = model_class.objects.none()
        elif allif_data.get("logged_in_user_has_branches_access"):
            if hasattr(model_class, 'division') and hasattr(model_class, 'branch'):
                queryset = queryset.filter(
                    division=allif_data.get("logged_user_division"),
                    branch=allif_data.get("logged_user_branch")
                )
            else:
                queryset = model_class.objects.none()
        elif allif_data.get("logged_in_user_has_departmental_access"):
            if hasattr(model_class, 'division') and hasattr(model_class, 'branch') and hasattr(model_class, 'department'):
                queryset = queryset.filter(
                    division=allif_data.get("logged_user_division"),
                    branch=allif_data.get("logged_user_branch"),
                    department=allif_data.get("logged_user_department")
                )
            else:
                queryset = model_class.objects.none()
        else:
            queryset = model_class.objects.none()

        searched_data = queryset.distinct() # Use distinct to avoid duplicates if Q objects overlap

    context = {
        "title": title,
        "searched_data": searched_data,
        "user_var": user_slug,
        "glblslug": company_slug,
        "search_term": search_term, # Pass the search term back to the template for display
        **(extra_context or {}) # Include any extra context passed in
    }
    return render(request, template_path, context)


# C:\am\allifapp\allifapperp\allifmaalcommonapp\utils.py

from django.db.models import QuerySet, Model, Q # Ensure Q is imported
from django.http import HttpRequest, Http404, HttpResponse # Ensure HttpResponse is imported
from django.shortcuts import render, get_object_or_404, redirect 
from django.urls import reverse 
from django.utils import timezone # For timezone.now()
from typing import Optional, Dict, List, Any

# For PDF generation
from django.template.loader import get_template
from xhtml2pdf import pisa # Assuming xhtml2pdf is installed (pip install xhtml2pdf)


# --- NEW: Advanced Search Configuration Map ---
# Define which fields are used for date and value range filtering for each model
allif_advanced_search_configs = {
    'CommonCurrenciesModel': {
        'date_field': 'date', # Name of the date field in CommonStocksModel
        'value_field': 'quantity', # Name of the quantity/value field in CommonStocksModel
        'default_order_by_date': '-date', # Default ordering for finding first/last date
        'default_order_by_value': '-quantity', # Default ordering for finding largest value
    },
    # Add configurations for other models here, e.g.:
    'CommonExpensesModel': {
        'date_field': 'created_at',
         'value_field': 'amount',
         'default_order_by_date': '-created_at',
         'default_order_by_value': '-amount',
     },
     'CommonCustomerPaymentsModel': {
         'date_field': 'payment_date',
         'value_field': 'amount_paid',
         'default_order_by_date': '-payment_date',
         'default_order_by_value': '-amount_paid',
     },
}

# --- NEW: Generic PDF Generation Utility ---
def allif_generate_pdf_response(
    template_path: str, 
    context: Dict[str, Any], 
    filename: str = "document.pdf"
) -> HttpResponse:
    """
    Generates a PDF response from a Django template using xhtml2pdf.
    """
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{filename}"'
    
    try:
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            # If there's an error during PDF creation, return a generic error message
            print(f"ERROR: PDF generation failed: {pisa_status.err}")
            return HttpResponse('We had some errors generating the PDF. Please try again.', status=500)
    except Exception as e:
        print(f"CRITICAL ERROR: Exception during PDF generation: {e}")
        return HttpResponse(f"An unexpected error occurred during PDF generation: {e}", status=500)
    
    return response


# --- NEW: Centralized Advanced Search Handler ---
def allif_advance_search_handler(
    request: HttpRequest,
    model_name: str,
    advanced_search_config_key: str, # Key to look up in ADVANCED_SEARCH_CONFIGS
    template_html_path: str,
    template_pdf_path: Optional[str] = None, # Path to the PDF template
    extra_context: Optional[dict] = None
) -> HttpResponse:
    """
    Handles generic advanced search functionality (date/value ranges) for various models,
    including conditional PDF generation.
    """
    allif_data = common_shared_data(request)
    user_slug = allif_data.get("usrslg")
    company_slug = allif_data.get("compslg")
    company_id = allif_data.get("main_sbscrbr_entity")

    title = "Advanced Search Results"
    searched_data = []
    
    model_class = allif_delete_models_class_map.get(model_name)
    if not model_class:
        print(f"ERROR: Advanced Search - Model '{model_name}' not found in allif_delete_models_class_map.")
        raise Http404(f"Model '{model_name}' not found for advanced search.")

    search_config = allif_advanced_search_configs.get(advanced_search_config_key)
    if not search_config:
        print(f"ERROR: Advanced Search - No configuration for key '{advanced_search_config_key}' in ADVANCED_SEARCH_CONFIGS.")
        raise ValueError(f"Advanced search configuration missing for '{advanced_search_config_key}'.")

    date_field = search_config['date_field']
    value_field = search_config['value_field']
    default_order_by_date = search_config['default_order_by_date']
    default_order_by_value = search_config['default_order_by_value']

    # --- Calculate dynamic default values for date and amount ranges ---
    current_date = timezone.now().date()
    # Filter by company for defaults
    company_queryset = model_class.objects.filter(company=company_id)

    first_item_by_date = company_queryset.order_by(date_field).first()
    last_item_by_date = company_queryset.order_by(f'-{date_field}').first()
    largest_item_by_value = company_queryset.order_by(default_order_by_value).first()

    firstDate = getattr(first_item_by_date, date_field, current_date) if first_item_by_date else current_date
    lastDate = getattr(last_item_by_date, date_field, current_date) if last_item_by_date else current_date
    largestAmount = getattr(largest_item_by_value, value_field, 0) if largest_item_by_value else 0

    # Ensure largestAmount is at least 0 if no items exist
    largestAmount = max(0, largestAmount)

    # Fetch common data for context (formats, scopes)
    formats = CommonDocsFormatModel.objects.all()
    scopes = CommonCompanyScopeModel.objects.filter(company=company_id).order_by('-date')[:4] # Adjust ordering/slicing as needed

    # --- Process POST/GET request for search parameters ---
    if request.method == 'POST':
        selected_option = request.POST.get('requiredformat')
        start_date_str = request.POST.get('startdate')
        end_date_str = request.POST.get('enddate')
        start_value_str = request.POST.get('startvalue')
        end_value_str = request.POST.get('endvalue')
    else: # Initial GET request or GET with parameters
        selected_option = request.GET.get('requiredformat')
        start_date_str = request.GET.get('startdate')
        end_date_str = request.GET.get('enddate')
        start_value_str = request.GET.get('startvalue')
        end_value_str = request.GET.get('endvalue')
    
    # Convert string inputs to appropriate types, using defaults if empty
    start_date = start_date_str if start_date_str else None
    end_date = end_date_str if end_date_str else None
    start_value = float(start_value_str) if start_value_str else None
    end_value = float(end_value_str) if end_value_str else None

    # Determine if any search criteria were provided
    search_criteria_provided = any([start_date_str, end_date_str, start_value_str, end_value_str])

    if search_criteria_provided:
        # Start with the base company-filtered queryset
        queryset = company_queryset # Already filtered by company

        # Apply multi-tenancy access filters
        queryset = allif_filtered_and_sorted_queryset(request, model_class, allif_data, explicit_scope='all') # Use 'all' scope for advanced search base

        # Apply date range filters
        if start_date:
            queryset = queryset.filter(**{f'{date_field}__gte': start_date})
        else:
            queryset = queryset.filter(**{f'{date_field}__gte': firstDate})
        
        if end_date:
            queryset = queryset.filter(**{f'{date_field}__lte': end_date})
        else:
            queryset = queryset.filter(**{f'{date_field}__lte': lastDate})

        # Apply value range filters
        if start_value is not None:
            queryset = queryset.filter(**{f'{value_field}__gte': start_value})
        else:
            queryset = queryset.filter(**{f'{value_field}__gte': 0}) # Default to 0 if not provided
        
        if end_value is not None:
            queryset = queryset.filter(**{f'{value_field}__lte': end_value})
        else:
            queryset = queryset.filter(**{f'{value_field}__lte': largestAmount}) # Default to largestAmount if not provided

        searched_data = queryset.distinct() # Use distinct to avoid duplicates if Q objects overlap

    # Prepare context for rendering
    context = {
        "title": title,
        "searched_data": searched_data,
        "formats": formats,
        "scopes": scopes,
        "user_var": user_slug,
        "glblslug": company_slug,
        "firstDate": firstDate,
        "lastDate": lastDate,
        "largestAmount": largestAmount,
        # Pass back search inputs for form persistence
        "start_date_input": start_date_str,
        "end_date_input": end_date_str,
        "start_value_input": start_value_str,
        "end_value_input": end_value_str,
        "selected_format_input": selected_option,
        **(extra_context or {}) # Include any extra context passed in
    }

    # --- Conditional Output (HTML or PDF) ---
    if selected_option == "pdf" and template_pdf_path:
        return allif_generate_pdf_response(
            template_pdf_path,
            context,
            filename=f"{advanced_search_config_key.lower()}-advanced-search-results.pdf"
        )
    else:
        # If no search criteria, or not PDF, render the HTML template
        return render(request, template_html_path, context)

# --- NEW: Document PDF Configuration Map ---
# Defines the main model, related items model, and context keys for each document type
DOCUMENT_PDF_CONFIGS = {
    'CommonPurchaseOrdersModel': { # Key for Purchase Orders
        'main_model': 'CommonPurchaseOrdersModel',
        'items_model': 'CommonPurchaseOrderItemsModel',
        'items_related_field': 'po_item_con', # Field on items model linking to main PO
        'title': 'Purchase Order',
        'filename_prefix': 'PO',
        'template_path': 'allifmaalcommonapp/currencies/currencies-pdf.html',
        'extra_context_fields': { # Map main_model fields to context names
            'supplier': 'po_supplier', # allifquery.supplier becomes context['po_supplier']
        },
        'related_lookups': ['supplier'], # Fields to select_related or prefetch_related for main model
    },
    # Add configurations for other document types, e.g.:
    # 'CommonInvoicesModel': {
    #     'main_model': 'CommonInvoicesModel',
    #     'items_model': 'CommonInvoiceItemsModel',
    #     'items_related_field': 'invoice_item_con',
    #     'title': 'Invoice',
    #     'filename_prefix': 'INV',
    #     'template_path': 'allifmaalcommonapp/sales/invoice-pdf.html',
    #     'extra_context_fields': {
    #         'customer': 'invoice_customer',
    #     },
    #     'related_lookups': ['customer'],
    # },
    # 'CommonQuotesModel': {
    #     'main_model': 'CommonQuotesModel',
    #     'items_model': 'CommonQuoteItemsModel',
    #     'items_related_field': 'quote_item_con',
    #     'title': 'Quotation',
    #     'filename_prefix': 'QTE',
    #     'template_path': 'allifmaalcommonapp/sales/quote-pdf.html',
    #     'extra_context_fields': {
    #         'customer': 'quote_customer',
    #     },
    #     'related_lookups': ['customer'],
    # },
}


# C:\am\allifapp\allifapperp\allifmaalcommonapp\utils.py

# --- Standard Python Imports ---
from typing import Optional, Dict, List, Any
import datetime # Added for default date handling if needed

# --- Django Imports ---
from django.db.models import QuerySet, Model, Q 
from django.http import HttpRequest, Http404, HttpResponse 
from django.shortcuts import render, get_object_or_404, redirect 
from django.urls import reverse 
from django.utils import timezone 
from django.template.loader import get_template 

# --- Third-party Imports ---
from xhtml2pdf import pisa 


# --- ALLIF_MODEL_REGISTRY (Central Model Class Map) ---
# This dictionary maps model names (strings) to their actual Python model classes.
# It's used by all generic handlers (delete, search, advanced search, PDF generation)
# to dynamically get the correct model class based on a string name.
ALLIF_MODEL_REGISTRY = { 
    'CommonSectorsModel': CommonSectorsModel,
    'CommonCompanyScopeModel': CommonCompanyScopeModel,
    'CommonTaxParametersModel': CommonTaxParametersModel,
    'CommonExpensesModel': CommonExpensesModel,
    'CommonTasksModel': CommonTasksModel,
    'CommonBanksModel': CommonBanksModel,
    'TriagesModel': TriagesModel, 
    'CommonCurrenciesModel': CommonCurrenciesModel, 
    'CommonSupplierPaymentsModel': CommonSupplierPaymentsModel,
    'CommonCustomerPaymentsModel': CommonCustomerPaymentsModel,
    'CommonPaymentTermsModel': CommonPaymentTermsModel,
    'CommonTransitModel': CommonTransitModel,
    'CommonStocksModel': CommonStocksModel, 
    'CommonPurchaseOrdersModel': CommonPurchaseOrdersModel, # <-- CRITICAL: Must be here
    'CommonPurchaseOrderItemsModel': CommonPurchaseOrderItemsModel, # <-- CRITICAL: Must be here
    # Add other document models here if you add them to imports above
    # 'CommonInvoicesModel': CommonInvoicesModel, 
    # 'CommonInvoiceItemsModel': CommonInvoiceItemsModel, 
    # 'CommonQuotesModel': CommonQuotesModel, 
    # 'CommonQuoteItemsModel': CommonQuoteItemsModel, 
}

# --- Search Configuration Map (for simple search) ---
SEARCH_CONFIGS = {
    'CommonStocksModel': ['description__icontains', 'partNumber__icontains'],
    'CommonCurrencyModel': ['name__icontains', 'description__icontains'],
    'CommonExpensesModel': ['description__icontains', 'amount__icontains', 'supplier__name__icontains'], 
    'CommonTasksModel': ['name__icontains', 'description__icontains'], 
    'TriagesModel': ['medical_file__icontains', 'pain_level__icontains'], 
}

# --- Advanced Search Configuration Map ---
ADVANCED_SEARCH_CONFIGS = {
    'CommonStocksModel': {
        'date_field': 'date', 
        'value_field': 'quantity', 
        'default_order_by_date': '-date', 
        'default_order_by_value': '-quantity', 
    },
    # Add configurations for other models here
}

# --- Document PDF Configuration Map ---
# Defines the main model, related items model, and context keys for each document type
DOCUMENT_PDF_CONFIGS = {
    'CommonPurchaseOrdersModel': { # Key for Purchase Orders
        'main_model': 'CommonPurchaseOrdersModel', # String name of the main model
        'items_model': 'CommonPurchaseOrderItemsModel', # String name of the items model
        'items_related_field': 'po_item_con', # Field on items model linking to main PO
        'title': 'Purchase Order',
        'filename_prefix': 'PO',
        'template_path': 'allifmaalcommonapp/purchases/po-pdf.html', # <-- Corrected template path for PO
        'extra_context_map': { # Map main_model fields to context names
            'supplier': 'po_supplier', # allifquery.supplier becomes context['po_supplier']
        },
        'related_lookups': ['supplier'], # Fields to select_related for main model optimization
    },
    # Add configurations for other document types as needed, e.g.:
     'CommonCurrenciesModel': {
         'main_model': 'CommonCurrenciesModel',
         'items_model': 'CommonCurrenciesModel',
         'items_related_field': 'invoice_item_con',
       'title': 'Invoice',
         'filename_prefix': 'INV',
         'template_path': 'allifmaalcommonapp/sales/invoice-pdf.html',
    #     'extra_context_map': {
    #         'customer': 'invoice_customer',
    #     },
    #     'related_lookups': ['customer'],
     },
}


# --- Centralized Document PDF Handler ---
def allif_document_pdf_handler(
    request: HttpRequest,
    pk: int,
    document_config_key: str, # Key to look up in DOCUMENT_PDF_CONFIGS
    extra_context: Optional[Dict[str, Any]] = None
) -> HttpResponse:
    """
    Handles generic PDF generation for various document types (PO, Invoice, Quote, etc.).
    Fetches the main document and its related items based on configuration.
    """
    allif_data = common_shared_data(request)
    company_id = allif_data.get("main_sbscrbr_entity")
    user_slug = allif_data.get("usrslg")
    company_slug = allif_data.get("compslg")

    config = DOCUMENT_PDF_CONFIGS.get(document_config_key)
    if not config:
        print(f"ERROR: PDF Handler - No configuration for key '{document_config_key}' in DOCUMENT_PDF_CONFIGS.")
        raise ValueError(f"Document PDF configuration missing for '{document_config_key}'.")

    main_model_name = config['main_model']
    
    items_model_name = config['items_model']
    items_related_field = config['items_related_field']
    title_prefix = config['title']
    filename_prefix = config['filename_prefix']
    template_path = config['template_path']
    extra_context_map = config.get('extra_context_map', {})
    related_lookups = config.get('related_lookups', [])

    # Debugging print to see what's being looked up
    print(f"DEBUG: PDF Handler - Looking up main_model_name: '{main_model_name}' and items_model_name: '{items_model_name}' in ALLIF_MODEL_REGISTRY.")

    main_model_class = ALLIF_MODEL_REGISTRY.get(main_model_name) # <-- Using ALLIF_MODEL_REGISTRY
    items_model_class = ALLIF_MODEL_REGISTRY.get(items_model_name) # <-- Using ALLIF_MODEL_REGISTRY

    if not main_model_class or not items_model_class:
        print(f"ERROR: PDF Handler - main_model_class: {main_model_class}, items_model_class: {items_model_class}")
        print(f"ERROR: PDF Handler - Model classes not found for '{main_model_name}' or '{items_model_name}' in ALLIF_MODEL_REGISTRY.")
        raise Http404("Required models not found for PDF generation.1111")

    try:
        # Fetch the main document object
        main_query = main_model_class.all_objects.filter(pk=pk)
        
        # Apply select_related/prefetch_related for optimized fetching of related data
        if related_lookups:
            main_query = main_query.select_related(*related_lookups)

        main_document = get_object_or_404(main_query, pk=pk)

        # --- Authorization Check (Crucial for multi-tenant) ---
        
        # Fetch related items for the document
        items_queryset = items_model_class.objects.filter(**{items_related_field: main_document})

        # Prepare context for the PDF template
        context = {
            "title": title_prefix,
            "main_sbscrbr_entity": allif_data.get("main_sbscrbr_entity"),
            "scopes": CommonCompanyScopeModel.objects.filter(company=company_id).order_by('-date')[:4], 
            "allifquery": main_document, 
            "allifqueryset": items_queryset, 
            "system_user": allif_data.get("owner_user_object"), 
            "user_var": user_slug, 
            "glblslug": company_slug, 
            "timezone": timezone, 
        }

        # Add any extra context fields dynamically from the main_document
        for model_field, context_name in extra_context_map.items():
            if hasattr(main_document, model_field):
                context[context_name] = getattr(main_document, model_field)

        # Merge any additional context passed from the view
        context.update(extra_context or {})

        # Generate filename
        filename = f"{filename_prefix}-{main_document.pk}.pdf" 
        if hasattr(main_document, 'name'): 
            filename = f"{filename_prefix}-{getattr(main_document, 'name')}-{main_document.pk}.pdf"
        elif hasattr(main_document, '__str__'): 
            filename = f"{filename_prefix}-{str(main_document).replace(' ', '_')}-{main_document.pk}.pdf"
        
        # Call the generic PDF generation utility
        return allif_generate_pdf_response(template_path, context, filename=filename)

    except Http404 as e:
        raise e 
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to generate PDF for {document_config_key} (ID: {pk}): {e}")
        raise Http404(f"An unexpected error occurred during PDF generation: {e}")
