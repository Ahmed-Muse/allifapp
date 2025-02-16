from django.shortcuts import render,redirect
from allifmaalusersapp.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required 
from allifmaalcommonapp.models import *
from allifmaalcommonapp.decorators import allifmaal_admin, unauthenticated_user,allowed_users,logged_in_user_is_owner_ceo,logged_in_user_can_add_view_edit_delete,logged_in_user_can_add,logged_in_user_can_view,logged_in_user_can_edit,logged_in_user_can_delete,logged_in_user_is_admin
# Create your views here.

#@allifmaal_admin
def adminappHome(request,*allifargs,**allifkwargs):
    try:
        title="System Control Center"
        context={"title":title,}
        return render(request,"allifmaaladminapp/home/home.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
    

def adminappUsers(request,*allifargs,**allifkwargs):
    try:
        title="Registered SystemUsers "
        
        users=User.objects.all()
        context={
            "title":title,
            
            "users":users,

        }
        return render(request,"allifmaaladminapp/users/users.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)



def adminappUserDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="User Details"
        allifquery=User.objects.filter(id=pk).first()
       
        allifqueryset=CommonEmployeesModel.objects.filter(username=allifquery).first()
        candoall=allifquery.can_do_all
        canadd=allifquery.can_add
        canview=allifquery.can_view
        canedit=allifquery.can_edit
        candelete=allifquery.can_delete
        usr_can_access_all=allifquery.can_access_all
        usr_can_access_related=allifquery.can_access_related
        if allifqueryset!=None:
            candoallprofile=""
            canaddprofile=""
            canviewprofile=""
            caneditprofile=""
            candeleteprofile=""
        else:
            context={
                "allifquery":allifquery,
            }
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
           
        context={
            "allifquery":allifquery,
            "allifqueryset":allifqueryset,
            "title":title,
            "candoall":candoall,
            "canadd":canadd,
            "canview":canview,
            "canedit":canedit,
            "candelete":candelete,
            "usr_can_access_all":usr_can_access_all,
            "usr_can_access_related":usr_can_access_related,

            "candoallprofile":candoallprofile,
            "canaddprofile":canaddprofile,
            "canviewprofile":canviewprofile,
            "caneditprofile":caneditprofile,
            "candeleteprofile":candeleteprofile,

        }
        return render(request,'allifmaaladminapp/users/user-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

def adminappCustomers(request):
    context={

    }
    return render(request,"allifmaaladminapp/home.html",context)
def adminappSuppliers(request):
    context={

    }
    return render(request,"allifmaaladminapp/home.html",context)
def adminappInvoices(request):
    context={

    }
    return render(request,"allifmaaladminapp/home.html",context)


def adminCustomerContacts(request,*allifargs,**allifkwargs):
    try:
        title="Contacts From Website Form"
        allifqueryset=CommonContactsModel.objects.all()
        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,"allifmaaladminapp/contacts/contacts.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)


def adminCustomerContactDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Website Contact Details"
        allifquery=CommonContactsModel.objects.filter(id=pk).first()
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,"allifmaaladminapp/contacts/contact-details.html",context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
#@allowed_users(allowed_roles=['admin'])  
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def adminDeleteCustomerContact(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonContactsModel.objects.get(id=pk).delete()
        return redirect('allifmaaladminapp:adminCustomerContacts',allifusr=usrslg,allifslug=compslg)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)