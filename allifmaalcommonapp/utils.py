# C:\am\allifapp\allifapperp\allifmaalcommonapp\utils.py

# C:\am\allifapp\allifapperp\allifmaalcommonapp\utils.py

from django.db.models import QuerySet # Import QuerySet for type hinting

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

