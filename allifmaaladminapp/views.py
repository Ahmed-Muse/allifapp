from django.shortcuts import render,redirect,HttpResponse
from allifmaalusersapp.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required 
from allifmaalcommonapp.models import *
from allifmaalcommonapp.decorators import allifmaal_admin, unauthenticated_user,allowed_users,logged_in_user_is_owner_ceo,logged_in_user_can_add_view_edit_delete,logged_in_user_can_add,logged_in_user_can_view,logged_in_user_can_edit,logged_in_user_can_delete,logged_in_user_is_admin
# Create your views here.
from allifmaalcommonapp.forms import CommonAddSectorForm

#@allifmaal_admin
def adminappHome(request,*allifargs,**allifkwargs):
    try:
        num_visits = request.session.get('num_visits', 0)
        num_visits += 1
        request.session['num_visits'] = num_visits
        title="System Control Center"
        context={"title":title,
                 "num_visits":num_visits,}
        return render(request,"allifmaaladminapp/home/home.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
    

def adminappUsers(request,*allifargs,**allifkwargs):
    try:
        title="Registered SystemUsers "
        
        allifqueryset=User.objects.all()
        context={
            "title":title,
            
            "allifqueryset":allifqueryset,

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
        #else:
            #context={
                #"allifquery":allifquery,
            #}
            #return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        else:
            context={
                "allifquery":allifquery,
            }
            return render(request,'allifmaaladminapp/users/user-details.html',context)
           
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
    

@login_required(login_url='allifmaalusersapp:userLoginPage')
def adminBlockUnblockEntity(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonCompanyDetailsModel.objects.filter(id=pk).first()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        if allifquery.status=="Blocked":
                allifquery.status="Unblocked"
        else:
            allifquery.status="Blocked"
            
        allifquery.save()
      
       
        return redirect('allifmaalcommonapp:commonCompanies',allifusr=usrslg,allifslug=user_var)
       
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    


##########################################################33

def ui1(request,*allifargs,**allifkwargs):
    print()
    context = {
           
        }
    return render(request,'allifmaaladminapp/ui/ui1.html',context)
def ui2(request,*allifargs,**allifkwargs):
    print()
    context ={
           
        }
    return render(request,'allifmaaladminapp/ui/ui2.html',context)
def ui3(request,*allifargs,**allifkwargs):
    print()
    context = {
           
        }
    return render(request,'allifmaaladminapp/ui/ui3.html',context)
def ui4(request,*allifargs,**allifkwargs):
    print()
    context = {
           
        }
    return render(request,'allifmaaladminapp/ui/ui4.html',context)

def ui6(request,*allifargs,**allifkwargs):
    print()
    context ={

        }
    return render(request,'allifmaaladminapp/ui/ui6.html',context)
def ui7(request,*allifargs,**allifkwargs):
    print()
    context = {
           
        }
    return render(request,'allifmaaladminapp/ui/ui7.html',context)
def ui8(request,*allifargs,**allifkwargs):
    print()
    context = {
           
        }
    return render(request,'allifmaaladminapp/ui/ui8.html',context)

#################### testingl inks

@register.filter(name='allif_generate_links')
def generate_new_link(link):
    url = reverse(link.url_name, kwargs=link.url_params)
    return f'<a href="{url}">{link.name}</a>'

def dynamic_form_view(request):
    if request.method == 'POST':
        names = request.POST.getlist('name[]')
        notes = request.POST.getlist('notes[]')

        forms = []
        for i in range(len(names)):
            data = {
                'name': names[i],
                'notes': notes[i],
            }
            form =CommonAddSectorForm(data)
            forms.append(form)

        valid = True
        for form in forms:
            if not form.is_valid():
                valid = False
                break

        if valid:
            for form in forms:
                sector_name = form.cleaned_data['name']
                sector_notes = form.cleaned_data['notes']
                # Create and save sector objects
                sector = CommonSectorsModel(name=sector_name, notes=sector_notes)
                sector.save()
            return HttpResponse("Sectors added successfully!")
        else:
            return HttpResponse("Form has errors.")

    return render(request, 'allifmaaladminapp/explore/dynamic_form.html')

from .models import Product

def product_list(request):
    products = Product.objects.all()
    context = {'table_data': products}
    return render(request, 'allifmaaladminapp/product_list.html', context)