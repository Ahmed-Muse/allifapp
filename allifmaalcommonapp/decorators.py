from django.shortcuts import render,redirect,HttpResponse
from .allifutils import common_shared_data
from django.contrib.auth.decorators import login_required
from .models import CommonCompanyDetailsModel,CommonApproversModel
from allifmaalusersapp.models import User
def allifmaal_admin_supperuser(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        if usernme.is_superuser==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func

def allifmaal_admin(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        if usernme.allifmaal_admin==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func


def logged_in_user_can_add_view_edit_delete(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_can_do_all=usernme.can_do_all
        if usr_can_do_all==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func

def logged_in_user_can_add(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_can_add=usernme.can_add
        if usr_can_add==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func

def logged_in_user_can_view(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_can_view=usernme.can_view
        global ahmed
        ahmed="ahmed"
        if usr_can_view==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func

def logged_in_user_can_edit(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_can_edit=usernme.can_edit
        if usr_can_edit==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func

def logged_in_user_can_delete(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_can_delete=usernme.can_delete
        if usr_can_delete==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func

def logged_in_user_is_admin(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        if usernme.user_category=="admin":
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func
def logged_in_user_is_owner_ceo(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        if usernme.user_category=="owner" or usernme.user_category=="ceo":
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func
def logged_in_user_is_staff(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        if usernme.user_category=="staff":
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func
def logged_in_user_is_director(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        if usernme.user_category=="director":
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func
def logged_in_user_is_general_manager(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        if usernme.user_category=="genmanager":
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func


################### ACCESS LEVELS ########
def logged_in_user_has_universal_delete(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_has_univeral_delete=usernme.universal_delete
        if usr_has_univeral_delete==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func
def logged_in_user_has_divisional_delete(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_has_divisional_delete=usernme.divisional_delete
        if usr_has_divisional_delete==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func
def logged_in_user_has_branches_delete(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_has_branches_delete=usernme.branches_delete
        if usr_has_branches_delete==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func
def logged_in_user_has_departmental_delete(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_has_departmental_delete=usernme.departmental_delete
        if usr_has_departmental_delete==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func

############# ACESS LEVELS ##################3
def logged_in_user_has_universal_access(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_has_universal_access=usernme.universal_access
        if usr_has_universal_access==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func

def logged_in_user_has_divisional_access(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_has_divisional_access=usernme.divisional_access
        if usr_has_divisional_access==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func
def logged_in_user_has_branches_access(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_has_branches_access=usernme.branches_access
        if usr_has_branches_access==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func
def logged_in_user_has_departmental_access(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_has_departmental_access=usernme.departmental_access
        if usr_has_departmental_access==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func


def logged_in_user_must_have_profile(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        allif_data=common_shared_data(request)
        context={"allifquery":request.user,}
        if request.user.is_authenticated:
            if allif_data.get("logged_in_user_profile"):
                return allif_param_func(request,*args,**kwargs)
            else:
                return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        else:
            return redirect('allifmaalusersapp:userLoginPage')
    return allif_wrapper_func

def logged_in_user_can_approve(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        allif_data=common_shared_data(request)
        if request.user.is_authenticated:
            if CommonApproversModel.objects.filter(approvers=allif_data.get("logged_in_user_profile")).exists():
                return allif_param_func(request,*args,**kwargs)
            else:
                return render(request,'allifmaalcommonapp/permissions/no_permission.html')
               
        else:
            return redirect('allifmaalusersapp:userLoginPage')
    return allif_wrapper_func

def subscriber_company_status(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        try:
            allif_data=common_shared_data(request)
            context={"allifquery":request.user,}
            compslg=request.user.usercompany
            main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
            if main_sbscrbr_entity is None:
                return redirect('allifmaalusersapp:userLogoutPage')
            else:
                subs_status=main_sbscrbr_entity.status
                if request.user.is_authenticated:
                    if subs_status=="Unblocked":
                        return allif_param_func(request,*args,**kwargs)
                    else:
                        return render(request,'allifmaalcommonapp/permissions/entity_blocked.html',context)
                else:
                    return redirect('allifmaalusersapp:userLoginPage')
        except Exception as ex:
            error_context={'error_message': ex,}
            return render(request,'allifmaalcommonapp/error/error.html',error_context)
    return allif_wrapper_func

#########################################################################################3
def unauthenticated_user(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        user_var=request.user.usercompany
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
            user_var=request.user.usercompany
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
            user_var=request.user.usercompany
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

       