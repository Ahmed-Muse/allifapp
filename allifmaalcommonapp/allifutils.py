# allifmaalcommonapp/utils.py
from django.shortcuts import render
from allifmaalusersapp.models import User
from django.contrib.auth.decorators import login_required
from .models import CommonCompanyDetailsModel,CommonEmployeesModel

@login_required(login_url='allifmaalusersapp:userLoginPage')
def common_shared_data(request):
    """
    The data from this view will be used in various functions in views.py.
    """
    logged_in_user=request.user
    usrslg=request.user.customurlslug
    compslg=request.user.usercompany
    usernmeslg=User.objects.filter(customurlslug=usrslg).first()
    main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
    logged_in_user_profile=CommonEmployeesModel.objects.filter(username=logged_in_user,company=main_sbscrbr_entity).first()
    logged_user_division=None
    
    logged_user_branch=None
    logged_user_department=None
    logged_user_operation_year=None
    logged_user_operation_term=None
    
    logged_user_profile_staffslg=None
    if logged_in_user_profile:
        logged_user_division=logged_in_user_profile.division
        logged_user_branch=logged_in_user_profile.branch
        logged_user_department=logged_in_user_profile.department
        logged_user_profile_staffslg=logged_in_user_profile.stffslug
        
        logged_user_operation_year=logged_in_user_profile.operation_year
        logged_user_operation_term=logged_in_user_profile.operation_term
    
    else:
        pass
      
    logged_in_user_has_universal_access=request.user.universal_access
    logged_in_user_has_divisional_access=request.user.divisional_access
    logged_in_user_has_branches_access=request.user.branches_access
    logged_in_user_has_departmental_access=request.user.departmental_access

    logged_in_user_has_universal_delete=request.user.universal_delete
    logged_in_user_has_divisional_delete=request.user.divisional_delete
    logged_in_user_has_branches_delete=request.user.branches_delete
    logged_in_user_has_departmental_delete=request.user.departmental_delete
    
    return {
        "usrslg":usrslg,
        "main_sbscrbr_entity":main_sbscrbr_entity,
        "usernmeslg":usernmeslg,
        "compslg":compslg,
       
        "logged_in_user_profile":logged_in_user_profile,
        "logged_in_user":logged_in_user,
        "logged_in_user_profile":logged_in_user_profile,
        "logged_user_division":logged_user_division,
        "logged_user_branch":logged_user_branch,
        "logged_user_department":logged_user_department,
        "logged_in_user_has_universal_access":logged_in_user_has_universal_access,
        "logged_in_user_has_divisional_access":logged_in_user_has_divisional_access,
        "logged_in_user_has_branches_access":logged_in_user_has_branches_access,
        "logged_in_user_has_departmental_access":logged_in_user_has_departmental_access,
        "logged_in_user_has_universal_delete":logged_in_user_has_universal_delete,
        "logged_in_user_has_divisional_delete":logged_in_user_has_divisional_delete,
        "logged_in_user_has_branches_delete":logged_in_user_has_branches_delete,
        "logged_in_user_has_departmental_delete":logged_in_user_has_departmental_delete,
        "logged_user_profile_staffslg":logged_user_profile_staffslg,
        "logged_user_operation_year":logged_user_operation_year,
        "logged_user_operation_term":logged_user_operation_term,
        
        #"usrslg": request.user.username if request.user.is_authenticated else "anonymous", 
    }

