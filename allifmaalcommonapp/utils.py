# C:\am\allifapp\allifapperp\allifmaalcommonapp\utils.py

# C:\am\allifapp\allifapperp\allifmaalcommonapp\utils.py
from django import forms # Import forms for type hinting if needed
from django.db.models import QuerySet # Import QuerySet for type hinting

from django.db.models import QuerySet, Model # Import Model
from django.http import HttpRequest

from typing import Optional # Import Optional for type hinting
from .models import *
from allifmaalshaafiapp.models import *


from django.shortcuts import render,redirect,get_object_or_404
from .allifutils import common_shared_data
from django.urls import reverse
from django.http import Http404



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
def common_form_edit_and_save(request, 
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


# --- NEW: Generic Direct Delete Logic Function ---
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
  