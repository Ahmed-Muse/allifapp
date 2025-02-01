from django.shortcuts import render,redirect
from .models import CommonCompanyDetailsModel,CommonEmployeesModel,User
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
        usr_can_view=usernme.can_add
        if usr_can_view==True:
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
        usr_can_view=usernme.can_edit
        if usr_can_view==True:
            return allif_param_func(request,*args,**kwargs)
        else:
            return render(request,'allifmaalcommonapp/permissions/no_permission.html')
    return allif_wrapper_func

def logged_in_user_can_delete(allif_param_func):
    def allif_wrapper_func(request,*args,**kwargs):
        usernme=request.user
        usr_can_view=usernme.can_delete
        if usr_can_view==True:
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

                  
