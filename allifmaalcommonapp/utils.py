# C:\am\allifapp\allifapperp\allifmaalcommonapp\utils.py

# C:\am\allifapp\allifapperp\allifmaalcommonapp\utils.py
from django import forms # Import forms for type hinting if needed
from django.db.models import QuerySet # Import QuerySet for type hinting

from django.db.models import QuerySet, Model # Import Model
from django.http import HttpRequest

from typing import Optional # Import Optional for type hinting
def get_filtered_queryset_by_access(request, model_class, allif_data, extra_filters=None, access_scope='active'):
    """
Filters a queryset based on the user's access level (universal, divisional, branch, departmental).
    Assumes model_class inherits from CommonBaseModel, where 'objects' manager
    already handles 'Active' status and 'Deletable' delete_status, and 'for_company' method.
    Now that the default manager (objects) already handles "active" status and for_company filtering,
    the utility function becomes much simpler. It will primarily focus on applying the division, branch, and 
    department filters based on user access.
    ...queryset = model_class.objects.for_company(allif_data.get("main_sbscrbr_entity")): This is the core simplification. We directly use the default objects manager (which is ActiveManager) and its for_company method. This means status='Active',
    delete_status='Deletable', and company=current_company are all applied in the initial query.
    The if/elif chain now only needs to add division, branch, or department filters, making it much cleaner.
    The hasattr checks are still important because while CommonBaseModel defines these fields,
    a specific model might not actually use them or they might be null=True. This ensures the filtering 
    doesn't break if a field is unexpectedly missing or not populated for a given model.
    ...
    access_scope parameter: Introduced with a default of 'active'.

    Conditional Base Queryset: The first part of the function now dynamically selects the starting manager (objects, all_objects, or objects.archived()) based on access_scope.

    Direct company filter: Instead of relying on for_company for all_objects (which doesn't have it), we apply the company filter directly to the queryset after selecting the base manager. This ensures consistency.
"""
    """
    Filters a queryset based on the user's access level (universal, divisional, branch, departmental)
    and the desired access scope (active, all, archived).

    Assumes model_class inherits from CommonBaseModel, where 'objects' manager
    handles 'Active' status and 'Deletable' delete_status, and 'for_company' method.
    Also assumes 'all_objects' and 'objects.archived()' managers are available.

    Args:
        request: The HttpRequest object.
        model_class: The Django Model class (e.g., CommonTasksModel, TriagesModel).
                     Must inherit from CommonBaseModel.
        allif_data: The dictionary containing user access data from common_shared_data.
        extra_filters (dict, optional): A dictionary of additional filters to apply
                                        (e.g., {'task_status': 'complete'}).
        access_scope (str): Defines which set of records to retrieve:
                            - 'active' (default): Uses model_class.objects (ActiveManager's default).
                            - 'all': Uses model_class.all_objects (all records, including inactive/archived).
                            - 'archived': Uses model_class.objects.archived() (only archived records).

    Returns:
        QuerySet: The filtered queryset, or an empty queryset if no access or no matching fields.
    """
    
    # 1. Determine the base queryset based on access_scope
    if access_scope == 'all':
        # Use the 'all_objects' manager to bypass default active/deletable filtering
        queryset = model_class.all_objects.all()
    elif access_scope == 'archived':
        # Use the 'archived' method from the default manager (ActiveManager)
        queryset = model_class.objects.archived()
    else: # Default is 'active'
        # Use the default 'objects' manager (which is ActiveManager)
        # This automatically filters by status='Active' and delete_status='Deletable'
        queryset = model_class.objects.all()

    # 2. Apply company filter (if the model has a 'company' field and company_id is available)
    company_id = allif_data.get("main_sbscrbr_entity")
    if hasattr(model_class, 'company') and company_id:
        # The 'for_company' method is part of ActiveManager, which 'objects' is.
        # If we started with 'all_objects', we need to filter manually.
        # So, it's safer to just apply the filter directly here to the base queryset.
        queryset = queryset.filter(company=company_id)
    
    # 3. Apply any additional filters specific to the view
    if extra_filters:
        queryset = queryset.filter(**extra_filters)

    # 4. Apply access level filtering for division, branch, department
    if allif_data.get("logged_in_user_has_universal_access"):
        # Universal access: company filter (already applied above) and extra_filters are sufficient.
        pass 
    elif allif_data.get("logged_in_user_has_divisional_access"):
        if hasattr(model_class, 'division'): # Check if model has the field
            queryset = queryset.filter(division=allif_data.get("logged_user_division"))
        else:
            queryset = model_class.objects.none() # Return empty if model doesn't support this level of access
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
        # No specific access level, or access denied
        queryset = model_class.objects.none() # Return an empty queryset

    # 5. Apply ordering if 'date' field exists (assuming 'date' is a common field in CommonBaseModel or specific models)
    return queryset.order_by('date') if hasattr(model_class, 'date') else queryset

# C:\am\allifapp\allifapperp\allifmaalcommonapp\utils.py

from django.db.models import QuerySet

def apply_sorting(queryset: QuerySet, request, default_sort_field: str, valid_sort_fields: list) -> QuerySet:
    """
    Applies ordering to a Django QuerySet based on a 'sort' GET parameter.
    This is universal and can be used for any model.

    Args:
        queryset (QuerySet): The base QuerySet to apply sorting to.
        request (HttpRequest): The HttpRequest object containing GET parameters.
        default_sort_field (str): The field to sort by if no 'sort' GET param is provided or is invalid.
                                  Prefix with '-' for descending (e.g., '-created_at').
        valid_sort_fields (list): A list of allowed field names for sorting (e.g., ['name', '-name', 'price', '-price']).
                                  Crucial for security to prevent sorting by arbitrary columns.

    Returns:
        QuerySet: The sorted QuerySet.
    """
    sort_by = request.GET.get('sort', default_sort_field)
    
    # Validate sort_by field for security and robustness
    # Check if the requested sort_by is in the list of valid fields.
    # Also check if the underlying model actually has the field (stripping the '-' for descending).
    # 'pk' is a universal field, so allow it even if not explicitly in model fields.
    field_to_check = sort_by.lstrip('-')
    if sort_by not in valid_sort_fields or not (hasattr(queryset.model, field_to_check) or field_to_check == 'pk'):
        sort_by = default_sort_field # Fallback to default if invalid or field doesn't exist

    return queryset.order_by(sort_by)


# C:\am\allifapp\allifapperp\allifmaalcommonapp\utils.py
from django.db import models
from django.db.models import QuerySet, Manager
from django.http import HttpRequest

def get_filtered_and_sorted_queryset_one_can_deleted_if_not_nneed(
    request: HttpRequest, 
    model_class: type[models.Model], # Pass the Model class itself (e.g., CommonExpensesModel)
    allif_data: dict, 
    sort_mapping: dict, # Dictionary to map UI choice to actual field name
    default_sort_field: str = '-date' # Default sort if nothing selected
) -> QuerySet:
    """
    Applies common filtering (company, scope, access levels) and sorting to a queryset.
    This utility function will take the request, the Model class you want to query, and 
    your allif_data (which contains access levels and company ID). It will then apply all the 
    common filtering (company, division, branch, department, and scope) and then apply the sorting based on
    the user's selection.
    This function will handle all the common filtering (company, access levels, scope) and the sorting logic.
    
    ...EXPLANATIONS....
    #model_class: You pass the actual Python class (e.g., CommonExpensesModel), not an instance.This allows the utility to work with any model.

    #sort_mapping: This dictionary is crucial. It maps the user-friendly string from your 
    dropdown (e.g., "Amount Descending") to the actual Django field name (e.g., '-amount'). This makes the if/elif chain for sorting obsolete.

    #Consolidated Filtering: All the if/elif logic for company, scope, division, branch, department is now inside this one function.

    #POST Sorting: It specifically looks for sort_option from request.POST.

    #GET Fallback: It includes a fallback to request.GET.get('sort') if no POST data is present, allowing you
    to mix and match. This means if you still have scope buttons that use GET, they'll work, and if a user 
    manually types ?sort=... in the URL, it will also work.

    Args:
        request (HttpRequest): The HttpRequest object.
        model_class (models.Model): The Django Model class to query (e.g., CommonExpensesModel).
        allif_data (dict): Dictionary containing user access levels and company ID.
        sort_mapping (dict): A dictionary mapping UI selection strings to model field names for sorting.
                             Example: {"Name": "name", "Amount": "-amount", "Quantity": "-quantity"}
        default_sort_field (str): The field to sort by if no valid sort option is provided.

    Returns:
        QuerySet: The filtered and sorted QuerySet.
    """
    company_id = allif_data.get("main_sbscrbr_entity")

    # --- 1. Determine the base queryset based on 'scope' GET parameter ---
    # Scope is usually a navigation filter, so it typically comes from GET
    scope = request.GET.get('scope', 'active') 
    
    base_manager = model_class.objects # Default to ActiveManager
    if hasattr(model_class, 'all_objects') and scope == 'all':
        base_manager = model_class.all_objects
    elif hasattr(model_class.objects, 'archived') and scope == 'archived':
        base_manager = model_class.objects.archived()
    else: # 'active' or any other invalid scope defaults to active
        base_manager = model_class.objects.all() # Ensure it's a queryset, not just the manager

    queryset = base_manager

    # --- 2. Apply company filter ---
    if hasattr(model_class, 'company') and company_id:
        queryset = queryset.filter(company=company_id)
    else:
        # If model doesn't have 'company' or company_id is missing,
        # it's safer to return an empty queryset or handle as per business logic.
        # For now, we'll let it proceed, but filtering by company will be skipped.
        pass 
    
    # --- 3. Apply access level filtering (division, branch, department) ---
    # This is the repetitive part that gets consolidated here
    if allif_data.get("logged_in_user_has_universal_access"):
        pass # Universal access means company filter is enough
    elif allif_data.get("logged_in_user_has_divisional_access"):
        if hasattr(model_class, 'division'):
            queryset = queryset.filter(division=allif_data.get("logged_user_division"))
        else:
            queryset = model_class.objects.none() # No division field, so no data
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
        queryset = model_class.objects.none() # No specific access level, or access denied

    # --- 4. Apply sorting based on POST data (from your form) ---
    # Get the selected option from the POST request
    selected_option = request.POST.get('sort_option') # Assuming 'sort_option' is the name of your select field

    sort_field = default_sort_field # Start with default
    if selected_option and selected_option in sort_mapping:
        sort_field = sort_mapping[selected_option]
    elif request.GET.get('sort'): # Fallback to GET 'sort' parameter if POST not used or invalid
        # This allows the URL-based sorting (from previous solutions) to still work
        # if the user manually changes the URL or if scope buttons are clicked.
        # We need to validate this GET 'sort' against the values in sort_mapping
        # to ensure it's a valid and allowed field.
        # Find if the GET sort value matches any of the sort_mapping values
        # This is a bit more complex, so for simplicity, we'll just check if it's
        # one of the *values* in the sort_mapping.
        allowed_sort_values = list(sort_mapping.values())
        if request.GET.get('sort') in allowed_sort_values:
            sort_field = request.GET.get('sort')
        else:
            # If GET sort is invalid, revert to default
            sort_field = default_sort_field


    # Apply the sorting
    queryset = queryset.order_by(sort_field)

    return queryset







# Define sort mappings and default sort fields for different models here.
# Use a clear identifier (e.g., model name in lowercase) as the key.
MODEL_SORT_CONFIGS = {
    'commonexpensesmodel': { # Key should be consistent, e.g., model._meta.model_name
        'sort_mapping': {
            "Expense Name Ascending": "name",
            "Expense Name Descending": "-name",
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

def get_filtered_and_sorted_queryset____one(request: HttpRequest,model_class: type[Model],allif_data: dict,) -> QuerySet:
    """
    Applies common filtering (company, scope, access levels) and sorting to a queryset.
    Retrieves sort_mapping and default_sort_field from MODEL_SORT_CONFIGS.

    Args:
        request (HttpRequest): The HttpRequest object.
        model_class (type[models.Model]): The Django Model class to query (e.g., CommonExpensesModel).
        allif_data (dict): Dictionary containing user access levels and company ID.

    Returns:
        QuerySet: The filtered and sorted QuerySet.
    """
    company_id = allif_data.get("main_sbscrbr_entity")

    # Get sort configuration for the given model
    model_identifier = model_class._meta.model_name # Gets the lowercase of the model name
    
    sort_config = MODEL_SORT_CONFIGS.get(model_identifier, {}) # gives specific model fields....
    
    sort_mapping = sort_config.get('sort_mapping', {}) # this also gives like sort_config
    
    default_sort_field = sort_config.get('default_sort_field', '-date') # this two give the default values
    default_ui_label = sort_config.get('default_ui_label', 'Default Sort')
   
    # --- 1. Determine the base queryset based on 'scope' GET parameter ---
    scope = request.GET.get('archived', 'active') 
    
    base_queryset_method = model_class.objects.all 
    if hasattr(model_class, 'all_objects') and scope == 'all': # not met
        base_queryset_method = model_class.all_objects.all
        
    elif hasattr(model_class.objects, 'archived') and scope == 'archived': # not met
        base_queryset_method = model_class.objects.archived
        
    else: # does this
        pass
        
    queryset = base_queryset_method() 

    # --- 2. Apply company filter ---
    if hasattr(model_class, 'company') and company_id: # this is met for now....
        queryset = queryset.filter(company=company_id)
        
    else:
        pass 
    
    # --- 3. Apply access level filtering (division, branch, department) ---
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

    # --- 4. Determine and apply sorting based on POST data (from your form) ---
    selected_ui_label = request.POST.get('sort_option') # TAKE NOTICE THAT sort_option COMING FROM templates... BOTH GIVE NONE FIRST, THEN EXPENSE SHOWS THE SELECTED AFTER YOU SLECT FILTER
   
    
    # If no POST, check GET for 'sort_ui_label' (for initial loads/scope changes)
    if not selected_ui_label and request.GET.get('sort_ui_label'):
        selected_ui_label = request.GET.get('sort_ui_label')
       
    else: # both fire execute this else
        pass
        
    # Resolve the actual sort field from the UI label
    sort_field = sort_mapping.get(selected_ui_label, default_sort_field) # all gives date field
   
    # Ensure selected_ui_label is set to the default if it was initially invalid or missing
    if not selected_ui_label or selected_ui_label not in sort_mapping:
        selected_ui_label = default_ui_label
        
    else:
        pass
      
    # Apply the sorting
    queryset = queryset.order_by(sort_field)
  
    # Attach the resolved UI label and sort mapping to the queryset for easy access in the view
    queryset.current_sort_ui_label = selected_ui_label # both give created at ascending
   
    queryset.sort_options = sort_mapping.items() 
   
    queryset.current_scope = scope 
   
    return queryset



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
def initialize_form_select_querysets(form_instance: forms.Form, allifmaalparameter: str, field_model_map: dict):
    """
    Initializes querysets for Select/ModelChoiceFields in a form based on a parameter.
    ...Explanation of initialize_form_select_querysets:

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


