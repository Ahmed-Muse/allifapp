from django.shortcuts import render,redirect,get_object_or_404
from.models import *
from datetime import date
from django.core.mail import send_mail
from .allifutils import common_shared_data
from django.db import IntegrityError, transaction # Import transaction for atomicity

# --- Import the default data lists ---
import logging
logger=logging.getLogger(__name__)
from .defaults_data import (
    DEFAULT_COMPANY_SCOPES, DEFAULT_TAXES, DEFAULT_CURRENCIES,
    DEFAULT_PAYMENT_TERMS, DEFAULT_UNITS_OF_MEASURE,
    DEFAULT_OPERATION_YEARS, DEFAULT_OPERATION_YEAR_TERMS,
    DEFAULT_CODES, DEFAULT_CATEGORIES,
    DEFAULT_GL_ACCOUNT_CATEGORIES, DEFAULT_CHART_OF_ACCOUNTS
)


from twilio.rest import Client
from.forms import *
from .decorators import logged_in_user_can_approve, subscriber_company_status, logged_in_user_must_have_profile,logged_in_user_has_universal_delete,logged_in_user_has_divisional_delete,logged_in_user_has_branches_delete,logged_in_user_has_departmental_delete,logged_in_user_has_universal_access,logged_in_user_has_divisional_access,logged_in_user_has_branches_access,logged_in_user_has_departmental_access,allifmaal_admin,allifmaal_admin_supperuser, unauthenticated_user,allowed_users,logged_in_user_is_owner_ceo,logged_in_user_can_add_view_edit_delete,logged_in_user_can_add,logged_in_user_can_view,logged_in_user_can_edit,logged_in_user_can_delete,logged_in_user_is_admin
from django.utils import timezone
from django.core.serializers import serialize
import json
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allifmaalusersapp.forms import CreateNewCustomUserForm
from django.http.response import HttpResponse, JsonResponse

from allifmaalusersapp.forms import UpdateCustomUserForm
from django.template.loader import get_template
from django.db.models import Q
from xhtml2pdf import pisa
from django.utils import timezone
from decimal import Decimal
from django.db.models import Count,Min,Max,Avg,Sum

from .resources import *
def commonWebsite(request):
    try:
        title="Allifmaal ERP"
        context={"title":title}
        return render(request,'allifmaalcommonapp/website/website.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/web-error.html',error_context)

def commonEngineering(request):
    try:
        title="Allifmaal Engineering"
        context={"title":title,}
        return render(request,'allifmaalcommonapp/website/engineering.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/web-error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
def CommonDecisionPoint(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("main_sbscrbr_entity") is None or '' or allif_data.get("compslg") is None or '':#means that the logged user did not create a company and does not belong to any company
            return redirect('allifmaalcommonapp:commonAddnewEntity',allifusr=allif_data.get("logged_in_user"))
        elif allif_data.get("compslg") and str(allif_data.get("main_sbscrbr_entity"))!=None:
            if str(allif_data.get("main_sbscrbr_entity").sector)=="Sales":
                return redirect('allifmaalsalesapp:salesHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Healthcare":
                return redirect('allifmaalshaafiapp:shaafiHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Hospitality":
                return redirect('allifmaalhotelsapp:hotelsHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Education":
                return redirect('allifmaalilmapp:ilmHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Services":
                return redirect('allifmaalservicesapp:servicesHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Realestate":
                return redirect('allifmaalrealestateapp:realestateHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Logistics":
                return redirect('allifmaallogisticsapp:logisticsHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                return HttpResponse("Sorry, Your company must belong to a sector")
        else:
            return render(request,'allifmaalcommonapp/error/error.html')
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
#@subscriber_company_status
def commonHome(request,*allifargs,**allifkwargs):
    try:
        if request.user.email.endswith("info@allifmaal.com"):#just for remembering purposes
            pass
        allif_data=common_shared_data(request)
        if allif_data.get("main_sbscrbr_entity")!=None:
            if str(allif_data.get("main_sbscrbr_entity").sector)=="Salest":
                return redirect('allifmaalsalesapp:salesHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Healthcare":
                return redirect('allifmaalshaafiapp:shaafiHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Hospitality":
                return redirect('allifmaalhotelsapp:hotelsHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Education":
                return redirect('allifmaalilmapp:ilmHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Services":
                return redirect('allifmaalservicesapp:servicesHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Realestate":
                return redirect('allifmaalrealestateapp:realestateHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Logistics":
                return redirect('allifmaallogisticsapp:logisticsHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                return redirect('allifmaalcommonapp:CommonDecisionPoint')
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
def commonSpecificDashboard(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("main_sbscrbr_entity")!=None:
            if str(allif_data.get("main_sbscrbr_entity").sector)=="Sales":
                return redirect('allifmaalsalesapp:salesDashboard',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Healthcare":
                return redirect('allifmaalshaafiapp:shaafiDashboard',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Hospitality":
                return redirect('allifmaalhotelsapp:hospitalityDashboard',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Education":
                return redirect('allifmaalilmapp:ilmDashboard',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Services":
                return redirect('allifmaalservicesapp:servicesDashboard',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Realestate":
                return redirect('allifmaalrealestateapp:realestateDashboard',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            elif str(allif_data.get("main_sbscrbr_entity").sector)=="Logistics":
                return redirect('allifmaallogisticsapp:logisticsDashboard',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                return redirect('allifmaalcommonapp:CommonDecisionPoint')
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

################################### Sectors ############################### 

@logged_in_user_must_have_profile
@allifmaal_admin
def commonSectors(request,allifusr,*allifargs,**allifkwargs):
    title="Main Sectors"
    try:
        allif_data=common_shared_data(request) # call the common function to get access to its variables.
        allifqueryset=CommonSectorsModel.objects.all()
        form=CommonAddSectorForm()
        if request.method=='POST':
            form=CommonAddSectorForm(request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("logged_in_user")
                obj.save()
                return redirect('allifmaalcommonapp:commonSectors',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSectorForm()
        context={
            "title":title,
            "form":form,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/sectors/sectors.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,"title":title,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@allifmaal_admin
def commonSectorDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Sector Details"
        allifquery=CommonSectorsModel.objects.filter(id=pk).first()
        allifqueryset=CommonCompanyDetailsModel.objects.filter(sector=allifquery)
        context={
            "allifquery":allifquery,
            "allifqueryset":allifqueryset,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/sectors/sector-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,"title":title,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@allifmaal_admin
def commonEditSector(request,pk,*allifargs,**allifkwargs):
    title="Update Sector Details"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonSectorsModel.objects.all()
        update_allifquery=CommonSectorsModel.objects.get(id=pk)
        form =CommonAddSectorForm(instance=update_allifquery)
        if request.method=='POST':
            form =CommonAddSectorForm(request.POST, instance=update_allifquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("logged_in_user")
                obj.save()
                return redirect('allifmaalcommonapp:commonSectors',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                form =CommonAddSectorForm(instance=update_allifquery)
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,"form":form,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form =CommonAddSectorForm(instance=update_allifquery)
        context = {
            'form':form,
            "update_allifquery":update_allifquery,
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/sectors/sectors.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,"title":title,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@allifmaal_admin
@logged_in_user_can_delete
def commonWantToDeleteSector(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonSectorsModel.objects.filter(id=pk).first()
        title="Are sure to delete?"
        context={
        "title":title,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/sectors/x-sector-confirm.html',context)
    except Exception as ex:
        error_context={'error_message': ex,"title":title,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
     
@logged_in_user_must_have_profile
@allifmaal_admin
@logged_in_user_can_delete  
def commonSectorDelete(request,pk):
    try:
        allif_data=common_shared_data(request)
        CommonSectorsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonSectors',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

################################### Sectors ############################### 
@logged_in_user_must_have_profile
@allifmaal_admin
def commonLoadContentTest(request):
    try:
        title="Main Sectors"
        context = {
            "title":title,
        }
        return render(request,'allifmaalcommonapp/sectors/sectors-list.html',context)
    except Exception as ex:
        error_context={'error_message': ex,"title":title,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
################################### Sectors ############################### 
@logged_in_user_must_have_profile
@allifmaal_admin
@logged_in_user_can_view
def commonDocsFormat(request,*allifargs,**allifkwargs):
    title="Formats"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonDocsFormatModel.objects.all()
        form=CommonAddDocFormatForm()
        if request.method == 'POST':
            form=CommonAddDocFormatForm(request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("logged_in_user")
                obj.save()
                return redirect('allifmaalcommonapp:commonDocsFormat',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        context = {
            "title":title,
            "form":form,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/docformats/docformats.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,'title':title,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@allifmaal_admin
@logged_in_user_can_edit
def commonEditDocsFormat(request,pk,*allifargs,**allifkwargs):
    title="Update Format"
    try:
        allif_data=common_shared_data(request)
        update=CommonDocsFormatModel.objects.get(id=pk)
        form =CommonAddDocFormatForm(instance=update)
        if request.method == 'POST':
            form =CommonAddDocFormatForm(request.POST, instance=update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("logged_in_user")
                obj.save()
                return redirect('allifmaalcommonapp:commonDocsFormat',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form =CommonAddSectorForm(instance=update)
        context = {
            'form':form,
            "update":update,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/docformats/docformats.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@allifmaal_admin 
@logged_in_user_can_delete
def commonDeleteDocsFormat(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonDocsFormatModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonDocsFormat',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

################################### Sectors ############################### 
@logged_in_user_must_have_profile
@allifmaal_admin
@logged_in_user_can_view
def commonDataSorts(request,*allifargs,**allifkwargs):
    title="Main Filters"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonDataSortsModel.objects.all()
        form=CommonAddDataSortsForm()
        if request.method == 'POST':
            form=CommonAddDataSortsForm(request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner =allif_data.get("logged_in_user")
                obj.save()
                return redirect('allifmaalcommonapp:commonDataSorts',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddDataSortsForm()
        context = {
            "title":title,
            "form":form,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/filters/filters.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@allifmaal_admin
@logged_in_user_can_edit
def commonEditDataSort(request,pk,*allifargs,**allifkwargs):
    title="Update Filter Details"
    try:
        allif_data=common_shared_data(request)
        update=CommonDataSortsModel.objects.get(id=pk)
        form =CommonAddDataSortsForm(instance=update)
        if request.method == 'POST':
            form =CommonAddDataSortsForm(request.POST, instance=update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("logged_in_user")
                obj.save()
                return redirect('allifmaalcommonapp:commonDataSorts',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form =CommonAddDataSortsForm(instance=update)
        context = {
            'form':form,
            "update":update,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/filters/filters.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@allifmaal_admin  
@logged_in_user_can_delete
def commonDeleteDataSort(request,pk):
    try:
        allif_data=common_shared_data(request)
        CommonDataSortsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonDataSorts',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


########################3 currencies ######################

@logged_in_user_must_have_profile
@logged_in_user_can_view
def commonCurrencies(request,*allifargs,**allifkwargs):
    title="Currencies"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonCurrenciesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/currencies/currencies.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddCurrency(request,*allifargs,**allifkwargs):
    try:
        title="Add New Currency"
        allif_data=common_shared_data(request)
        form=CommonAddCurrencyForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddCurrencyForm(allif_data.get("main_sbscrbr_entity"),request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonCurrencies',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddCurrencyForm(allif_data.get("main_sbscrbr_entity"))

        context={
            "form":form,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/currencies/add_currency.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_edit
def commonEditCurrency(request,pk,*allifargs,**allifkwargs):
    title="Update Currency Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonCurrenciesModel.objects.filter(id=pk).first()
        form=CommonAddCurrencyForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddCurrencyForm(allif_data.get("main_sbscrbr_entity"),request.POST, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonCurrencies',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddCurrencyForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context = {
            'form':form,
            "allifquery_update":allifquery_update,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/currencies/add_currency.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile 
@logged_in_user_can_delete
def commonDeleteCurrency(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonCurrenciesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonCurrencies',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    


########################3 Payment terms ######################

@logged_in_user_must_have_profile
@logged_in_user_can_view
def commonPaymentTerms(request,*allifargs,**allifkwargs):
    title="Payment Terms"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonPaymentTermsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/payments/terms/payment_terms.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddPaymentTerm(request,*allifargs,**allifkwargs):
    try:
        title="Add New Payment Terms"
        allif_data=common_shared_data(request)
        form=CommonAddPaymentTermForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddPaymentTermForm(allif_data.get("main_sbscrbr_entity"),request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonPaymentTerms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddPaymentTermForm(allif_data.get("main_sbscrbr_entity"))

        context={
            "form":form,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/payments/terms/add_payment_term.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_edit
def commonEditPaymentTerm(request,pk,*allifargs,**allifkwargs):
    title="Update Payment Term Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonPaymentTermsModel.objects.filter(id=pk).first()
        form=CommonAddPaymentTermForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddPaymentTermForm(allif_data.get("main_sbscrbr_entity"),request.POST, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonPaymentTerms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddPaymentTermForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context = {
            'form':form,
            "allifquery_update":allifquery_update,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/currencies/add_currency.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile  
@logged_in_user_can_delete
def commonDeletePaymentTerm(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonPaymentTermsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonPaymentTerms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


############################ units of measure section #########

@logged_in_user_must_have_profile
@logged_in_user_can_view
def commonUnits(request,*allifargs,**allifkwargs):
    title="Units of Measure"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonUnitsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/units/units.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddUnit(request,*allifargs,**allifkwargs):
    try:
        title="Add New Unit of Measure"
        allif_data=common_shared_data(request)
        form=CommonAddUnitForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddUnitForm(allif_data.get("main_sbscrbr_entity"),request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonUnits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddUnitForm(allif_data.get("main_sbscrbr_entity"))

        context={
            "form":form,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/units/add_unit.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_edit
def commonEditUnit(request,pk,*allifargs,**allifkwargs):
    title="Update Unit of Measure Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonUnitsModel.objects.filter(id=pk).first()
        form=CommonAddUnitForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddUnitForm(allif_data.get("main_sbscrbr_entity"),request.POST, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonUnits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddUnitForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context = {
            'form':form,
            "allifquery_update":allifquery_update,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/units/add_unit.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile  
@logged_in_user_can_delete
def commonDeleteUnit(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonUnitsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonUnits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#######################3 OPERATION YEAR ####################################3

@logged_in_user_must_have_profile
@logged_in_user_can_view
def commonOperationYears(request,*allifargs,**allifkwargs):
    title="Operation Years"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonOperationYearsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/operations/years/operation_years.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddOperationYear(request,*allifargs,**allifkwargs):
    try:
        title="Add New Operation Year"
        allif_data=common_shared_data(request)
        form=CommonAddOperationYearForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddOperationYearForm(allif_data.get("main_sbscrbr_entity"),request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonOperationYears',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddOperationYearForm(allif_data.get("main_sbscrbr_entity"))

        context={
            "form":form,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/operations/years/add_year.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_edit
def commonEditOperationYear(request,pk,*allifargs,**allifkwargs):
    title="Edit The Operation Year Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonOperationYearsModel.objects.filter(id=pk).first()
        form=CommonAddOperationYearForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddOperationYearForm(allif_data.get("main_sbscrbr_entity"),request.POST, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonOperationYears',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddOperationYearForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context = {
            'form':form,
            "allifquery_update":allifquery_update,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/operations/years/add_year.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile  
@logged_in_user_can_delete
def commonDeleteOperationYear(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonOperationYearsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonOperationYears',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
    
#######################3 OPERATION YEAR Terms ####################################3

@logged_in_user_must_have_profile
@logged_in_user_can_view
def commonOperationYearTerms(request,*allifargs,**allifkwargs):
    title="Operation Year Terms"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonOperationYearTermsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/operations/years/terms/terms.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddOperationYearTerm(request,*allifargs,**allifkwargs):
    try:
        title="Add New Operation Year Term"
        allif_data=common_shared_data(request)
        form=CommonAddOperationYearTermForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddOperationYearTermForm(allif_data.get("main_sbscrbr_entity"),request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonOperationYearTerms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddOperationYearTermForm(allif_data.get("main_sbscrbr_entity"))

        context={
            "form":form,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/operations/years/terms/add_term.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_edit
def commonEditOperationYearTerm(request,pk,*allifargs,**allifkwargs):
    title="Edit The Operation Year Term Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonOperationYearTermsModel.objects.filter(id=pk).first()
        form=CommonAddOperationYearTermForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddOperationYearTermForm(allif_data.get("main_sbscrbr_entity"),request.POST, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonOperationYearTerms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddOperationYearTermForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context = {
            'form':form,
            "allifquery_update":allifquery_update,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/operations/years/terms/add_term.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile  
@logged_in_user_can_delete
def commonDeleteOperationYearTerm(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonOperationYearTermsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonOperationYearTerms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

    

   
########################################33 stock ####################3
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCategories(request,*allifargs,**allifkwargs):
    try:
        title="Main Categories"
        allif_data=common_shared_data(request)
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonCategoriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonCategoriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonCategoriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonCategoriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/operations/categories/categories.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddCategory(request,*allifargs,**allifkwargs):
    try:
       
        title="Category Registration"
        allif_data=common_shared_data(request)
        form=CommonCategoryAddForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonCategoryAddForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonCategories',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonCategoryAddForm(allif_data.get("main_sbscrbr_entity"))

        context={
            "form":form,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/operations/categories/add-category.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonEditCategory(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Category Details"
        allif_data=common_shared_data(request)
        allifquery_update=CommonCategoriesModel.objects.filter(id=pk).first()
        form=CommonCategoryAddForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonCategoryAddForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonCategories',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonCategoryAddForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)

        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/operations/categories/add-category.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCategorySearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonCategoriesModel.objects.filter((Q(description__icontains=allifsearch)|Q(name__icontains=allifsearch)|Q(code__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        
        else:
            searched_data=[]

        context={
        "title":title,
       
        "searched_data":searched_data,
        
           
        }
        return render(request,'allifmaalcommonapp/operations/categories/categories.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteCategory(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonCategoriesModel.objects.filter(id=pk).first()
        message="Are u sure to delete"
        context={
        "message":message,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/operations/categories/x-category-cnfrm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin  
@logged_in_user_has_departmental_delete
def commonDeleteCategory(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonCategoriesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonCategories',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCategoryDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonCategoriesModel.objects.filter(id=pk).first()
        title=allifquery
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/operations/categories/category-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
    
#############################3 CODES #########################3

   
########################################33 stock ####################3
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCodes(request,*allifargs,**allifkwargs):
    try:
        title="Main Codes"
        allif_data=common_shared_data(request)
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonCodesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonCodesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonCodesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonCodesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/operations/codes/codes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddCode(request,*allifargs,**allifkwargs):
    try:
       
        title="Code Registration"
        allif_data=common_shared_data(request)
        form=CommonAddCodeForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddCodeForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonCodes',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddCodeForm(allif_data.get("main_sbscrbr_entity"))

        context={
            "form":form,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/operations/codes/add_code.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonEditCode(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Code Details"
        allif_data=common_shared_data(request)
        allifquery_update=CommonCodesModel.objects.filter(id=pk).first()
        form=CommonAddCodeForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddCodeForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonCodes',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonCategoryAddForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)

        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/operations/codes/add_code.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCodeSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonCodesModel.objects.filter((Q(description__icontains=allifsearch)|Q(name__icontains=allifsearch)|Q(code__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        
        else:
            searched_data=[]

        context={
        "title":title,
       
        "searched_data":searched_data,
        
           
        }
        return render(request,'allifmaalcommonapp/operations/codes/codes.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteCode(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonCategoriesModel.objects.filter(id=pk).first()
        message="Are u sure to delete"
        context={
        "message":message,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/operations/codes/delet_code_confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin  
@logged_in_user_has_departmental_delete
def commonDeleteCode(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonCodesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonCodes',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCodeDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonCodesModel.objects.filter(id=pk).first()
        title=allifquery
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/operations/codes/code_details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
############################### .......Entities and companies details........... #########################3#
@logged_in_user_must_have_profile
#@allifmaal_admin
def commonCompanies(request,*allifargs,**allifkwargs):
    title="Registered Companies"
    try:
        allifqueryset=CommonCompanyDetailsModel.objects.all()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                allifqueryset=CommonCompanyDetailsModel.objects.all().order_by("company")
            else:
                allifqueryset=CommonCompanyDetailsModel.objects.all().order_by("-company")
        else:
            allifqueryset=CommonCompanyDetailsModel.objects.all()
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request,'allifmaalcommonapp/companies/companies.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
# dont add pre-conditions here like the requirement for the profiles
@login_required(login_url='allifmaalusersapp:userLoginPage') 
def commonAddnewEntity(request,allifusr,*allifargs,**allifkwargs):
    title="Entity Registration"
    try:
        usrslg=request.user.customurlslug
        usernmeslg=User.objects.filter(customurlslug=usrslg).first()
        user_var_comp=request.user.usercompany
        # create divisions, branches and department when the company is created to have profile for the new user....
        main_division="Main Division"
        main_division="Main Division"
        main_branch="Main Branch"
        main_department="Main Department"
        allif_data=common_shared_data(request)
        form=CommonAddCompanyDetailsForm(request.POST, request.FILES)
        if request.method=='POST':
            form=CommonAddCompanyDetailsForm(request.POST,request.FILES)
            if form.is_valid():
                sector=int(request.POST.get('sector'))
                name=request.POST.get('company')
                address=request.POST.get('address')
                if CommonCompanyDetailsModel.objects.filter(company=name).exists():
                    messages.info(request,'Sorry! A company with similar name exists. Please Choose another name.')
                    return redirect('allifmaalcommonapp:commonAddnewEntity',allifusr=allif_data.get("logged_in_user"))
                else:
                    if name and sector!="":
                        sectorselec=CommonSectorsModel.objects.filter(id=sector).first()
                        obj=form.save(commit=False)
                        obj.owner=usernmeslg
                         # if the legal name changes, the slug will change and the company will lose all data related to it.
                        obj.legalName=str(f'{name}+{address}')#important...used to generate company slug...dont change the legal name of the company
                        obj.save()
                        newcompny=CommonCompanyDetailsModel.objects.filter(company=obj).first()
                        #set the user division, branch and department
                        usernmeslg.usercompany=str(newcompny.companyslug)
                        main_div=str(main_division+"-"+str(newcompny))
                        main_bran=str(main_branch+"-"+str(newcompny))
                        main_dept=str(main_department+"-"+str(newcompny))
        
                        usernmeslg.userdivision=str(main_div)
                        usernmeslg.userbranch=str(main_bran)
                        usernmeslg.userdepartment=str(main_dept)

                            # since we need to create user profile next, create default division, branch and department
                        new_division=CommonDivisionsModel(division=main_div,company=newcompny).save()
                        new_branch=CommonBranchesModel(branch=main_bran,division=new_division,company=newcompny).save()
                        new_department=CommonDepartmentsModel(department=main_dept,division=new_division,branch=new_branch,company=newcompny).save()

                        # give the user all the permissions since they are the owner of this enttity
                        usernmeslg.can_do_all=True
                        usernmeslg.can_add=True
                        usernmeslg.can_edit=True
                        usernmeslg.can_view=True
                        usernmeslg.can_delete=True
                        usernmeslg.universal_delete=True
                        usernmeslg.divisional_delete=True
                        usernmeslg.branches_delete=True
                        usernmeslg.departmental_delete=True
                        usernmeslg.universal_access=True
                        usernmeslg.divisional_access=True
                        usernmeslg.branches_access=True
                        usernmeslg.departmental_access=True
                        usernmeslg.can_access_all=True
                        usernmeslg.can_access_related=True
                        usernmeslg.user_category="admin"
                        usernmeslg.save()
                        if sectorselec is not None:
                            if sectorselec.name=="Sales":
                                return redirect('allifmaalsalesapp:salesHome',allifusr=usrslg,allifslug=user_var_comp)
                            elif sectorselec.name=="Healthcare":
                                return redirect('allifmaalshaafiapp:shaafiHome',allifusr=usrslg,allifslug=user_var_comp)
                            elif sectorselec.name=="Hospitality":
                                return redirect('allifmaalhotelsapp:hotelsHome',allifusr=usrslg,allifslug=user_var_comp)
                            elif sectorselec.name=="Education":
                                return redirect('allifmaalilmapp:ilmHome',allifusr=usrslg,allifslug=user_var_comp)
                            elif sectorselec.name=="Logistics":
                                return redirect('allifmaallogisticsapp:logisticsHome',allifusr=usrslg,allifslug=user_var_comp)
                            elif sectorselec.name=="Realestate":
                                return redirect('allifmaalrealestateapp:realestateHome',allifusr=usrslg,allifslug=user_var_comp)
                            elif sectorselec.name=="Services":
                                return redirect('allifmaalservicesapp:servicesHome',allifusr=usrslg,allifslug=user_var_comp)
                            else:
                                form=CommonAddCompanyDetailsForm(request.POST, request.FILES)
                        else:
                            form=CommonAddCompanyDetailsForm(request.POST, request.FILES)
                    else:
                        form=CommonAddCompanyDetailsForm(request.POST, request.FILES)
            else:
                form=CommonAddCompanyDetailsForm(request.POST, request.FILES)
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddCompanyDetailsForm(request.POST, request.FILES)

        context={"form":form,
                 "title":title,"user_var":usernmeslg,}
        return render(request,'allifmaalcommonapp/companies/newentity.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_view
@subscriber_company_status
def commonCompanyDetailsForClients(request,*allifargs,**allifkwargs):
    title="Company Details and Settings"
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonCompanyDetailsModel.objects.filter(companyslug=allif_data.get("compslg")).first()
        scopes=CommonCompanyScopeModel.objects.filter(company=allifquery)
        context={
            "title":title,
            "allifquery":allifquery,
            "scopes":scopes,
            }
        return render(request,'allifmaalcommonapp/companies/company-details-clients.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@allifmaal_admin 
@logged_in_user_can_edit
def commonEditEntityByAllifAdmin(request,pk,*allifargs,**allifkwargs):
    title="Update Entity Details"
    try:
        allif_data=common_shared_data(request)
        user_var_update=CommonCompanyDetailsModel.objects.filter(id=pk).first()
        form=CommonEditCompanyDetailsFormByAllifAdmin(instance=user_var_update)
        if request.method=='POST':
            form=CommonEditCompanyDetailsFormByAllifAdmin(request.POST or None,request.FILES, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                obj.save()
                return redirect('allifmaalcommonapp:commonCompanies',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                form=CommonEditCompanyDetailsFormByAllifAdmin(request.POST or None, instance=user_var_update)
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonEditCompanyDetailsFormByAllifAdmin(request.POST or None, instance=user_var_update)
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/companies/edit-entity.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@logged_in_user_can_edit
@logged_in_user_is_admin
def commonEditEntityByClients(request,allifpk,*allifargs,**allifkwargs):
    title="Update Entity Details"
    try:
        allif_data=common_shared_data(request)
        user_var_update=CommonCompanyDetailsModel.objects.filter(companyslug=allifpk).first()
        form=CommonAddByClientCompanyDetailsForm(instance=user_var_update)
        if request.method=='POST':
            form=CommonAddByClientCompanyDetailsForm(request.POST or None,request.FILES, instance=user_var_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("logged_in_user")
                obj.save()
                return redirect('allifmaalcommonapp:commonCompanyDetailsForClients',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                form=CommonAddByClientCompanyDetailsForm(request.POST or None, instance=user_var_update)
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddByClientCompanyDetailsForm(request.POST or None, instance=user_var_update)
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/companies/edit-entity-client.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
        
@logged_in_user_must_have_profile
@logged_in_user_can_view
@allifmaal_admin
def commonCompanyDetailsForAllifAdmin(request,pk,*allifargs,**allifkwargs):
    try:
        title="Company Details"
        allifquery=CommonCompanyDetailsModel.objects.filter(id=pk).first()
        allifqueryset=CommonCompanyScopeModel.objects.filter(company=allifquery)
        context={
            "allifquery":allifquery,
           "allifqueryset":allifqueryset,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/companies/company-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_view
@allifmaal_admin
def commonShowClickedRowCompanyDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Company Details"
        allifqueryset=CommonCompanyDetailsModel.objects.all()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        clicked_row_data=CommonCompanyDetailsModel.objects.filter(id=pk).first()
        context={
            "clicked_row_data":clicked_row_data,
            "allifqueryset":allifqueryset,
            "formats":formats,
           "datasorts":datasorts,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/companies/companies.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@logged_in_user_can_delete
@logged_in_user_is_admin 
def commonWantToDeleteCompany(request,pk,*allifargs,**allifkwargs):
    title="Are you sure to delete?"
    try:
        allifquery=CommonCompanyDetailsModel.objects.filter(id=pk).first()
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/companies/comp-delete-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
@logged_in_user_must_have_profile
@logged_in_user_can_delete
@logged_in_user_is_admin
def commonDeleteEntity(request,allifslug,*allifargs,**allifkwargs):
    title="Are you sure to delete?"
    try:
        allifquery=CommonCompanyDetailsModel.objects.filter(companyslug=allifslug).first()
        if allifquery.can_delete=="undeletable":
            context={"allifquery":allifquery,"title":title,}
            return render(request,'allifmaalcommonapp/error/cant_delete.html',context)
        else:
            allifquery.delete()
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_view
@allifmaal_admin
def commonCompanySearch(request,*allifargs,**allifkwargs):
    title="Search"
    try:
        searched_data=[]
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonCompanyDetailsModel.objects.filter(Q(company__contains=allifsearch) | Q(address__contains=allifsearch))
        else:
            searched_data=CommonCompanyDetailsModel.objects.all()
        context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
        }
        return render(request,'allifmaalcommonapp/companies/companies.html',context)
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_view
@allifmaal_admin
def commonCompanyAdvanceSearch(request,*allifargs, **allifkwargs):
    title="Companies Advanced Search"
    try:
        allif_data=common_shared_data(request)
        main_sbscrbr_entity = CommonCompanyDetailsModel.objects.filter(companyslug=allif_data.get("compslg")).first()
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity).order_by('date')[:4]
        context = {
            "title": title,
            "main_sbscrbr_entity": main_sbscrbr_entity,
            "scopes": scopes,
        }
        if request.method == 'POST':
            selected_option = request.POST.get('requiredformat')
            start_date = request.POST.get('strtdate')
            end_date = request.POST.get('enddate')
            searched_data = CommonCompanyDetailsModel.objects.all()  # Default to all if no date range
            if start_date and end_date:
                searched_data = CommonCompanyDetailsModel.objects.filter(Q(date__gte=start_date) & Q(date__lte=end_date))
                context["searched_data"] = searched_data
            else:
                context["allifqueryset"] = searched_data
            if selected_option == "pdf":
                template_path = 'allifmaalcommonapp/companies/search-pdf.html'
                template = get_template(template_path)
                html = template.render(context)
                response = HttpResponse(content_type='application/pdf')
                response = HttpResponse(content_type='application/doc')
                response['Content-Disposition'] = f'filename="Companies-Search-Results.pdf"'

                pisa_status = pisa.CreatePDF(html, dest=response)
                if pisa_status.err:
                    return HttpResponse('We had some errors <pre>' + html + '</pre>')
                return response
            else:
                context={
                    "searched_data":searched_data,
                }
                return render(request, 'allifmaalcommonapp/companies/companies.html', context)

        else:
            context["allifqueryset"] = CommonCompanyDetailsModel.objects.all()
            return render(request, 'allifmaalcommonapp/companies/companies.html', context)

    except Exception as ex:
        error_context = {'error_message': ex}
        return render(request, 'allifmaalcommonapp/error/error.html', error_context)

############################ Creating default values #####################....

@logged_in_user_must_have_profile
@logged_in_user_can_delete
@logged_in_user_is_admin 
def commonDefaultValues(request,*allifargs,**allifkwargs):
    try:
        title="Default Values"
        
        context={
       
        "title":title,
        }
        return render(request,'allifmaalcommonapp/operations/defaults/defaults.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   

# dont add pre-conditions here like the requirement for the profiles
@login_required(login_url='allifmaalusersapp:userLoginPage') 
def commonAdminCreateDefaultValues(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
    
        doc_formats=[
            {'name': 'pdf', 'notes': 'document formats'},
           
            ]
        data_sorts=[
            {'name': 'ascending', 'notes': 'data sort format'},
            {'name': 'descending', 'notes': 'data sort format'},
            ]
        # --- END MODIFIED PART ---
        
        current_owner = allif_data.get("usernmeslg")
        current_date=timezone.now().date()
    
        # Use a transaction to ensure all or none are saved cleanly
        with transaction.atomic():
            for data in doc_formats:
                if data['name'] not in CommonDocsFormatModel.objects.filter(name=data['name']):
                    CommonDocsFormatModel.objects.get_or_create(
                    name=data['name'],
                    notes=data['notes'],
                    owner=current_owner,
                    date=current_date,)
            
            for data in data_sorts:
                if data['name'] not in CommonDataSortsModel.objects.filter(name=data['name']):
                    CommonDataSortsModel.objects.get_or_create(
                    name=data['name'],
                    notes=data['notes'],
                    owner=current_owner,
                    date=current_date,)
                else:
                    return redirect('allifmaalcommonapp:commonDefaultValues',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

        
        return redirect('allifmaalcommonapp:commonDefaultValues',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@login_required(login_url='allifmaalusersapp:userLoginPage')
def commonCreateDefaultValues(request, *allifargs, **allifkwargs):
    try:
        """
        Generates ALL default setup values (Units, COA, Taxes, etc.) for a new company.
        """
        allif_data = common_shared_data(request)

        # --- Retrieve common context data ---
        current_owner = allif_data.get("usernmeslg")
        current_company = allif_data.get("main_sbscrbr_entity")
        current_branch = allif_data.get("logged_user_branch")
        current_division = allif_data.get("logged_user_division")
        current_department = allif_data.get("logged_user_department")
        current_date = timezone.now().date() # For fields that don't have auto_now_add

        # --- Initial Validation ---
        if not current_company:
            messages.error(request, "Company context missing. Cannot generate default values.")
            logger.error("commonCreateDefaultValues: Attempted to run without a current_company in allif_data.")
            return redirect('allifmaalcommonapp:commonHome', allifusr=allif_data.get("usrslg"), allifslug=allif_data.get("compslg"))

        # --- Initialize counters and error list for all sections ---
        results = {
            'company_scopes': {'created': 0, 'skipped': 0, 'errors': []},
            'taxes': {'created': 0, 'skipped': 0, 'errors': []},
            'supplier_taxes': {'created': 0, 'skipped': 0, 'errors': []},
            'currencies': {'created': 0, 'skipped': 0, 'errors': []},
            'payment_terms': {'created': 0, 'skipped': 0, 'errors': []},
            'units': {'created': 0, 'skipped': 0, 'errors': []},
            'operation_years': {'created': 0, 'skipped': 0, 'errors': []},
            'operation_year_terms': {'created': 0, 'skipped': 0, 'errors': []},
            'codes': {'created': 0, 'skipped': 0, 'errors': []},
            'categories': {'created': 0, 'skipped': 0, 'errors': []},
            'gl_categories': {'created': 0, 'skipped': 0, 'errors': []},
            'chart_of_accounts': {'created': 0, 'skipped': 0, 'errors': []},
            'overall_error': False
        }

        try:
            # --- START: ONE SINGLE TRANSACTION FOR ALL DEFAULTS ---
            with transaction.atomic():

                # --- Process Company Scopes ---
                for scope_data in DEFAULT_COMPANY_SCOPES:
                    try:
                        _, created = CommonCompanyScopeModel.objects.get_or_create(
                            name=scope_data['name'],
                            company=current_company,
                            defaults={
                                'comments': scope_data['comments'],
                                'owner': current_owner,
                                'branch': current_branch,
                                'division': current_division,
                                'department': current_department,
                                'date': current_date,
                            }
                        )
                        if created: results['company_scopes']['created'] += 1
                        else: results['company_scopes']['skipped'] += 1
                    except IntegrityError as e:
                        results['company_scopes']['skipped'] += 1
                        results['company_scopes']['errors'].append(f"Duplicate scope '{scope_data['name']}': {e}")
                        logger.warning(f"IntegrityError for Company Scope '{scope_data['name']}': {e}")
                    except Exception as e:
                        results['company_scopes']['skipped'] += 1
                        results['company_scopes']['errors'].append(f"Error creating scope '{scope_data['name']}': {e}")
                        logger.exception(f"Unexpected error for Company Scope '{scope_data['name']}'.")

                # --- Process Taxes ---
                for tax_data in DEFAULT_TAXES:
                    # CommonTaxParametersModel
                    try:
                        _, created = CommonTaxParametersModel.objects.get_or_create(
                            taxname=tax_data['taxname'],
                            company=current_company,
                            defaults={
                                'taxdescription': tax_data['taxdescription'],
                                'taxrate': tax_data['taxrate'],
                                'owner': current_owner,
                                'branch': current_branch,
                                'division': current_division,
                                'department': current_department,
                                'date': current_date,
                            }
                        )
                        if created: results['taxes']['created'] += 1
                        else: results['taxes']['skipped'] += 1
                    except IntegrityError as e:
                        results['taxes']['skipped'] += 1
                        results['taxes']['errors'].append(f"Duplicate tax '{tax_data['taxname']}': {e}")
                        logger.warning(f"IntegrityError for Tax '{tax_data['taxname']}': {e}")
                    except Exception as e:
                        results['taxes']['skipped'] += 1
                        results['taxes']['errors'].append(f"Error creating tax '{tax_data['taxname']}': {e}")
                        logger.exception(f"Unexpected error for Tax '{tax_data['taxname']}'.")

                    # CommonSupplierTaxParametersModel
                    try:
                        _, created = CommonSupplierTaxParametersModel.objects.get_or_create(
                            taxname=tax_data['taxname'],
                            company=current_company,
                            defaults={
                                'taxdescription': tax_data['taxdescription'],
                                'taxrate': tax_data['taxrate'],
                                'owner': current_owner,
                                'branch': current_branch,
                                'division': current_division,
                                'department': current_department,
                                'date': current_date,
                            }
                        )
                        if created: results['supplier_taxes']['created'] += 1
                        else: results['supplier_taxes']['skipped'] += 1
                    except IntegrityError as e:
                        results['supplier_taxes']['skipped'] += 1
                        results['supplier_taxes']['errors'].append(f"Duplicate supplier tax '{tax_data['taxname']}': {e}")
                        logger.warning(f"IntegrityError for Supplier Tax '{tax_data['taxname']}': {e}")
                    except Exception as e:
                        results['supplier_taxes']['skipped'] += 1
                        results['supplier_taxes']['errors'].append(f"Error creating supplier tax '{tax_data['taxname']}': {e}")
                        logger.exception(f"Unexpected error for Supplier Tax '{tax_data['taxname']}'.")

                # --- Process Currencies ---
                for currency_data in DEFAULT_CURRENCIES:
                    try:
                        _, created = CommonCurrenciesModel.objects.get_or_create(
                            description=currency_data['description'],
                            company=current_company,
                            defaults={
                                'comments': currency_data['comments'],
                                'owner': current_owner,
                                'branch': current_branch,
                                'division': current_division,
                                'department': current_department,
                                'date': current_date,
                            }
                        )
                        if created: results['currencies']['created'] += 1
                        else: results['currencies']['skipped'] += 1
                    except IntegrityError as e:
                        results['currencies']['skipped'] += 1
                        results['currencies']['errors'].append(f"Duplicate currency '{currency_data['description']}': {e}")
                        logger.warning(f"IntegrityError for Currency '{currency_data['description']}': {e}")
                    except Exception as e:
                        results['currencies']['skipped'] += 1
                        results['currencies']['errors'].append(f"Error creating currency '{currency_data['description']}': {e}")
                        logger.exception(f"Unexpected error for Currency '{currency_data['description']}'.")

                # --- Process Payment Terms ---
                for term_data in DEFAULT_PAYMENT_TERMS:
                    try:
                        _, created = CommonPaymentTermsModel.objects.get_or_create(
                            description=term_data['description'],
                            company=current_company,
                            defaults={
                                'comments': term_data['comments'],
                                'owner': current_owner,
                                'branch': current_branch,
                                'division': current_division,
                                'department': current_department,
                                'date': current_date,
                            }
                        )
                        if created: results['payment_terms']['created'] += 1
                        else: results['payment_terms']['skipped'] += 1
                    except IntegrityError as e:
                        results['payment_terms']['skipped'] += 1
                        results['payment_terms']['errors'].append(f"Duplicate payment term '{term_data['description']}': {e}")
                        logger.warning(f"IntegrityError for Payment Term '{term_data['description']}': {e}")
                    except Exception as e:
                        results['payment_terms']['skipped'] += 1
                        results['payment_terms']['errors'].append(f"Error creating payment term '{term_data['description']}': {e}")
                        logger.exception(f"Unexpected error for Payment Term '{term_data['description']}'.")

                # --- Process Units ---
                for unit_data in DEFAULT_UNITS_OF_MEASURE:
                    try:
                        _, created = CommonUnitsModel.objects.get_or_create(
                            description=unit_data['description'],
                            company=current_company,
                            defaults={
                                'comments': unit_data['comments'],
                                'owner': current_owner,
                                'branch': current_branch,
                                'division': current_division,
                                'department': current_department,
                                'date': current_date, # Only if 'date' is NOT auto_now_add=True
                            }
                        )
                        if created: results['units']['created'] += 1
                        else: results['units']['skipped'] += 1
                    except IntegrityError as e:
                        results['units']['skipped'] += 1
                        results['units']['errors'].append(f"Duplicate unit '{unit_data['description']}': {e}")
                        logger.warning(f"IntegrityError for Unit '{unit_data['description']}': {e}")
                    except Exception as e:
                        results['units']['skipped'] += 1
                        results['units']['errors'].append(f"Error creating unit '{unit_data['description']}': {e}")
                        logger.exception(f"Unexpected error for Unit '{unit_data['description']}'.")

                # --- Process Operation Years ---
                operation_year_map = {} # To store mapping for terms
                for year_data in DEFAULT_OPERATION_YEARS:
                    try:
                        year_instance, created = CommonOperationYearsModel.objects.get_or_create(
                            year=year_data['year'], # Assuming 'year' is the unique identifier field
                            company=current_company,
                            defaults={
                                'comments': year_data['comments'],
                                'owner': current_owner,
                                'branch': current_branch,
                                'division': current_division,
                                'department': current_department,
                                'date': current_date,
                                'start_date': current_date, # Assuming default start/end dates
                                'end_date': current_date,
                            }
                        )
                        operation_year_map[year_data['year']] = year_instance
                        if created: results['operation_years']['created'] += 1
                        else: results['operation_years']['skipped'] += 1
                    except IntegrityError as e:
                        results['operation_years']['skipped'] += 1
                        results['operation_years']['errors'].append(f"Duplicate year '{year_data['year']}': {e}")
                        logger.warning(f"IntegrityError for Operation Year '{year_data['year']}': {e}")
                        try: # Try to get the existing one to link future terms
                            operation_year_map[year_data['year']] = CommonOperationYearsModel.objects.get(
                                year=year_data['year'], company=current_company
                            )
                        except CommonOperationYearsModel.DoesNotExist:
                            logger.error(f"Failed to retrieve existing Operation Year '{year_data['year']}' after IntegrityError.")
                            results['operation_years']['errors'].append(f"Failed to link existing Operation Year: {year_data['year']}")
                    except Exception as e:
                        results['operation_years']['skipped'] += 1
                        results['operation_years']['errors'].append(f"Error creating year '{year_data['year']}': {e}")
                        logger.exception(f"Unexpected error for Operation Year '{year_data['year']}'.")

                # --- Process Operation Year Terms ---
                for term_data in DEFAULT_OPERATION_YEAR_TERMS:
                    parent_year = operation_year_map.get(term_data['operation_year_name'])
                    if not parent_year:
                        results['operation_year_terms']['skipped'] += 1
                        results['operation_year_terms']['errors'].append(f"Missing parent year '{term_data['operation_year_name']}' for term '{term_data['name']}'.")
                        logger.error(f"Skipping term '{term_data['name']}' due to missing parent year '{term_data['operation_year_name']}'.")
                        continue
                    try:
                        _, created = CommonOperationYearTermsModel.objects.get_or_create(
                            name=term_data['name'], # Assuming 'name' is the unique field for terms within a year
                            operation_year=parent_year, # Link to the actual year instance
                            company=current_company,
                            defaults={
                                'comments': term_data['comments'],
                                'owner': current_owner,
                                'branch': current_branch,
                                'division': current_division,
                                'department': current_department,
                                'date': current_date,
                                'start_date': current_date, # Assuming default start/end dates
                                'end_date': current_date,
                            }
                        )
                        if created: results['operation_year_terms']['created'] += 1
                        else: results['operation_year_terms']['skipped'] += 1
                    except IntegrityError as e:
                        results['operation_year_terms']['skipped'] += 1
                        results['operation_year_terms']['errors'].append(f"Duplicate term '{term_data['name']}' for year '{term_data['operation_year_name']}': {e}")
                        logger.warning(f"IntegrityError for Operation Year Term '{term_data['name']}': {e}")
                    except Exception as e:
                        results['operation_year_terms']['skipped'] += 1
                        results['operation_year_terms']['errors'].append(f"Error creating term '{term_data['name']}' for year '{term_data['operation_year_name']}': {e}")
                        logger.exception(f"Unexpected error for Operation Year Term '{term_data['name']}'.")

                # --- Process Codes ---
                for code_data in DEFAULT_CODES:
                    try:
                        _, created = CommonCodesModel.objects.get_or_create(
                            code=code_data['code'], # Assuming 'code' is the unique identifier field
                            company=current_company,
                            defaults={
                                'name': code_data['name'],
                                'description': code_data['description'],
                                'owner': current_owner,
                                'branch': current_branch,
                                'division': current_division,
                                'department': current_department,
                                # 'date' not included if auto_now_add=True
                            }
                        )
                        if created: results['codes']['created'] += 1
                        else: results['codes']['skipped'] += 1
                    except IntegrityError as e:
                        results['codes']['skipped'] += 1
                        results['codes']['errors'].append(f"Duplicate code '{code_data['code']}': {e}")
                        logger.warning(f"IntegrityError for Code '{code_data['code']}': {e}")
                    except Exception as e:
                        results['codes']['skipped'] += 1
                        results['codes']['errors'].append(f"Error creating code '{code_data['code']}': {e}")
                        logger.exception(f"Unexpected error for Code '{code_data['code']}'.")

                # --- Process Categories ---
                for cat_data in DEFAULT_CATEGORIES:
                    try:
                        _, created = CommonCategoriesModel.objects.get_or_create(
                            name=cat_data['name'], # Assuming 'name' is the unique identifier field
                            company=current_company,
                            defaults={
                                'description': cat_data['description'],
                                'code': cat_data['code'],
                                'owner': current_owner,
                                'branch': current_branch,
                                'division': current_division,
                                'department': current_department,
                                'date': current_date,
                                'start_date': current_date, # Assuming default start/end dates
                                'end_date': current_date,
                            }
                        )
                        if created: results['categories']['created'] += 1
                        else: results['categories']['skipped'] += 1
                    except IntegrityError as e:
                        results['categories']['skipped'] += 1
                        results['categories']['errors'].append(f"Duplicate category '{cat_data['name']}': {e}")
                        logger.warning(f"IntegrityError for Category '{cat_data['name']}': {e}")
                    except Exception as e:
                        results['categories']['skipped'] += 1
                        results['categories']['errors'].append(f"Error creating category '{cat_data['name']}': {e}")
                        logger.exception(f"Unexpected error for Category '{cat_data['name']}'.")

                # --- Process GL Account Categories (Phase 1 of COA) ---
                gl_category_objects_map = {} # To store mapping for individual accounts
                for gl_cat_data in DEFAULT_GL_ACCOUNT_CATEGORIES:
                    try:
                        gl_category_instance, created = CommonGeneralLedgersModel.objects.get_or_create(
                            description=gl_cat_data['description'], # Lookup by 'description' which is the category name
                            company=current_company,
                            #defaults={'type': gl_cat_data['type']} # Pass 'type' as a default
                        )
                        logger.info("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
                        gl_category_objects_map[gl_cat_data['description']] = gl_category_instance
                        if created: results['gl_categories']['created'] += 1
                        else: results['gl_categories']['skipped'] += 1
                    except IntegrityError as e:
                        results['gl_categories']['skipped'] += 1
                        results['gl_categories']['errors'].append(f"Duplicate GL Category: {gl_cat_data['description']}")
                        logger.warning(f"IntegrityError for GL Category '{gl_cat_data['description']}': {e}")
                        # Attempt to get the existing category to link future accounts
                        try:
                            gl_category_objects_map[gl_cat_data['description']] = CommonGeneralLedgersModel.objects.get(
                                description=gl_cat_data['description'], company=current_company
                            )
                        except CommonGeneralLedgersModel.DoesNotExist:
                            logger.error(f"Failed to retrieve existing GL Category '{gl_cat_data['description']}' after IntegrityError.")
                            results['gl_categories']['errors'].append(f"Failed to link existing GL Category: {gl_cat_data['description']}")
                    except Exception as e:
                        results['gl_categories']['skipped'] += 1
                        results['gl_categories']['errors'].append(f"Error creating GL Category {gl_cat_data['description']}: {e}")
                        logger.exception(f"Unexpected error for GL Category '{gl_cat_data['description']}'.")

                # --- Process Chart of Accounts (Ledger Accounts) ---
                for account_data in DEFAULT_CHART_OF_ACCOUNTS:
                    category_name = account_data['category_name']
                    target_category = gl_category_objects_map.get(category_name)

                    if not target_category:
                        results['chart_of_accounts']['skipped'] += 1
                        results['chart_of_accounts']['errors'].append(f"Missing GL Category '{category_name}' for account {account_data['description']}. Skipping.")
                        logger.error(f"Skipping account '{account_data['description']}' due to missing GL category '{category_name}'.")
                        continue # Skip this account if its category isn't available

                    try:
                        # Assuming CommonLedgerAccountModel has a 'code' field that is unique_together with 'company'
                        _, created = CommonChartofAccountsModel.objects.get_or_create(
                            code=account_data['code'],
                            company=current_company,
                            defaults={
                                'description': account_data['description'],
                                'category': target_category, # Link to the actual Django Category object
                                'comments': account_data['comments'],
                                'owner': current_owner,
                                'branch': current_branch,
                                'division': current_division,
                                'department': current_department,
                                'date': current_date,
                                'balance': 0.00, # Initial balance, assuming the model can handle it
                            }
                        )
                        if created: results['chart_of_accounts']['created'] += 1
                        else: results['chart_of_accounts']['skipped'] += 1
                    except IntegrityError as e:
                        results['chart_of_accounts']['skipped'] += 1
                        results['chart_of_accounts']['errors'].append(f"Duplicate Account Code '{account_data['code']}': {e}")
                        logger.warning(f"IntegrityError for Account '{account_data['code']}': {e}")
                    except Exception as e:
                        results['chart_of_accounts']['skipped'] += 1
                        results['chart_of_accounts']['errors'].append(f"Error creating account '{account_data['code']}': {e}")
                        logger.exception(f"Unexpected error for Account '{account_data['code']}'.")

            # --- END: ONE SINGLE TRANSACTION FOR ALL DEFAULTS ---

            # --- Final User Feedback ---
            total_errors = sum(len(res['errors']) for key, res in results.items() if isinstance(res, dict))
            total_created = sum(res['created'] for key, res in results.items() if isinstance(res, dict))
            total_skipped = sum(res['skipped'] for key, res in results.items() if isinstance(res, dict))

            if total_errors > 0:
                messages.warning(request, f"Default setup completed with {total_errors} issues. Created: {total_created}, Skipped: {total_skipped}. Please check system logs for details.")
                logger.error(f"Default setup for {current_company.company} completed with errors. Results: {results}")
            elif total_created > 0:
                messages.success(request, f"Default setup completed successfully! Created {total_created} entries. Skipped {total_skipped} existing entries.")
                logger.info(f"Default setup for {current_company.company} completed successfully. Results: {results}")
            else:
                messages.info(request, "All default settings already exist for this company. No new entries were generated.")
                logger.info(f"Default setup for {current_company.company}: All entries already existed. Results: {results}")

        except Exception as outer_e:
            # This catches any critical errors that caused the entire transaction to fail and roll back
            messages.error(request, f"A critical error prevented the default setup. Please try again. ({outer_e})")
            logger.critical(f"CRITICAL ERROR (Full Default Setup). Transaction rolled back for {current_company.name}: {outer_e}", exc_info=True)
            results['overall_error'] = True # Mark that an overall error occurred

        return redirect('allifmaalcommonapp:commonHome', allifusr=allif_data.get("usrslg"), allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
##########################3 company scope ######################################

@logged_in_user_must_have_profile
@logged_in_user_can_add 
@subscriber_company_status
def commonDeleteDefaultValues(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        """
        Deletes all associated data for a specific company across multiple models.
        This function should be called from a view or management command.
        """
        company= allif_data.get("main_sbscrbr_entity")

        company_name = allif_data.get("main_sbscrbr_entity")

        # --- Initialize counters for feedback ---
        deleted_counts = {}
        skipped_models = []
        error_messages = []

    
        # --- Use a single transaction for all deletions ---
        with transaction.atomic():
          
            count, _ = CommonGeneralLedgersModel.objects.filter(company=company).delete()
            deleted_counts['CommonGeneralLedgersModel'] = count
            logger.info(f"Deleted {count} CommonGeneralLedgersModel entries for {company_name}.")
            
            count, _ = CommonChartofAccountsModel.objects.filter(company=company).delete()
            deleted_counts['CommonChartofAccountsModel'] = count
            logger.info(f"Deleted {count} CommonChartofAccountsModel entries for {company_name}.")

            # 3. Delete Units
            # Be careful if CommonUnitsModel has PROTECT and is_system_default logic.
            # You might need to exclude the system default unit here.
            # Example: count, _ = CommonUnitsModel.objects.filter(company=company, is_system_default=False).delete()
            count, _ = CommonUnitsModel.objects.filter(company=company).delete()
            deleted_counts['CommonUnitsModel'] = count
            logger.info(f"Deleted {count} CommonUnitsModel entries for {company_name}.")

            # 4. Delete Company Scopes
            count, _ = CommonCompanyScopeModel.objects.filter(company=company).delete()
            deleted_counts['CommonCompanyScopeModel'] = count
            logger.info(f"Deleted {count} CommonCompanyScopeModel entries for {company_name}.")

            # 5. Delete Tax Parameters
            count, _ = CommonTaxParametersModel.objects.filter(company=company).delete()
            deleted_counts['CommonTaxParametersModel'] = count
            logger.info(f"Deleted {count} CommonTaxParametersModel entries for {company_name}.")

            count, _ = CommonSupplierTaxParametersModel.objects.filter(company=company).delete()
            deleted_counts['CommonSupplierTaxParametersModel'] = count
            logger.info(f"Deleted {count} CommonSupplierTaxParametersModel entries for {company_name}.")

            # 6. Delete Currencies
            count, _ = CommonCurrenciesModel.objects.filter(company=company).delete()
            deleted_counts['CommonCurrenciesModel'] = count
            logger.info(f"Deleted {count} CommonCurrenciesModel entries for {company_name}.")

            # 7. Delete Payment Terms
            count, _ = CommonPaymentTermsModel.objects.filter(company=company).delete()
            deleted_counts['CommonPaymentTermsModel'] = count
            logger.info(f"Deleted {count} CommonPaymentTermsModel entries for {company_name}.")

            # 8. Delete Operation Year Terms (children of CommonOperationYearsModel)
            count, _ = CommonOperationYearTermsModel.objects.filter(company=company).delete()
            deleted_counts['CommonOperationYearTermsModel'] = count
            logger.info(f"Deleted {count} CommonOperationYearTermsModel entries for {company_name}.")

            # 9. Delete Operation Years
            count, _ = CommonOperationYearsModel.objects.filter(company=company).delete()
            deleted_counts['CommonOperationYearsModel'] = count
            logger.info(f"Deleted {count} CommonOperationYearsModel entries for {company_name}.")

            # 10. Delete Codes
            count, _ = CommonCodesModel.objects.filter(company=company).delete()
            deleted_counts['CommonCodesModel'] = count
            logger.info(f"Deleted {count} CommonCodesModel entries for {company_name}.")

            # 11. Delete Categories
            count, _ = CommonCategoriesModel.objects.filter(company=company).delete()
            deleted_counts['CommonCategoriesModel'] = count
            logger.info(f"Deleted {count} CommonCategoriesModel entries for {company_name}.")

            return redirect('allifmaalcommonapp:commonHome',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@logged_in_user_can_add 
@subscriber_company_status
def commonAddCompanyScope(request,*allifargs,**allifkwargs):
    title="Scopes"
    try:
        allif_data=common_shared_data(request)
        form=CommonAddCompanyScopeForm(allif_data.get("main_sbscrbr_entity"))
        allifqueryset=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        if request.method == 'POST':
            form=CommonAddCompanyScopeForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)

                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonAddCompanyScope',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
        else:
            form=CommonAddCompanyScopeForm(allif_data.get("main_sbscrbr_entity"))
        context={
                "form":form,
                "title":title,
                "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/scopes/scopes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@logged_in_user_can_edit 
@subscriber_company_status
def commonEditCompanyScope(request,pk,*allifargs,**allifkwargs):
    title="Update Scope"
    try:
        allif_data=common_shared_data(request)
        user_var_update=CommonCompanyScopeModel.objects.filter(pk=pk).first()
        form=CommonAddCompanyScopeForm(allif_data.get("main_sbscrbr_entity"),instance=user_var_update)
        if request.method=='POST':
            form=CommonAddCompanyScopeForm(allif_data.get("main_sbscrbr_entity"),request.POST or None,request.FILES, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                return redirect('allifmaalcommonapp:commonAddCompanyScope',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                form=CommonAddCompanyScopeForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=user_var_update)
        else:
            form=CommonAddCompanyScopeForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=user_var_update)
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/scopes/scopes.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
        
@logged_in_user_must_have_profile
@logged_in_user_can_delete
@subscriber_company_status
def commonDeleteCompanyScope(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonCompanyScopeModel.objects.filter(pk=pk).first().delete()
        return redirect('allifmaalcommonapp:commonAddCompanyScope',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile 
@logged_in_user_is_admin
@logged_in_user_can_delete
@subscriber_company_status
def commonWantToDeleteScope(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonCompanyScopeModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/scopes/delete-confirm.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
       


@logged_in_user_must_have_profile
@logged_in_user_can_view
@subscriber_company_status
def commonDivisions(request,*allifargs,**allifkwargs):
    title="Divisions"
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonDivisionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonDivisionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        else:
            allifqueryset=[]
        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/divisions/divisions.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@logged_in_user_can_add
@subscriber_company_status
def commonAddDivision(request,*allifargs,**allifkwargs):
    title="New Division"
    try:
        allif_data=common_shared_data(request)
        form=CommonAddDivisionForm()
        if request.method == 'POST':
            form=CommonAddDivisionForm(request.POST,request.FILES)
            if form.is_valid():
                division=request.POST.get('division')
                address=request.POST.get('address')
                if division!="":
                    obj=form.save(commit=False)
                    obj.owner=allif_data.get("logged_in_user")
                    obj.company=allif_data.get("main_sbscrbr_entity")
                    obj.legalname=str(f'{division}+{address}')#important...used to generate company slug
                    obj.save()
                    return redirect('allifmaalcommonapp:commonDivisions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
                else:
                    form=CommonAddDivisionForm(request.POST, request.FILES)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddDivisionForm(request.POST, request.FILES)
        context={"form":form,
                 "title":title,}
        return render(request,'allifmaalcommonapp/divisions/add-division.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@logged_in_user_can_edit
@logged_in_user_is_admin
@subscriber_company_status
def commonEditDivision(request,pk,*allifargs,**allifkwargs):
    title="Update Division Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonDivisionsModel.objects.filter(id=pk).first()
        form=CommonAddDivisionForm(instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddDivisionForm(request.POST or None,request.FILES, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.save()
                return redirect('allifmaalcommonapp:commonDivisions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddDivisionForm(request.POST or None, instance=allifquery_update)
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/divisions/add-division.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       

@logged_in_user_must_have_profile
@logged_in_user_can_view
@subscriber_company_status
def commonDivisionDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Division Details"
        allifquery=CommonDivisionsModel.objects.filter(id=pk).first()
        relatedqueryset=CommonBranchesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allifquery)
        context={
        "allifquery":allifquery,
        "relatedqueryset": relatedqueryset,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/divisions/division-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@logged_in_user_is_admin
@logged_in_user_can_delete
@subscriber_company_status
def commonWantToDeleteDivision(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonDivisionsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/divisions/delete-division-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
    
@logged_in_user_must_have_profile
@logged_in_user_can_delete
@logged_in_user_is_admin
@logged_in_user_has_universal_delete
@subscriber_company_status
def commonDeleteDivision(request,pk,*allifargs,**allifkwargs):
    try:
        CommonDivisionsModel.objects.filter(id=pk).first().delete()
        allif_data=common_shared_data(request)
        return redirect('allifmaalcommonapp:commonDivisions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    


############################### .......Entities and companies details........... #########################3#
@logged_in_user_must_have_profile
@logged_in_user_can_view
@subscriber_company_status
def commonBranches(request,*allifargs,**allifkwargs):
    title="Branches"
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonBranchesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonBranchesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonBranchesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))

        else:
            allifqueryset=[]
        
        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/branches/branches.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@logged_in_user_can_add
@subscriber_company_status
def commonAddBranch(request,*allifargs,**allifkwargs):
    title="New Branch"
    try:
        allif_data=common_shared_data(request)
        form=CommonAddBranchForm(allif_data.get("main_sbscrbr_entity"))
        if request.method == 'POST':
            form=CommonAddBranchForm(allif_data.get("main_sbscrbr_entity"),request.POST,request.FILES)
            if form.is_valid():
                branch=request.POST.get('branch')
                address=request.POST.get('address')
                if branch!="":
                    obj = form.save(commit=False)
                    obj.owner=allif_data.get("usernmeslg")
                    obj.company=allif_data.get("main_sbscrbr_entity")
                    obj.legalname=str(f'{branch}+{address}')#important...used to generate company slug
                    obj.save()
                    return redirect('allifmaalcommonapp:commonBranches',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
                else:
                    form=CommonAddBranchForm(allif_data.get("main_sbscrbr_entity"),request.POST, request.FILES)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddBranchForm(allif_data.get("main_sbscrbr_entity"),request.POST, request.FILES)
        context={"form":form,
                 "title":title,}
        return render(request,'allifmaalcommonapp/branches/add-branch.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@logged_in_user_can_edit
@subscriber_company_status 
def commonEditBranch(request,pk,*allifargs,**allifkwargs):
    title="Update Branch Details"
    try:
        allif_data=common_shared_data(request)
        user_var_update=CommonBranchesModel.objects.filter(id=pk).first()
        form=CommonAddBranchForm(allif_data.get("main_sbscrbr_entity"),instance=user_var_update)
        if request.method=='POST':
            form=CommonAddBranchForm(allif_data.get("main_sbscrbr_entity"),request.POST or None,request.FILES, instance=user_var_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonBranches',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddBranchForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=user_var_update)
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/branches/add-branch.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
        
@logged_in_user_must_have_profile
@logged_in_user_can_view
def commonBranchDetails(request,pk,*allifargs,**allifkwargs):
    title="Branch Details"
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonBranchesModel.objects.filter(id=pk).first()
        if allif_data.get("logged_in_user_has_branches_access")==True:
            relatedqueryset=CommonDepartmentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),branch=allifquery)
        else:
            relatedqueryset=CommonDepartmentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),branch=allifquery,department=allif_data.get("logged_user_department"))
        context={
            "allifquery":allifquery,
           "relatedqueryset":relatedqueryset,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/branches/branch-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@logged_in_user_is_admin
@logged_in_user_can_delete
@logged_in_user_has_branches_delete
@subscriber_company_status
def commonWantToDeleteBranch(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonBranchesModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/branches/delete-branch-confirm.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   

@logged_in_user_must_have_profile
@logged_in_user_can_delete
@logged_in_user_is_admin
@subscriber_company_status
def commonDeleteBranch(request,pk,*allifargs,**allifkwargs):
    try:
        CommonBranchesModel.objects.filter(pk=pk).first().delete()
        allif_data=common_shared_data(request)
        return redirect('allifmaalcommonapp:commonBranches',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_view
@subscriber_company_status
def commonBranchSearch(request,*allifargs,**allifkwargs):
    title="Search"
    try:  
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            if allif_data.get("logged_in_user_has_universal_access")==True:
                searched_data=CommonBranchesModel.objects.filter((Q(branch__icontains=allifsearch)|Q(address__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
            elif allif_data.get("logged_in_user_has_divisional_access")==True:
                searched_data=CommonBranchesModel.objects.filter((Q(branch__icontains=allifsearch)|Q(address__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")))
            elif allif_data.get("logged_in_user_has_branches_access")==True:
                searched_data=CommonBranchesModel.objects.filter((Q(branch__icontains=allifsearch)|Q(address__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")))
            else:
                searched_data=[]
        else:
            searched_data=[]
        context={
        "title":title,
        "searched_data":searched_data,
        }
        return render(request,'allifmaalcommonapp/branches/branches.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

 ################################### below are departments #######################
@logged_in_user_must_have_profile
@logged_in_user_can_view
@subscriber_company_status
def commonDepartments(request,*allifargs,**allifkwargs):
    title="Departments"
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonDepartmentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonDepartmentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonDepartmentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonDepartmentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
       
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/departments/departments.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_view
def commonDepartmentSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            if allif_data.get("logged_in_user_has_universal_access")==True:
                searched_data=CommonDepartmentsModel.objects.filter((Q(department__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
            elif allif_data.get("logged_in_user_has_divisional_access")==True:
                searched_data=CommonDepartmentsModel.objects.filter((Q(department__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")))
            elif allif_data.get("logged_in_user_has_branches_access")==True:
                searched_data=CommonDepartmentsModel.objects.filter((Q(department__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")))
            elif allif_data.get("logged_in_user_has_departmental_access")==True:
                searched_data=CommonDepartmentsModel.objects.filter((Q(department__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")))
            else:
                searched_data=[]
        else:
            searched_data=[]
        context={
        "title":title,
        "allifsearch":allifsearch,
        "searched_data":searched_data,
        }
        return render(request,'allifmaalcommonapp/departments/departments.html',context)
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_add
@subscriber_company_status
def commonAddDepartment(request,*allifargs,**allifkwargs):
    title="Add New Department"
    try:
        allif_data=common_shared_data(request)
        form=CommonAddDepartmentForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            descrp=request.POST.get('department')
            account=CommonDepartmentsModel.objects.filter(department=descrp,company=allif_data.get("main_sbscrbr_entity")).first()
            form=CommonAddDepartmentForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("logged_in_user")
                if account is None:
                    obj.save()
                    return redirect('allifmaalcommonapp:commonDepartments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
                else:
                    error_message="Sorry, a similar department description exists!!!"
                    allifcontext={"error_message":error_message,}
                    return render(request,'allifmaalcommonapp/error/error.html',allifcontext)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddDepartmentForm(allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/departments/add-department.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@logged_in_user_can_edit 
@subscriber_company_status
def commonEditDepartment(request,pk,*allifargs,**allifkwargs):
    title="Update Department Details"
    try:
        allif_data=common_shared_data(request)
        user_var_update=CommonDepartmentsModel.objects.filter(id=pk).first()
        form=CommonAddDepartmentForm(allif_data.get("main_sbscrbr_entity"),instance=user_var_update)
        if request.method=='POST':
            form=CommonAddDepartmentForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=user_var_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonDepartments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
        else:
            form=CommonAddDepartmentForm(allif_data.get("main_sbscrbr_entity"),instance=user_var_update)

        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/departments/add-department.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
        
@logged_in_user_must_have_profile
@logged_in_user_can_view 
@subscriber_company_status
def commonDepartmentDetails(request,allifslug,*allifargs,**allifkwargs):
    try:
        title="Department Details"
        allifquery=CommonDepartmentsModel.objects.filter(pk=allifslug).first()
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/departments/department-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile 
@logged_in_user_is_admin
@subscriber_company_status
@logged_in_user_has_departmental_delete
def commonWantToDeleteDepartment(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonDepartmentsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/departments/delete-dept-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
@logged_in_user_must_have_profile
@logged_in_user_can_delete  
@logged_in_user_is_admin
@subscriber_company_status
@logged_in_user_has_departmental_delete
def commonDeleteDepartment(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonDepartmentsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonDepartments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#################################...HRM....... System users ..........#####################################
@logged_in_user_must_have_profile
#@subscriber_company_status
def commonhrm(request,*allifargs,**allifkwargs):
    title="Human Resources Management"
    try:
        allifqueryset=[]
        allif_data=common_shared_data(request)
        datasorts=CommonDataSortsModel.objects.all()
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                if allif_data.get("logged_in_user_has_universal_access")==True:
                    allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg")).order_by('-first_name')
                elif allif_data.get("logged_in_user_has_divisional_access")==True:
                    allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"),userdivision=allif_data.get("logged_user_division")).order_by('-first_name')
                elif allif_data.get("logged_in_user_has_branches_access")==True:
                    allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"),userdivision=allif_data.get("logged_user_division"),userbranch=allif_data.get("logged_user_branch")).order_by('-first_name')
                elif allif_data.get("logged_in_user_has_departmental_access")==True:
                    allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"),userdivision=allif_data.get("logged_user_division"),userbranch=allif_data.get("logged_user_branch"),userdepartment=allif_data.get("logged_user_department")).order_by('-first_name')
                else:
                    allifqueryset=[]
            else:
                if allif_data.get("logged_in_user_has_universal_access")==True:
                    allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"))
                elif allif_data.get("logged_in_user_has_divisional_access")==True:
                    allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"),userdivision=str(allif_data.get("logged_user_division")))
                elif allif_data.get("logged_in_user_has_branches_access")==True:
                    allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"),userdivision=allif_data.get("logged_user_division"),userbranch=allif_data.get("logged_user_branch"))
                elif allif_data.get("logged_in_user_has_departmental_access")==True:
                    allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"),userdivision=allif_data.get("logged_user_division"),userbranch=allif_data.get("logged_user_branch"),userdepartment=allif_data.get("logged_user_department"))
                else:
                    allifqueryset=[]
        else:
            if allif_data.get("logged_in_user_has_universal_access")==True:
                allifqueryset=User.objects.filter(usercompany=allif_data.get("main_sbscrbr_entity"))
                allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"))
            elif allif_data.get("logged_in_user_has_divisional_access")==True:
                allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"),userdivision=allif_data.get("logged_user_division"))
            elif allif_data.get("logged_in_user_has_branches_access")==True:
                allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"),userdivision=allif_data.get("logged_user_division"),userbranch=allif_data.get("logged_user_branch"))
            elif allif_data.get("logged_in_user_has_departmental_access")==True:
                allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"),userdivision=allif_data.get("logged_user_division"),userbranch=allif_data.get("logged_user_branch"),userdepartment=allif_data.get("logged_user_department"))
            else:
                allifqueryset=[]
        
        context={
            "title":title,
             "allifqueryset":allifqueryset,
             "datasorts":datasorts,
            } 
        return render(request,'allifmaalcommonapp/hrm/staff/staff.html',context)     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@logged_in_user_can_add
@logged_in_user_is_admin
@subscriber_company_status
def commonAddUser(request,allifusr,allifslug,*allifargs,**allifkwargs):#this is where a new user is added by the subscriber admin.
    title="New Staff User Registeration"
    try:
        allif_data=common_shared_data(request)
        
        allif_data=common_shared_data(request)
        form=CreateNewCustomUserForm()
        if request.method=='POST':
            fname=request.POST.get('first_name')
            lname=request.POST.get('last_name')
            email=request.POST.get('email')
            form=CreateNewCustomUserForm(request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                #this is very important line... dont change unless you know what you are doing....
                obj.usercompany=str(allif_data.get("compslg"))
                obj.userdivision=allif_data.get("usernmeslg").userdivision
                obj.userbranch=allif_data.get("usernmeslg").userbranch
                obj.userdepartment=allif_data.get("usernmeslg").userdepartment
                obj.fullNames=str(f'{fname}+{lname}')#important...used to generate user slug
                obj.save()
                return redirect('allifmaalcommonapp:commonhrm',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                messages.info(request,f'Sorry {email} is likely taken, or passwords not match')
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CreateNewCustomUserForm()

        context={"title":title,"form":form,}
        return render(request,"allifmaalcommonapp/hrm/users/adduser.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@logged_in_user_can_edit
@logged_in_user_is_admin
@subscriber_company_status
def commonEditUser(request,pk,*allifargs,**allifkwargs):
    title="Update User Details"
    try:
        user_var_update=User.objects.filter(id=pk).first()
        form=UpdateCustomUserForm(instance=user_var_update)
        allif_data=common_shared_data(request)
        
        if request.method=='POST':
            form=UpdateCustomUserForm(request.POST or None, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                """this is very important line... dont change unless you know what you are doing...."""
                obj.usercompany=str(allif_data.get("compslg"))
                obj.save()
                return redirect('allifmaalcommonapp:commonhrm',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=UpdateCustomUserForm(instance=user_var_update)

        context={"title":title,"form":form,"user_var_update":user_var_update,}
        return render(request,"allifmaalcommonapp/hrm/users/adduser.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@logged_in_user_is_admin
#@subscriber_company_status
def commonUserDetails(request,pk,*allifargs,**allifkwargs):
    title="User Details"
    try:
        allifquery=User.objects.filter(id=pk).first()
        allifqueryset=CommonEmployeesModel.objects.filter(username=allifquery).first()
        candoall=allifquery.can_do_all
        canadd=allifquery.can_add
        canview=allifquery.can_view
        canedit=allifquery.can_edit
        candelete=allifquery.can_delete
        usr_can_access_all=allifquery.can_access_all
        usr_can_access_related=allifquery.can_access_related

        universal_delete=allifquery.universal_delete
        divisional_delete=allifquery.divisional_delete
        branches_delete=allifquery.branches_delete
        departmental_delete=allifquery.departmental_delete

        universal_access=allifquery.universal_access
        divisional_access=allifquery.divisional_access
        branches_access=allifquery.branches_access
        departmental_access=allifquery.departmental_access

        
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

            "universal_delete":universal_delete,
            "divisional_delete":divisional_delete,
            "branches_delete":branches_delete,
            "departmental_delete":departmental_delete,

            "universal_access":universal_access,
            "divisional_access":divisional_access,
            "branches_access":branches_access,
            "departmental_access":departmental_access,
           

        }
        return render(request,'allifmaalcommonapp/hrm/users/user-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
def commonLoggedInUserDetails(request,*allifargs,**allifkwargs):
    title="User Details"
    try:
        allifquery=request.user
        allifqueryset=CommonEmployeesModel.objects.filter(username=allifquery).first()
        candoall=allifquery.can_do_all
        canadd=allifquery.can_add
        canview=allifquery.can_view
        canedit=allifquery.can_edit
        candelete=allifquery.can_delete
        usr_can_access_all=allifquery.can_access_all
        usr_can_access_related=allifquery.can_access_related
        
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

        }
        return render(request,'allifmaalcommonapp/hrm/users/logged-in-user-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
#@subscriber_company_status
def commonShowClickedRowUserDetails(request,pk,*allifargs,**allifkwargs):
    title="User Details"
    try:
        clicked_row_data=User.objects.filter(id=pk).first()
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=User.objects.filter(usercompany=allif_data.get("main_sbscrbr_entity"))
            allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"),userdivision=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"),userdivision=allif_data.get("logged_user_division"),userbranch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=User.objects.filter(usercompany=allif_data.get("compslg"),userdivision=allif_data.get("logged_user_division"),userbranch=allif_data.get("logged_user_branch"),userdepartment=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={
            "clicked_row_data":clicked_row_data,
            "allifqueryset":allifqueryset,
            "formats":formats,
           "datasorts":datasorts,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/hrm/staff/staff.html',context)
   
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete 
@logged_in_user_is_admin 
def commonWantToDeleteUser(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=User.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/hrm/users/user-delete-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete 
@logged_in_user_is_admin 
@logged_in_user_has_universal_delete
def commonDeleteUser(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        User.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonhrm',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
def commonUserSearch(request,*allifargs,**allifkwargs):
    title="Search"
    try:
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=User.objects.filter((Q(first_name__icontains=allifsearch)|Q(last_name__icontains=allifsearch)) & Q(usercompany=allif_data.get("compslg")))
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
        }
        return render(request,'allifmaalcommonapp/hrm/staff/staff.html',context)
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserCanAddEditViewDelete(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=User.objects.filter(id=pk).first()
        allif_data=common_shared_data(request)
        if allifquery.can_do_all==True:
            allifquery.can_do_all=False
            allifquery.can_add=False
            allifquery.can_view=False
            allifquery.can_edit=False
            allifquery.can_delete=False
        else:
            allifquery.can_do_all=True
            allifquery.can_add=True
            allifquery.can_view=True
            allifquery.can_edit=True
            allifquery.can_delete=True
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def commonUserCanAdd(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
        if allifquery.can_add==True:
            allifquery.can_add=False
        else:
            allifquery.can_add=True
        allifquery.can_do_all=False
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserCanView(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
        if allifquery.can_view==True:
            allifquery.can_view=False
        else:
            allifquery.can_view=True
        allifquery.can_do_all=False
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserCanEdit(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
        if allifquery.can_edit==True:
            allifquery.can_edit=False
        else:
            allifquery.can_edit=True
        allifquery.can_do_all=False
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserCanDelete(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
        if allifquery.can_delete==True:
            allifquery.can_delete=False
        else:
            allifquery.can_delete=True
        allifquery.can_do_all=False 
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#####################3  access control for entities and sub entities
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserCanAccessAll(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
        if allifquery.can_access_all==True:
            allifquery.can_access_all=False
        else:
            allifquery.can_access_all=True
        allifquery.save()
        
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserCanAccessRelated(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
        if allifquery.can_access_related==True:
            allifquery.can_access_related=False
        else:
            allifquery.can_access_related=True
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserHasUniversalDelete(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
        if allifquery.universal_delete==True:
            allifquery.universal_delete=False
        else:
            allifquery.universal_delete=True
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserHasDivisionalDelete(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
        if allifquery.divisional_delete==True:
            allifquery.divisional_delete=False
        else:
            allifquery.divisional_delete=True
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserHasBranchesDelete(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
        
        if allifquery.branches_delete==True:
            allifquery.branches_delete=False
        else:
            allifquery.branches_delete=True
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserHasDepartmentalDelete(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
       
        if allifquery.departmental_delete==True:
            allifquery.departmental_delete=False
        else:
            allifquery.departmental_delete=True
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserHasUniversalAccess(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
        
        if allifquery.universal_access==True:
            allifquery.universal_access=False
        else:
            allifquery.universal_access=True
        allifquery.can_do_all=False
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserHasDivisionalAccess(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
       
        if allifquery.divisional_access==True:
            allifquery.divisional_access=False
        else:
            allifquery.divisional_access=True
        allifquery.can_do_all=False
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserHasBranchesAccess(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
       
        if allifquery.branches_access==True:
            allifquery.branches_access=False
        else:
            allifquery.branches_access=True
        allifquery.can_do_all=False
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin 
def commonUserHasDepartmentalAccess(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
        
        if allifquery.departmental_access==True:
            allifquery.departmental_access=False
        else:
            allifquery.departmental_access=True
        allifquery.can_do_all=False
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_has_universal_access
def commonUserAllifaamlAdmin(request,pk):
    try:
        allif_data=common_shared_data(request)
        allifquery=User.objects.filter(id=pk).first()
        user=request.user.is_superuser
        if user==True:
            if allifquery.allifmaal_admin==True:
                allifquery.allifmaal_admin=False
            else:
                allifquery.allifmaal_admin=True
            allifquery.save()
            return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            
        else:
            return render(request,'allifmaalcommonapp/error/error.html',error_context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


###################### staff profiles #####################################

@logged_in_user_must_have_profile
def commonStaffProfiles(request,*allifargs,**allifkwargs):
    title="Staff Profiles"
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonEmployeesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonEmployeesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonEmployeesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonEmployeesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
           
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            } 
        return render(request,'allifmaalcommonapp/hrm/profiles/profiles.html',context)
                    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@login_required(login_url='allifmaalusersapp:userLoginPage')
def commonAddStaffProfile(request,allifusr,allifslug,*allifargs,**allifkwargs): # when someone logs in, they are directed to this page to create company details.
    title="Create Staff Profile"
    try:
        allif_data=common_shared_data(request)
        form=CommonAddStaffProfileForm(allif_data.get("main_sbscrbr_entity"))

        """
        if  main_sbscrbr_entity!=None:
            class CommonAddStaffProfileForm(forms.ModelForm):
                class Meta:
                    model = CommonEmployeesModel
                    fields = ['staffNo','division','branch','firstName','lastName','middleName','gender','department','title','education',
                                'comment','salary','total_salary_paid','salary_payable','salary_balance','username','sysperms','company']
                    widgets={
                    'staffNo':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
                    'firstName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
                    'lastName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
                    'middleName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
                   
                    'title':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
                    'education':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
                    'comment':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
                    'salary':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
                    'total_salary_paid':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
                    'salary_payable':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
                    'salary_balance':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
                    'gender':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
                    'username':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
                    'sysperms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
                    'company':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
                    'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
                    'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
                    'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
                    }
                    
                def __init__(self,*args,**kwargs):
                    super (CommonAddStaffProfileForm,self).__init__(*args,**kwargs) # populates the post
                    self.fields['username'].queryset =User.objects.filter(usercompany=main_sbscrbr_entity.companyslug)
                    self.fields['department'].queryset=CommonDepartmentsModel.objects.filter(company=main_sbscrbr_entity)
                    self.fields['division'].queryset =CommonDivisionsModel.objects.filter(company=main_sbscrbr_entity)
                    self.fields['branch'].queryset=CommonBranchesModel.objects.filter(company=main_sbscrbr_entity)
            form=CommonAddStaffProfileForm(main_sbscrbr_entity)
            """
        if request.method=='POST':
            form=CommonAddStaffProfileForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.save()
                return redirect('allifmaalcommonapp:commonStaffProfiles',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddStaffProfileForm(allif_data.get("main_sbscrbr_entity"))
        context={
            "title":title,
            "form":form,
            }
        return render(request,'allifmaalcommonapp/hrm/profiles/add-staff-profile.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_has_universal_delete
@logged_in_user_can_edit
def commonEditStaffProfile(request,pk,*allifargs,**allifkwargs):
    title="Update Staff Profile Details"
    try:
        allif_data=common_shared_data(request)
        updateItem= CommonEmployeesModel.objects.filter(id=pk).first()
        form=CommonAddStaffProfileForm(allif_data.get("main_sbscrbr_entity"),instance=updateItem)
        if request.method=='POST':
            form=CommonAddStaffProfileForm(allif_data.get("main_sbscrbr_entity"),request.POST,instance=updateItem)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.save()
                return redirect('allifmaalcommonapp:commonStaffProfiles',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
               
        else:
            form=CommonAddStaffProfileForm(allif_data.get("main_sbscrbr_entity"),instance=updateItem)
       
        context={
            "title":title,
            "form":form,
            }
        return render(request,'allifmaalcommonapp/hrm/profiles/add-staff-profile.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
def commonStaffProfileDetails(request,allifslug,*allifargs,**allifkwargs):
    try:
        title="Staff Profile Details"
        allifqueryset=CommonEmployeesModel.objects.filter(stffslug=allifslug).first()
        context={
            "allifqueryset":allifqueryset,
            "title":title,
    
        }
        return render(request,'allifmaalcommonapp/hrm/profiles/profile-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
def commonWantToDeleteProfile(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonEmployeesModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/hrm/profiles/profile-delete-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_can_delete  
def commonDeleteProfile(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonEmployeesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonStaffProfiles',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
def commonProfileSearch(request,*allifargs,**allifkwargs):
    title="Search"
    try:
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            if allif_data.get("logged_in_user_has_universal_access")==True:
                searched_data=CommonEmployeesModel.objects.filter((Q(firstName__icontains=allifsearch)|Q(lastName__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
            elif allif_data.get("logged_in_user_has_divisional_access")==True:
                searched_data=CommonEmployeesModel.objects.filter((Q(firstName__icontains=allifsearch)|Q(lastName__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")))
            elif allif_data.get("logged_in_user_has_branches_access")==True:
                searched_data=CommonEmployeesModel.objects.filter((Q(firstName__icontains=allifsearch)|Q(lastName__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")))
            elif allif_data.get("logged_in_user_has_departmental_access")==True:
                searched_data=CommonEmployeesModel.objects.filter((Q(firstName__icontains=allifsearch)|Q(lastName__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")))
            else:
                searched_data=[]
        else:
            searched_data=CommonEmployeesModel.objects.filter((Q(firstName__icontains=allifsearch)|Q(lastName__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")))
        context={
        "title":title,
        "allifsearch":allifsearch,
        "searched_data":searched_data,}
        return render(request,'allifmaalcommonapp/hrm/profiles/profiles.html',context)
  
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

##############################3 APPROVERS #############################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin
def commonApprovers(request,allifusr,allifslug,*allifargs,**allifkwargs):
    title="Approvers"
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonApproversModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonApproversModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonApproversModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonApproversModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={"title":title,"allifqueryset":allifqueryset,}
        return render(request,'allifmaalcommonapp/approvers/approvers.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
@logged_in_user_is_admin
def commonAddApprover(request,allifusr,allifslug,*allifargs,**allifkwargs):
    title="Add New Approver"
    try:
        allif_data=common_shared_data(request)
        form=CommonAddApproverForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddApproverForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonApprovers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
               
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddApproverForm(allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/approvers/add-approver.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_is_admin
def commonEditApprover(request,allifusr,pk,*allifargs,**allifkwargs):
    title="Edit Approver Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonApproversModel.objects.filter(id=pk).first()
        form=CommonAddApproverForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddApproverForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonApprovers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddApproverForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/approvers/add-approver.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def commonApproverDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Account Details"
        allifquery=CommonApproversModel.objects.filter(id=pk).first()
        
        context={
            "allifquery":allifquery,
            "title":title,
           
        }
        return render(request,'allifmaalcommonapp/approvers/approver-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_departmental_delete
@logged_in_user_can_delete
def commonWantToDeleteApprover(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonApproversModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/approvers/delete-approver-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_universal_delete
@logged_in_user_can_delete
def commonDeleteApprover(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonApproversModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonApprovers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    


###################333 tax parameters settings ###############

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonTaxParameters(request,*allifargs,**allifkwargs):
    title="Applicable Tax Details"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonTaxParametersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        latest=CommonTaxParametersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:3]
        form=CommonAddTaxParameterForm(allif_data.get("main_sbscrbr_entity"),request.POST)
        if request.method == 'POST':
            form=CommonAddTaxParameterForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonTaxParameters',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddTaxParameterForm(allif_data.get("main_sbscrbr_entity"))
        context={
            "title":title,
            "form":form,
            "allifqueryset":allifqueryset,
            "latest":latest,
        }
        return render(request,'allifmaalcommonapp/taxes/taxes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def CommonUpdateTaxDetails(request,pk,*allifargs,**allifkwargs):
    title="Update Tax Details"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonTaxParametersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        update=CommonTaxParametersModel.objects.get(id=pk)
        form =CommonAddTaxParameterForm(allif_data.get("main_sbscrbr_entity"),instance=update)
        if request.method == 'POST':
            form = CommonAddTaxParameterForm(allif_data.get("main_sbscrbr_entity"),request.POST,instance=update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonTaxParameters',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form =CommonAddTaxParameterForm(allif_data.get("main_sbscrbr_entity"),instance=update)
        context = {
            'form':form,
            "update":update,
            "title":title,
            "allifqueryset":allifqueryset,
        }
        
        return render(request,'allifmaalcommonapp/taxes/taxes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def CommonDeleteTaxParameter(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonTaxParametersModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonTaxParameters',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    


#####################3 supplier tax parameters ##########
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonSupplierTaxParameters(request,*allifargs,**allifkwargs):
    title="Applicable Tax Details"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonSupplierTaxParametersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        latest=CommonSupplierTaxParametersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:3]
        form=CommonSupplierAddTaxParameterForm(allif_data.get("main_sbscrbr_entity"),request.POST)
        if request.method == 'POST':
            form=CommonSupplierAddTaxParameterForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSupplierTaxParameters',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonSupplierAddTaxParameterForm(allif_data.get("main_sbscrbr_entity"))
        context={
            "title":title,
            "form":form,
            "allifqueryset":allifqueryset,
            "latest":latest,
        }
        return render(request,'allifmaalcommonapp/taxes/suppliertaxes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def CommonSupplierUpdateTaxDetails(request,pk,*allifargs,**allifkwargs):
    title="Update Tax Details"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonSupplierTaxParametersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        update=CommonSupplierTaxParametersModel.objects.get(id=pk)
        form=CommonSupplierAddTaxParameterForm(allif_data.get("main_sbscrbr_entity"),instance=update)
        if request.method == 'POST':
            form = CommonSupplierAddTaxParameterForm(allif_data.get("main_sbscrbr_entity"),request.POST,instance=update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSupplierTaxParameters',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form =CommonSupplierAddTaxParameterForm(allif_data.get("main_sbscrbr_entity"),instance=update)
        context = {
            'form':form,
            "update":update,
            "title":title,
            "allifqueryset":allifqueryset,
        }
        
        return render(request,'allifmaalcommonapp/taxes/suppliertaxes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def CommonSupplierDeleteTaxParameter(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonSupplierTaxParametersModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonSupplierTaxParameters',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
################################# ACCOUNTS  #############################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin
def commonGeneralLedgers(request,allifusr,allifslug,*allifargs,**allifkwargs):
    title="General Ledger Accounts"
    
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonGeneralLedgersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonGeneralLedgersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonGeneralLedgersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonGeneralLedgersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={"title":title,"allifqueryset":allifqueryset,}
        return render(request,'allifmaalcommonapp/accounts/genledgers.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
@logged_in_user_is_admin
def commonAddGeneralLedger(request,allifusr,allifslug,*allifargs,**allifkwargs):
    title="New General Ledger Account"
    try:
        allif_data=common_shared_data(request)
        form=CommonAddGeneralLedgerForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            descrp=request.POST.get('description')
            deprtmnt=request.POST.get('department')
            CommonDepartmentsModel.objects.filter(id=deprtmnt,company=allif_data.get("main_sbscrbr_entity")).first()
            account=CommonGeneralLedgersModel.objects.filter(description=descrp,department=allif_data.get("logged_user_department"),company=allif_data.get("main_sbscrbr_entity")).first()
            form=CommonAddGeneralLedgerForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                if account is None:
                    obj.save()
                    return redirect('allifmaalcommonapp:commonGeneralLedgers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
                else:
                    error_message="Sorry, a similar account description exists!!!"
                    allifcontext={"error_message":error_message,"form":form,"title":title,}
                    return render(request,'allifmaalcommonapp/accounts/add-gl.html',allifcontext) 
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddGeneralLedgerForm(allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/accounts/add-gl.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_is_admin
def commonEditGeneralLedger(request,allifusr,pk,*allifargs,**allifkwargs):
    title="Update General Ledger Account Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonGeneralLedgersModel.objects.filter(id=pk).first()
        form=CommonAddGeneralLedgerForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddGeneralLedgerForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonGeneralLedgers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddGeneralLedgerForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/accounts/add-gl.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def commonGeneralLedgerDetails(request,allifslug,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Account Details"
        allifquery=CommonGeneralLedgersModel.objects.filter(pk=allifslug).first()
        allifqueryset=CommonChartofAccountsModel.objects.filter(category=allifquery,company=allif_data.get("main_sbscrbr_entity"))
        context={
            "allifquery":allifquery,
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/accounts/gl-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_departmental_delete
@logged_in_user_can_delete
def commonWantToDeleteGenLedger(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonGeneralLedgersModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/accounts/delete-gl-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_universal_delete
@logged_in_user_can_delete
def commonDeleteGeneralLedger(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonGeneralLedgersModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonGeneralLedgers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_departmental_access
def commonSynchGLAccount(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonGeneralLedgersModel.objects.filter(id=pk,company=allif_data.get("main_sbscrbr_entity")).first()
        related_coa_accs=CommonChartofAccountsModel.objects.filter(category=allifquery,company=allif_data.get("main_sbscrbr_entity"))
        acc_balance=0
        for items in related_coa_accs:
            acc_balance+=items.balance
        acc_total=acc_balance
        allifquery.balance=acc_total
        allifquery.save()
        return redirect('allifmaalcommonapp:commonGeneralLedgers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


####################### chart of accounts ########################
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def commonChartofAccounts(request,*allifargs,**allifkwargs):
    title="Chart of Accounts"
    try:
        allif_data=common_shared_data(request)
        
        prospects=CommonQuotesModel.objects.filter(prospect="Likely").order_by('-total','-date')[:15]
        posted_invoices=CommonInvoicesModel.objects.filter(posting_inv_status="posted").order_by('-invoice_total','-date')[:7]
        no_of_prospects=CommonQuotesModel.objects.filter(prospect="Likely").count()
        
        total_value_of_prospects=CommonQuotesModel.objects.filter(prospect="Likely").aggregate(Sum('total'))['total__sum']
        total_value_of_latest_posted_invoices=CommonInvoicesModel.objects.filter(posting_inv_status="posted").aggregate(Sum('invoice_total'))['invoice_total__sum']
        
        debtors=CommonCustomersModel.objects.filter(balance__gt=2).order_by('-balance')[:7]
        creditors=CommonSuppliersModel.objects.filter(balance__gt=2).order_by('-balance')[:8]
        
        debtor_total_balance=CommonCustomersModel.objects.filter(balance__gt=2).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        gold_customers=CommonCustomersModel.objects.all().order_by('-turnover')[:15]
        main_assets=CommonAssetsModel.objects.filter(value__gt=0).order_by('-value')[:10]
        
        gold_customers_turnover=CommonCustomersModel.objects.all().aggregate(Sum('turnover'))['turnover__sum']
      
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        form=CommonFilterCOAForm(allif_data.get("main_sbscrbr_entity"))
        allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by("code")
        assets_tot_val=CommonChartofAccountsModel.objects.filter(code__lte=19999 or 0,company=allif_data.get("main_sbscrbr_entity")).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        liablts_tot_val=CommonChartofAccountsModel.objects.filter(code__gt=19999 or 0,code__lte=29999 or 0,company=allif_data.get("main_sbscrbr_entity")).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        creditors_total_balance=CommonSuppliersModel.objects.filter(balance__gt=2,company=allif_data.get("main_sbscrbr_entity")).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        equity_tot_val=CommonChartofAccountsModel.objects.filter(code__gt=29999 or 0,code__lte=39999 or 0,company=allif_data.get("main_sbscrbr_entity")).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        sum_liablts_and_equity=Decimal(liablts_tot_val or 0)+Decimal(equity_tot_val or 0)+Decimal(creditors_total_balance or 0)

        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                if allif_data.get("logged_in_user_has_universal_access")==True:
                    allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-balance')
                elif allif_data.get("logged_in_user_has_divisional_access")==True:
                    allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('-balance')
                elif allif_data.get("logged_in_user_has_branches_access")==True:
                    allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('-balance')
                elif allif_data.get("logged_in_user_has_departmental_access")==True:
                    allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('-balance')
                else:
                    allifqueryset=[]
            else:
                if allif_data.get("logged_in_user_has_universal_access")==True:
                    allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by("code")
                elif allif_data.get("logged_in_user_has_divisional_access")==True:
                    allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by("code")
                elif allif_data.get("logged_in_user_has_branches_access")==True:
                    allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by("code")
                elif allif_data.get("logged_in_user_has_departmental_access")==True:
                    allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by("code")
                else:
                    allifqueryset=[]
        else:
            if allif_data.get("logged_in_user_has_universal_access")==True:
                allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by("code")
            elif allif_data.get("logged_in_user_has_divisional_access")==True:
                allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by("code")
            elif allif_data.get("logged_in_user_has_branches_access")==True:
                allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by("code")
            elif allif_data.get("logged_in_user_has_departmental_access")==True:
                allifqueryset=CommonChartofAccountsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by("code")
            else:
                allifqueryset=[]
        
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
            "form":form,
            "assets_tot_val":assets_tot_val,
            "liablts_tot_val":liablts_tot_val,
            "equity_tot_val":equity_tot_val,
            "sum_liablts_and_equity":sum_liablts_and_equity,
            "datasorts":datasorts,
            "formats":formats,
        }
        return render(request,'allifmaalcommonapp/accounts/chart-of-accs.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_can_add
def commonAddChartofAccount(request,*allifargs,**allifkwargs):
    title="Add New Account"
    try:
        allif_data=common_shared_data(request)
        form=CommonAddChartofAccountForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            code=request.POST.get('code')
            descrp=request.POST.get('description')
            deprtmnt=request.POST.get('department')
            account=CommonChartofAccountsModel.objects.filter(code=code,description=descrp,company=allif_data.get("main_sbscrbr_entity"),department=deprtmnt).first()
            form=CommonAddChartofAccountForm(allif_data.get("main_sbscrbr_entity"), request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                if account is None:
                    obj.save()
                    return redirect('allifmaalcommonapp:commonChartofAccounts',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
                else:
                    error_message="Sorry, a similar account description exists!!!"
                    allifcontext={"error_message":error_message,"form":form,"title":title,}
                    return render(request,'allifmaalcommonapp/accounts/add-coa.html',allifcontext)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddChartofAccountForm(allif_data.get("main_sbscrbr_entity"), request.POST)
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/accounts/add-coa.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_can_add
def commonChartofAccountSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        searched_data=[]
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            if allif_data.get("logged_in_user_has_universal_access")==True:
                searched_data=CommonChartofAccountsModel.objects.filter((Q(description__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(category__description__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity"))).order_by("code")
            elif allif_data.get("logged_in_user_has_divisional_access")==True:
                searched_data=CommonChartofAccountsModel.objects.filter((Q(description__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(category__description__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")) & Q(division=allif_data.get("logged_user_division"))).order_by("code")
            elif allif_data.get("logged_in_user_has_branches_access")==True:
                searched_data=CommonChartofAccountsModel.objects.filter((Q(description__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(category__description__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")) & Q(division=allif_data.get("logged_user_division")) & Q(branch=allif_data.get("logged_user_branch"))).order_by("code")
            elif allif_data.get("logged_in_user_has_departmental_access")==True:
                searched_data=CommonChartofAccountsModel.objects.filter((Q(description__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(category__description__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")) & Q(division=allif_data.get("logged_user_division")) & Q(department=allif_data.get("logged_user_department")) & Q(branch=allif_data.get("logged_user_branch"))).order_by("code")
               
            else:
                searched_data=[]
        else:
            searched_data=[]
        context={
        "title":title,
        "allifsearch":allifsearch,
        "searched_data":searched_data,
        }
        return render(request,'allifmaalcommonapp/accounts/chart-of-accs.html',context)
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_can_edit
def commonEditChartofAccount(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Update Account Details"
        allifquery_update=CommonChartofAccountsModel.objects.filter(id=pk).first()
        form=CommonAddChartofAccountForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddChartofAccountForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonChartofAccounts',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddChartofAccountForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/accounts/add-coa.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
        
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_can_view
def commonChartofAccountDetails(request,allifslug,*allifargs,**allifkwargs):
    try:
        title="Account Details"
        allifquery=CommonChartofAccountsModel.objects.filter(pk=allifslug).first()
        context={
            "allifquery":allifquery,
            "title":title,}
        return render(request,'allifmaalcommonapp/accounts/coa-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_can_delete
@logged_in_user_has_departmental_delete
def commonWantToDeleteCoA(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonChartofAccountsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/accounts/delete-coa-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_can_delete
@logged_in_user_has_departmental_delete
def commonDeleteChartofAccount(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonChartofAccountsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonChartofAccounts',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def commonSelectedRelatedAccs(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        if request.method=="GET":
            selectedoption=request.GET.get('allifidforselecteditem')
            selectedcategoryid=CommonGeneralLedgersModel.objects.filter(pk=selectedoption,company=allif_data.get("main_sbscrbr_entity")).first()
            catid=selectedcategoryid.id
            allifquery=CommonChartofAccountsModel.objects.filter(category=catid,company=allif_data.get("main_sbscrbr_entity"))#this is a queryset that will be sent to the backend.
            allifqueryrelatedlist=list(CommonChartofAccountsModel.objects.filter(category=catid,company=allif_data.get("main_sbscrbr_entity")))#this is a list
            serialized_data = serialize("json", allifqueryrelatedlist)
            myjsondata= json.loads(serialized_data)
            allifqueryset=list(CommonChartofAccountsModel.objects.filter(category=catid,company=allif_data.get("main_sbscrbr_entity")).values("category","description","id","code","balance"))
            allifrelatedserlized= json.loads(serialize('json', allifquery))#this is a list
            mystringjsondata=json.dumps(allifrelatedserlized)#this is string
            return JsonResponse(allifqueryset,safe=False)
        else:
            allifqueryset=[]
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def commonClearAcc(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        acc=CommonChartofAccountsModel.objects.filter(id=pk).first()
        acc.balance=0
        acc.save()
        return redirect('allifmaalcommonapp:commonChartofAccounts',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def commonChartofAccAdvanceSearch(request,*allifargs,**allifkwargs):
    title="Chart of A/Cs Advanced Search"
    try:
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        allifqueryset=[]
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('name')[:4]
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_value=request.POST.get('startvalue')
            end_value=request.POST.get('endvalue')
            if start_value!="" and end_value!="":
                searched_data=CommonChartofAccountsModel.objects.filter(Q(balance__gte=start_value)& Q(balance__lte=end_value)& Q(company=allif_data.get("main_sbscrbr_entity"))).order_by('code')
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/accounts/coa-search-pdf.html'
                    allifcontext={"searched_data":searched_data,"title":title,"main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),"scopes":scopes}
                  
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = f'filename="Chart-of-accounts-Advanced-Searched_Results.pdf"'
                    template = get_template(template_path)
                    html=template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                else:
                    allifqueryset=CommonChartofAccountsModel.objects.filter(Q(balance__gte=start_value)& Q(balance__lte=end_value)& Q(company=allif_data.get("main_sbscrbr_entity"))).order_by('code')
                    context={"allifqueryset":allifqueryset,"formats":formats,"title":title,}
                    return render(request,'allifmaalcommonapp/accounts/chart-of-accs.html',context)  
            else:
                allifqueryset=[]
            context={"allifqueryset":allifqueryset,"formats":formats,"title":title,}
            return render(request,'allifmaalcommonapp/accounts/chart-of-accs.html',context)
        else:
            context={"allifqueryset":allifqueryset,"formats":formats,"title":title,"scopes":scopes
            }
            return render(request,'allifmaalcommonapp/companies/companies.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

############################### EMAILS AND SMS ####################

@logged_in_user_must_have_profile
def commonEmailsAndSMS(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Emails and SMSs"
        allifqueryset=CommonEmailsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        ################## Sending an Email ###########################################
        ahmed='info@allifmaal.com'
        muse='allifmaalengineering@gmail.com'
        subject = title
        message = f'Thank you for creating an account!'
        email_sender=allif_data.get("usernmeslg").email #'ahmedmusadir@gmail.com'
        recipient_list = [ahmed,muse]
        send_mail(subject, message, email_sender, recipient_list)# uncomment to send emails.
        email=CommonEmailsModel(subject=subject,message=message,recipient=recipient_list,sender=email_sender,company=allif_data.get("main_sbscrbr_entity"))
        #email.save()

        ################3 this below is for the SMS... this worked ###################
        account_sid = "ACb19b2a5701ec5f53c38e113ae9595917" # Twilio account
        auth_token  = "143c2731b15d0a8a9a918db838ac048a"  # Twilio Token
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        to="+252610993964",# number registered with Twilio
        from_="+17753731268",#virtual number from Twilio
        body="Testing Message Here") # message to be sent.

        context={"title":title,"allifqueryset":allifqueryset,}
        return render(request,'allifmaalcommonapp/comms/emailsms.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
def commonDeleteEmail(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonEmailsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonChartofAccounts',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


#################################### BANKS SECTION #############################
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonBanks(request,*allifargs,**allifkwargs):
    try:
        title="Banks"
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonBanksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonBanksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonBanksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonBanksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]

        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/banks/banks.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddBank(request,allifusr,allifslug,*allifargs,**allifkwargs):
    title="Add New Bank"
    try:
        allif_data=common_shared_data(request)
        form=CommonAddBankForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddBankForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonBanks',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddBankForm(allif_data.get("main_sbscrbr_entity"))
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/banks/add-bank.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditBank(request,pk,*allifargs,**allifkwargs):
    title="Update Bank Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonBanksModel.objects.filter(id=pk).first()
        form=CommonAddBankForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddBankForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonBanks',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
               
        else:
            form=CommonAddBankForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/banks/add-bank.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonBankDetails(request,allifslug,*allifargs,**allifkwargs):
    try:
        title="Bank Details"
        allif_data=common_shared_data(request)
        allifquery=CommonBanksModel.objects.filter(pk=allifslug).first()
        allifqueryset=CommonBankWithdrawalsModel.objects.filter(bank=allifquery,company=allif_data.get("main_sbscrbr_entity"))
        queryset=CommonBankWithdrawalsModel.objects.filter(bank=allifquery,company=allif_data.get("main_sbscrbr_entity"))
        deposits=CommonShareholderBankDepositsModel.objects.filter(bank=allifquery)
        context={
            "allifquery":allifquery,
            "title":title,
            "allifqueryset":allifqueryset,
            "queryset":queryset,
            "deposits":deposits,
        }
        return render(request,'allifmaalcommonapp/banks/bank-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_can_delete  
def commonWantToDeleteBank(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonBanksModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/banks/delete-bank-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_branches_delete
@logged_in_user_can_delete  
def commonDeleteBank(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonBanksModel.objects.filter(pk=pk).first().delete()
        return redirect('allifmaalcommonapp:commonBanks',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view 
def commonBankSearch(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Search Results"
        searched_data=[]
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            if allif_data.get("logged_in_user_has_universal_access")==True:
                searched_data=CommonBanksModel.objects.filter((Q(name__icontains=allifsearch)|Q(account__icontains=allifsearch)|Q(balance__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
            elif allif_data.get("logged_in_user_has_divisional_access")==True:
                searched_data=CommonBanksModel.objects.filter((Q(name__icontains=allifsearch)|Q(account__icontains=allifsearch)|Q(balance__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")) & Q(division=allif_data.get("logged_user_division")))
            elif allif_data.get("logged_in_user_has_branches_access")==True:
                searched_data=CommonBanksModel.objects.filter((Q(name__icontains=allifsearch)|Q(account__icontains=allifsearch)|Q(balance__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")) & Q(division=allif_data.get("logged_user_division")) & Q(branch=allif_data.get("logged_user_branch")))
            elif allif_data.get("logged_in_user_has_departmental_access")==True:
                searched_data=CommonBanksModel.objects.filter((Q(name__icontains=allifsearch)|Q(account__icontains=allifsearch)|Q(balance__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")) & Q(division=allif_data.get("logged_user_division")) & Q(department=allif_data.get("logged_user_department")) & Q(branch=allif_data.get("logged_user_branch")))
            else:
                searched_data=[]
        else:
            searched_data=[]

        context={"title":title,"allifsearch":allifsearch,"searched_data":searched_data,}
        return render(request,'allifmaalcommonapp/banks/banks.html',context)
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
############################################### BANK DEPOSITS ################################
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view 
def commonBankShareholderDeposits(request,*allifargs,**allifkwargs):
    try:
        title="Bank Deposits"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        allifqueryset=[]
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={"title":title,"allifqueryset":allifqueryset,"formats":formats,
        }
        return render(request,'allifmaalcommonapp/banks/deposits/shareholders/deposits-sh.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
@logged_in_user_is_admin
def commonAddBankShareholderDeposit(request,*allifargs,**allifkwargs):
    title="Add New Bank Deposit"
    try:
        allif_data=common_shared_data(request)
        form=CommonBankDepositAddForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonBankDepositAddForm(allif_data.get("main_sbscrbr_entity"), request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonBankShareholderDeposits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
               
        context={
            "form":form,
            "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
            "title":title,
           
            }
        return render(request,'allifmaalcommonapp/banks/deposits/shareholders/add-deposit-sh.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
        

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
@logged_in_user_is_admin
def commonPostShareholderDeposit(request,pk,*allifargs,**allifkwargs):
    #try:
        allif_data=common_shared_data(request)
        allifquery=CommonShareholderBankDepositsModel.objects.filter(id=pk).first()
        #if allifquery.status=="posted":
        bank=allifquery.bank
        amount=allifquery.amount
        chartaccasset=allifquery.asset
        chartacceqty=allifquery.equity
        ########### increase the asset account
        query=CommonChartofAccountsModel.objects.filter(id=chartaccasset.id).first()
        initial_bank_balnce=query.balance
        query.balance=initial_bank_balnce+Decimal(amount)
        query.save()

        ############ increase equity account ##############
        eqtyquery=CommonChartofAccountsModel.objects.filter(id=chartacceqty.id).first()
        initial_bank_balnce=eqtyquery.balance
        eqtyquery.balance=initial_bank_balnce+Decimal(amount)
        allifquery.status="posted"
        allifquery.save()
        eqtyquery.save()
        return redirect('allifmaalcommonapp:commonBankShareholderDeposits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
        #else:
           # return render(request,'allifmaalcommonapp/error/error.html',error_context)
          
    #except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditBankShareholderDeposit(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonShareholderBankDepositsModel.objects.filter(id=pk).first()
        form=CommonBankDepositAddForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery_update)
        title=allifquery_update
        if request.method=='POST':
            form=CommonBankDepositAddForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=allifquery_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonBankShareholderDeposits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
        
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonBankDepositAddForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery_update)

        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/banks/deposits/shareholders/add-deposit-sh.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonBankShareholderDepositDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonShareholderBankDepositsModel.objects.filter(pk=pk).first()
        title="Deposit Details"
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/banks/deposits/shareholders/deposit-details-sh.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonWantToDeleteDeposit(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonShareholderBankDepositsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/banks/deposits/shareholders/delete-deposit-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)         

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
@logged_in_user_has_branches_delete
def commonDeleteBankShareholderDeposit(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonShareholderBankDepositsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonBankShareholderDeposits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDepositSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonShareholderBankDepositsModel.objects.filter((Q(description__icontains=allifsearch)|Q(amount__icontains=allifsearch)|Q(bank__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
        }
        return render(request,'allifmaalcommonapp/banks/deposits/shareholders/deposits-sh.html',context)
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDepositAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Bank Deposits Advanced Search"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        current_date=timezone.now().date().today()
        firstDate=current_date
        lastDate=current_date
        largestAmount=0
        firstDepo=CommonShareholderBankDepositsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first()

        lastDepo=CommonShareholderBankDepositsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if firstDepo and lastDepo:
            firstDate=CommonShareholderBankDepositsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
            lastDate=CommonShareholderBankDepositsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
            largestAmount=CommonShareholderBankDepositsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-amount').first().amount
        else:
            firstDate=current_date
            lastDate=current_date
     
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
               
                if selected_option=="pdf":
                    template_path='allifmaalcommonapp/banks/deposits/shareholders/deposit-search-pdf.html'
                    allifcontext={"searched_data":searched_data,"title":title,"main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),"scopes":scopes,}
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="bank-deposits-advanced-searched-results.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                    "formats":formats,
                    "title":title,
                     "scopes":scopes
                    }
                    return render(request,'allifmaalcommonapp/banks/deposits/shareholders/deposits-sh.html',context)
                   
            else:
                searched_data=[]
                allifqueryset=[]
                context={"allifqueryset":allifqueryset,"formats":formats,"title":title,
                }
                return render(request,'allifmaalcommonapp/banks/deposits/shareholders/deposits-sh.html',context)
       
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
             "scopes":scopes
            }
            return render(request,'allifmaalcommonapp/banks/deposits/shareholders/deposits-sh.html',context)
           
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonClearShareholderDepositSearch(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        return redirect('allifmaalcommonapp:commonBankShareholderDeposits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
############################################### BANK WITHDRAWALS ################################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonBankWithdrawals(request,*allifargs,**allifkwargs):
    try:
        title="Bank Withdrawals"
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        allifqueryset=[]
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonBankWithdrawalsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonBankWithdrawalsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonBankWithdrawalsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonBankWithdrawalsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request,'allifmaalcommonapp/banks/withdrawals/withdrawals.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddBankWithdrawal(request,*allifargs,**allifkwargs):
    try:
        title="New Withdrawal"
        allif_data=common_shared_data(request)
        form=CommonBankWithdrawalsAddForm(allif_data.get("main_sbscrbr_entity"))
        
        if request.method=='POST':
            bank=request.POST.get('bank')
            amount=request.POST.get('amount')
            chart_account=request.POST.get('asset')
            bankcoa=request.POST.get('bankcoa')
            
            form=CommonBankWithdrawalsAddForm(allif_data.get("main_sbscrbr_entity"), request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
               
                obj.save()
                myquery=CommonBanksModel.objects.filter(id=bank).first()
                initial_bank_balnce=myquery.balance
                myquery.balance=initial_bank_balnce-Decimal(amount)
                myquery.deposit=0
                myquery.withdrawal=Decimal(amount)
                myquery.save()
                acc=CommonChartofAccountsModel.objects.filter(pk=chart_account).first()# The misc cost service supplier
                init_acc_balance=acc.balance
                acc.balance=init_acc_balance+Decimal(amount)
                
                acc.save()

                accnt=CommonChartofAccountsModel.objects.filter(pk=bankcoa).first()# The misc cost service supplier
                init_acc_balance=accnt.balance
                accnt.balance=init_acc_balance-Decimal(amount)
                accnt.save()
                return redirect('allifmaalcommonapp:commonBankWithdrawals',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)

        context={
            "form":form,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/banks/withdrawals/add-withdrawal.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditBankWithdrawal(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonBankWithdrawalsModel.objects.filter(id=pk).first()
        form=CommonBankWithdrawalsAddForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery_update)
        title=allifquery_update
        if request.method=='POST':
            form=CommonBankWithdrawalsAddForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonBankWithdrawals',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)

        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/banks/withdrawals/add-withdrawal.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonBankWithdrawalDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonBankWithdrawalsModel.objects.filter(pk=pk).first()
        title="Withdrawal Details"
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/banks/withdrawals/withdrawal-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonWantToDeleteWithdrawal(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonBankWithdrawalsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/banks/withdrawals/delete-withdrawal-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)              

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
@logged_in_user_has_branches_delete
def commonDeleteBankWithdrawal(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonBankWithdrawalsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonBankWithdrawals',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWithdrawalSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        searched_data=[]
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonBankWithdrawalsModel.objects.filter((Q(description__icontains=allifsearch)|Q(amount__icontains=allifsearch)|Q(bank__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]

        context={
        "title":title,
        "searched_data":searched_data,
        }
        return render(request,'allifmaalcommonapp/banks/withdrawals/withdrawals.html',context)
   
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWithdrawalAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Bank Withdrawals Advanced Search"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        allifqueryset=CommonBankWithdrawalsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        current_date=timezone.now().date().today()
        firstDate=current_date
        lastDate=current_date
        largestAmount=0
        firstDepo=CommonBankWithdrawalsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first()

        lastDepo=CommonBankWithdrawalsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if firstDepo and lastDepo:
            firstDate=CommonBankWithdrawalsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
            lastDate=CommonBankWithdrawalsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
            largestAmount=CommonBankWithdrawalsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-amount').first().amount
        else:
            firstDate=current_date
            lastDate=current_date

        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonBankWithdrawalsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/banks/withdrawals/withdrawal-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                    "scopes":scopes
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="bank-withdrawals-advanced-searched-results.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                # if excel is selected
                
                else:
                    searched_data=CommonBankWithdrawalsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                    context = {
                    "searched_data":searched_data,
                    "formats":formats,
                    "title":title,
                     "scopes":scopes
                    }
                    return render(request,'allifmaalcommonapp/banks/withdrawals/withdrawals.html',context)
                    
            else:
                allifqueryset=CommonBankWithdrawalsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
                
                
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
             "scopes":scopes
            }
            return render(request,'allifmaalcommonapp/banks/withdrawals/withdrawals.html',context)
           
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
             "scopes":scopes
            }
            return render(request,'allifmaalcommonapp/banks/withdrawals/withdrawals.html',context)
          
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
#################################### BANKS SECTION #############################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonClearShareholderWithdrwlSearch(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        return redirect('allifmaalcommonapp:commonBankWithdrawals',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
##############################33 suppliers section ###############3
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonSuppliers(request,*allifargs,**allifkwargs):
    try:
        title="Suppliers And Vendors"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                if allif_data.get("logged_in_user_has_universal_access")==True:
                    allifqueryset=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-name')
                elif allif_data.get("logged_in_user_has_divisional_access")==True:
                    allifqueryset=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('-name')
                elif allif_data.get("logged_in_user_has_branches_access")==True:
                    allifqueryset=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('-name')
                elif allif_data.get("logged_in_user_has_departmental_access")==True:
                    allifqueryset=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('-name')
                else:
                    allifqueryset=[]
        else:
            if allif_data.get("logged_in_user_has_universal_access")==True:
                allifqueryset=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('date')
            elif allif_data.get("logged_in_user_has_divisional_access")==True:
                allifqueryset=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
            elif allif_data.get("logged_in_user_has_branches_access")==True:
                allifqueryset=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
            elif allif_data.get("logged_in_user_has_departmental_access")==True:
                allifqueryset=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
            else:
                allifqueryset=[]
          
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request,'allifmaalcommonapp/suppliers/suppliers.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonSupplierSearch(request,*allifargs,**allifkwargs):
    title="Search Results"
    try:
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonSuppliersModel.objects.filter((Q(name__icontains=allifsearch)|Q(balance__icontains=allifsearch)|Q(address__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            allifsearch=[]

        context={
        "title":title,
        "searched_data":searched_data,}
        return render(request,'allifmaalcommonapp/suppliers/suppliers.html',context)
   
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonClearSupplierSearch(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        return redirect('allifmaalcommonapp:commonSuppliers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
     
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddSupplier(request,allifusr,allifslug,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Add New Supplier"
        form=CommonAddSupplierForm(allif_data.get("main_sbscrbr_entity"))
       
        if request.method=='POST':
            form=CommonAddSupplierForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSuppliers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
              
        else:
            form=CommonAddSupplierForm(allif_data.get("main_sbscrbr_entity"))
         
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/suppliers/add-supplier.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditSupplier(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Supplier Details"
        allif_data=common_shared_data(request)
        allifquery_update=CommonSuppliersModel.objects.filter(id=pk).first()
        form=CommonAddSupplierForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddSupplierForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSuppliers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSupplierForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
           
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/suppliers/add-supplier.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonSupplierDetails(request,allifslug,*allifargs,**allifkwargs):
    try:
        title="Supplier Details"
        allifquery=CommonSuppliersModel.objects.filter(pk=allifslug).first()
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/suppliers/supplier-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
@logged_in_user_has_departmental_delete
def commonWantToDeleteSupplier(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonSuppliersModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/suppliers/delete-supplier-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)  
        
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
@logged_in_user_has_departmental_delete
def commonDeleteSupplier(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonSuppliersModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonSuppliers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
def commonSupplierAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Supplier Advanced Search Results"
        allifqueryset=[]
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        current_date=timezone.now().date().today()
        firstDate=current_date
        lastDate=current_date
        largestAmount=0
        firstDepo=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first()
    
        lastDepo=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if firstDepo and lastDepo:
            firstDate=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
            lastDate=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
            largestAmount=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-balance').first().balance
        else:
            firstDate=current_date
            lastDate=current_date

        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonSuppliersModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(balance__gte=start_value or 0) & Q(balance__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/suppliers/supsearchpdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                    "scopes":scopes,
                    "title":title,}
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="supplier-advanced-searched-results.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                else:
                    allifqueryset=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
                    context={"title":title,"allifqueryset":allifqueryset,}
                    return render(request,'allifmaalcommonapp/suppliers/suppliers.html',context)
            else:
                searched_data=[]
                main_sbscrbr_entity=allif_data.get("main_sbscrbr_entity")
        else:
            main_sbscrbr_entity=allif_data.get("main_sbscrbr_entity")
            searched_data=[]

        context={
        "allifqueryset":allifqueryset,
        "formats":formats,
        "title":title,
       
        }
        return render(request,'allifmaalcommonapp/suppliers/suppliers.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
    
############################################ CUSTOMERS ######################
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCustomers(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
        sector=str(allif_data.get("main_sbscrbr_entity").sector)
        if sector == "Healthcare":
            title="Registered Patients"
        elif sector=="Education":
            title="Registered Students"
        else:
            title="Registered Customers"
        
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]

        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request,'allifmaalcommonapp/customers/customers.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddCustomer(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        sector=str(allif_data.get("main_sbscrbr_entity").sector)

        ###### start... UID generation ##################
        allifquery=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        currntyear=timezone.now().date().today().year
        allifuid=str(nmbr)+"/"+str(currntyear)+"/"+str(unque)
        ###### End... UID generation ##################
        
        if sector == "Healthcare":
            title="Patient Registeration"
        elif sector=="Education":
            title="Student Registeration"
        else:
            title="Customer Registeration"
            
        form=CommonCustomerAddForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonCustomerAddForm(allif_data.get("main_sbscrbr_entity"), request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.uid=allifuid
                obj.save()
                return redirect('allifmaalcommonapp:commonCustomers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonCustomerAddForm(allif_data.get("main_sbscrbr_entity"))
          
        context={
            "form":form,
            "sector":sector,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/customers/add-customer.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditCustomer(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        sector=str(allif_data.get("main_sbscrbr_entity").sector)
        allifquery_update=CommonCustomersModel.objects.filter(id=pk).first()
        allifuid=allifquery_update.uid
        form=CommonCustomerAddForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery_update)
        if sector == "Healthcare":
            title="Update Patient Details"
        elif sector=="Education":
            title="Update Student Details"
        else:
            title="Update Customer Details"

        if request.method=='POST':
            form=CommonCustomerAddForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=allifquery_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.uid=allifuid
                obj.save()
                return redirect('allifmaalcommonapp:commonCustomers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
           
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
                
        else:
                form=CommonCustomerAddForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery_update)

        context={"title":title,"form":form,"sector":sector, "allifquery_update":allifquery_update}
        return render(request,'allifmaalcommonapp/customers/add-customer.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCustomerDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonCustomersModel.objects.filter(pk=pk).first()
        sector=str(allif_data.get("main_sbscrbr_entity").sector)
        if sector == "Healthcare":
            title="Patient Details"
        elif sector=="Education":
            title="Student Details"
        else:
            title="Customer Details"

        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/customers/customer-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin 
def commonDeleteCustomer(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonCustomersModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonCustomers',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCustomerSearch(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Search Results"
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonCustomersModel.objects.filter((Q(name__icontains=allifsearch)|Q(balance__icontains=allifsearch)|Q(address__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
       
        }
        return render(request,'allifmaalcommonapp/customers/customers.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCustomerAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Customer Advanced Search Results"
        allif_data=common_shared_data(request)
        allifqueryset=[]
       
        current_date=timezone.now().date().today()
        firstDate=current_date
        lastDate=current_date
        largestAmount=0
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        firstDepo=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first()
    
        lastDepo=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if firstDepo and lastDepo:
            firstDate=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
            lastDate=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
            largestAmount=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-balance').first().balance
        else:
            firstDate=current_date
            lastDate=current_date

        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonCustomersModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(balance__gte=start_value or 0) & Q(balance__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/customers/customer_search_pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                    "scopes":scopes,
                
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="Customer-advanced-searched-results.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                # if excel is selected
               
                else:
                    searched_data=[]
                context = {
                "searched_data":searched_data,
                
                "title":title,
                    
                }
                return render(request,'allifmaalcommonapp/customers/customers.html',context)
                    
            else:
                searched_data=[]
            
            context={
            "allifqueryset":allifqueryset,
            "searched_data":searched_data,
            
            "title":title,
             
            }
            return render(request,'allifmaalcommonapp/customers/customers.html',context)
           
        else:
            context={
            "allifqueryset":allifqueryset,
           
            "title":title,
            
            }
            return render(request,'allifmaalcommonapp/customers/customers.html',context)
          
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonWantToDeleteCustomer(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonCustomersModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/customers/cust-delete-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)         
##########################################3 ASSETS #####################################
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAssetCategories(request,*allifargs,**allifkwargs):
    try:
        title="Asset Categories"
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonAssetCategoriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonAssetCategoriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonAssetCategoriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonAssetCategoriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
       
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/assets/categories.html',context)
        
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAssetCategorySearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonAssetCategoriesModel.objects.filter((Q(description__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]
        context={
        "title":title,
        "searched_data":searched_data,
     
    }
        return render(request,'allifmaalcommonapp/assets/categories.html',context)
        
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddAssetCategory(request,*allifargs,**allifkwargs):
    try:
        title="Add New Asset Category"
        allif_data=common_shared_data(request)
        form=CommonAddAssetCategoryForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddAssetCategoryForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonAssetCategories',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)

        else:
            form=CommonAddAssetCategoryForm(allif_data.get("main_sbscrbr_entity"))
    
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/assets/add-cat.html',context)
        
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditAssetCategory(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Asset Category Details"
        allif_data=common_shared_data(request)
        allifquery_update=CommonAssetCategoriesModel.objects.filter(id=pk).first()
        form=CommonAddAssetCategoryForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddAssetCategoryForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonAssetCategories',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        
        else:
            form=CommonAddAssetCategoryForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)

        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/assets/add-cat.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAssetCategoryDetails(request,allifslug,*allifargs,**allifkwargs):
    try:
        title="Asset Category Details"
        allifquery=CommonAssetCategoriesModel.objects.filter(pk=allifslug).first()
        context={
            "allifquery":allifquery,
            "title":title,
          
        }
        return render(request,'allifmaalcommonapp/assets/cat-details.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonWantToDeleteAssetCategory(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonAssetCategoriesModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/assets/asset-cat-delete-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)        
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_can_delete  
@logged_in_user_has_departmental_delete
def commonDeleteAssetCategory(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonAssetCategoriesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonAssetCategories',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

    ############################ ASSETS ##########################3
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAssets(request,*allifargs,**allifkwargs):
    try:
        title="Assets"
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonAssetsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonAssetsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonAssetsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonAssetsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]

        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/assets/assets.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAssetSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonAssetsModel.objects.filter((Q(description__icontains=allifsearch)|Q(supplier__name__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]

        context={
        "title":title,
        "searched_data":searched_data,
      
        }
        return render(request,'allifmaalcommonapp/assets/assets.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddAsset(request,*allifargs,**allifkwargs):
    try:
        title="Asset Registration"
        allif_data=common_shared_data(request)
        form=CommonAssetsAddForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAssetsAddForm(allif_data.get("main_sbscrbr_entity"), request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonAssets',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAssetsAddForm(allif_data.get("main_sbscrbr_entity"))
        context={
            "form":form,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/assets/add-asset.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPostAsset(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonAssetsModel.objects.filter(id=pk).first()#very important to get id to go to particular shipment
        supplier_id=allifquery.supplier
        payment_option=allifquery.terms
        asset_value_acc_id=allifquery.asset_account
        cost_value_acc_id=allifquery.cost_account
        asset_total_value=Decimal(allifquery.asset_total_amount)
        asset_posting_status=allifquery.status
        deposit_value=allifquery.deposit
       
        if asset_posting_status=="waiting":
            if str(payment_option)=="Cash": #.....this is hard-coding the db filter.....#
                ##############.... Reduce the cash or cash equivalent account.........########3#####3
                cost_acc_selected=CommonChartofAccountsModel.objects.filter(pk=cost_value_acc_id.id).first()
                initial_cash_balance=cost_acc_selected.balance
                if initial_cash_balance>=asset_total_value:
                    cost_acc_selected.balance=Decimal(initial_cash_balance)-asset_total_value
                    cost_acc_selected.save()

                    ##############.... Increasee the asset account.........########3#####3
                    asset_acc=CommonChartofAccountsModel.objects.filter(pk=asset_value_acc_id.id).first()
                    initial_asset_balance=Decimal(asset_acc.balance)
                    asset_acc.balance=initial_asset_balance+asset_total_value
                    asset_acc.save()

                    ##############.... increase the supplier turnover account.........########3#####3
                    supplier_acc=CommonSuppliersModel.objects.filter(pk=supplier_id.id).first()
                    initial_supplier_turnover=supplier_acc.turnover
                    supplier_acc.turnover=initial_supplier_turnover+asset_total_value
                    supplier_acc.save()
                    allifquery.status="posted"
                    allifquery.save()
                    return redirect('allifmaalcommonapp:commonAssets',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

                    
                else:
                    error_message=f"Sorry, please ensure that there are enough funds in {cost_acc_selected} to pay for {allifquery}"
                    allifcontext={"error_message":error_message,}
                    return render(request,'allifmaalcommonapp/error/error.html',allifcontext)
                  
            elif payment_option=="Deposit": # this means there is partial payment for the asset
                cost_acc_selected=CommonChartofAccountsModel.objects.filter(pk=cost_value_acc_id.id).first()
                initial_cash_balance=cost_acc_selected.balance
                if initial_cash_balance>=deposit_value and deposit_value<asset_total_value:
                    cost_acc_selected.balance=Decimal(initial_cash_balance)-deposit_value
                    cost_acc_selected.save()

                    ##############.... Increasee the asset account.........########3#####3
                    asset_acc=CommonChartofAccountsModel.objects.filter(pk=asset_value_acc_id.id).first()
                    initial_asset_balance=Decimal(asset_acc.balance)
                    asset_acc.balance=initial_asset_balance+asset_total_value
                    asset_acc.save()

                    ##############.... increase the supplier turnover account.........########3#####3
                    supplier_acc=CommonSuppliersModel.objects.filter(pk=supplier_id.id).first()
                    initial_supplier_turnover=supplier_acc.turnover
                    supplier_acc.turnover=initial_supplier_turnover+asset_total_value
                    supplier_initial_balance=supplier_acc.balance
                    supplier_acc.balance=Decimal(supplier_initial_balance)+Decimal(asset_total_value-deposit_value)
                    supplier_acc.save()
                    allifquery.status="posted"
                    allifquery.save()
                    return redirect('allifmaalcommonapp:commonAssets',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

                    
                else:
                    error_message=f"Sorry, please ensure there are enough funds in {cost_acc_selected} to pay for {allifquery} and deposit is not more than total value of the asset"
                    allifcontext={"error_message":error_message,}
                    return render(request,'allifmaalcommonapp/error/error.html',allifcontext)
                    
                
            elif payment_option=="Credit":
                ##############.... increase the asset account.........########3#####3
                asset_acc=CommonChartofAccountsModel.objects.filter(pk=asset_value_acc_id.id).first()
                initial_asset_balance=asset_acc.balance
                asset_acc.balance=initial_asset_balance+asset_total_value
                asset_acc.save()
            
                ############## increase the account payables by creating a positive value in the supplier a/c
                supplier=CommonSuppliersModel.objects.filter(pk=supplier_id.id).first()
                initial_supplier_balance=supplier.balance
                initial_supplier_turnover=supplier.turnover
                supplier.balance=initial_supplier_balance+asset_total_value
                supplier.turnover=initial_supplier_turnover+asset_total_value
                supplier.save()
                allifquery.status="posted"
                allifquery.save()
                return redirect('allifmaalcommonapp:commonAssets',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:# this means that the company is buying the asset on credit terms
                error_message=f"Sorry, correct payment terms"
                allifcontext={"error_message":error_message,}
                return render(request,'allifmaalcommonapp/error/error.html',allifcontext)
            
            
        else:
            error_message=f"Sorry, this is already posted"
            allifcontext={"error_message":error_message,}
            return render(request,'allifmaalcommonapp/error/error.html',allifcontext)
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)  

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditAsset(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonAssetsModel.objects.filter(id=pk).first()
        form=CommonAssetsAddForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery_update)
        title=f"Edit {allifquery_update} Details"

        if request.method=='POST':
            form=CommonAssetsAddForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=allifquery_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonAssets',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAssetsAddForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery_update)

        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/assets/add-asset.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAssetDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonAssetsModel.objects.filter(pk=pk).first()
        title=allifquery

        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/assets/asset-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonWantToDeleteAsset(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonAssetsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/assets/asset-delete-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)            

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin
def commonDeleteAsset(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)

        CommonAssetsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonAssets',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)



############################3 ASSET DEPRECIATIONS #############3



@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin
def commonDepreciateAsset(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
      
        # depreciation = 1/asset_life...if asset life is 2 years, then depr is 1/2 which is 0.5
        # this means the asset will loose 50% each year.
        allifquery=CommonAssetsModel.objects.filter(id=pk).first()
        depreciation_method=allifquery.depreciation
        salvage_value=allifquery.salvage_value
        asset_cost=allifquery.value
        purchase_year=allifquery.acquired.year

        current_date=timezone.now().date()# this gives the daate when you want to know the value of the asset
        acquired_date=allifquery.acquired # this gives the date when the asset was bought
        expiry_date=allifquery.expires # this gives the date when the asset life ends..
        asset_life_in_days=(expiry_date-acquired_date).days# this gives the asset life in days....this is timedelta object
        no_of_days_in_use=(current_date-acquired_date).days
        asset_life_years=Decimal(asset_life_in_days/365)
        no_years_in_use=round((no_of_days_in_use/365),0)
        
        per_day_drop_value=round(((asset_cost-salvage_value)/asset_life_in_days),2)
        total_drop_value=no_of_days_in_use*per_day_drop_value# this will help us to avoid using a for loop for calculating the depreciation.
        annual_drop_value=round((asset_cost-salvage_value)/Decimal(asset_life_years),2)
        annual_depr_rate=round((annual_drop_value/(asset_cost-salvage_value or 1)),2)
        per_year_depr_rate=(asset_cost-salvage_value)/asset_life_years
        allifquery.days_in_use=no_of_days_in_use
        allifquery.asset_life=asset_life_years
        allifquery.save()
        
        if depreciation_method=="Straight-Line":
            date_today=date.today()
            # depr = (purchase_value-salvage_value)/asset_life 
            # or 
            # depr_rate = 1/asset_life
            #depreciable_base = purchase_value-salvage_value
            # annual_depr_value = depr_rate*depreciable_base
            depr_rate=round(1/asset_life_years,2)
            depreciable_base=allifquery.value-allifquery.salvage_value
            annual_depr_value=round(depr_rate*depreciable_base,2)# this can be used with a for loop.
            
            #since we used no_of_days_in_use and per_day_drop_value, we dont have to use a for loop here.
            
            #allifquery.per_day_value_drop=per_day_drop_value
            allifquery.annual_depreciation_rate=round(annual_depr_rate*100,0)
            #allifquery.current_value=Decimal(allifquery.value-total_drop_value)
            #allifquery.depreciated_by=total_drop_value
            
            allifquery.annual_value_drops=annual_depr_value
            allifquery.asset_age=int(no_years_in_use)
            allifquery.current_value=allifquery.value-allifquery.salvage_value
            allifquery.depreciated_by=0
            allifquery.sum_years_digits=0
            allifquery.save()
           
            allifquery.years_depreciated=[]
            allifquery.annual_value_drops=[]
            for year in range(0,int(allifquery.asset_age)+1):# add one so as the current value can be set to salvage when the looping of years is finished
                if allifquery.current_value>salvage_value:
                    allifquery.depreciated_by+=annual_depr_value
                    allifquery.years_depreciated.append(purchase_year+year)
                    allifquery.annual_value_drops.append(annual_depr_value)
                    allifquery.current_value=round(allifquery.current_value-annual_depr_value,2)
                    allifquery.save()
                else:
                    allifquery.current_value=round(allifquery.salvage_value,2)
                    allifquery.save()
                    break
            
            value_drops_list=allifquery.annual_value_drops
            years_depreciated=allifquery.years_depreciated
            context={
            "allifquery":allifquery,
            "value_drops_list":value_drops_list,
            "years_depreciated":years_depreciated,
           
            }
            return render(request,'allifmaalcommonapp/assets/asset-details.html',context)
        
        elif depreciation_method=="Declining-Balance":
            # Declining Balance Depreciation = Book Value x (1 / Useful_Life)..
            allifquery.current_value=allifquery.value
            allifquery.asset_life=int(asset_life_years)
            allifquery.asset_age=int(no_years_in_use)
            allifquery.life=int(asset_life_years)
            allifquery.depreciated_by=0
            allifquery.sum_years_digits=0
            allifquery.per_day_value_drop=0
            allifquery.days_in_use=no_of_days_in_use
            allifquery.save()
            allifquery.years_depreciated=[]
            allifquery.annual_value_drops=[]

            for year in range(0,int(allifquery.asset_age)):
                if allifquery.current_value>salvage_value:
                    value_drop=round(allifquery.current_value/asset_life_years,2)
                    allifquery.current_value=round(allifquery.current_value-value_drop,2)
                    allifquery.depreciated_by+=value_drop
                    allifquery.years_depreciated.append(purchase_year+year)
                    allifquery.annual_value_drops.append(value_drop)
                    allifquery.save()
                   
                else:
                    break
            
            value_drops_list=allifquery.annual_value_drops
            years_depreciated=allifquery.years_depreciated
            context={
            "allifquery":allifquery,
            "value_drops_list":value_drops_list,
            "years_depreciated":years_depreciated,
           
            }
            return render(request,'allifmaalcommonapp/assets/asset-details.html',context)
        
        elif depreciation_method=="Double-Declining-Balance":
            # book value = asset cost - already depreciated/written of value
            # the current/book value should not go below the salvage value.
            # DDB = Book Value x (2 / Useful Life)
            first_year_value_drop=Decimal(2*annual_depr_rate*asset_cost)
            allifquery.current_value=Decimal(allifquery.value)
            allifquery.asset_life=asset_life_years
            allifquery.asset_age=int(no_years_in_use)
            allifquery.annual_depreciation_rate=(annual_depr_rate)*100
            allifquery.depreciated_by=0
            allifquery.sum_years_digits=0
            allifquery.per_day_value_drop=0
            allifquery.save()
           
            allifquery.years_depreciated=[]
            allifquery.annual_value_drops=[]
           
            for year in range(0,int(allifquery.asset_age)):
    
                if allifquery.current_value>salvage_value:
                    per_year_value_drop=round((2*annual_depr_rate*allifquery.current_value),2)
                    allifquery.current_value=Decimal(allifquery.current_value-per_year_value_drop)
                    allifquery.years_depreciated.append(purchase_year+year)
                    allifquery.annual_value_drops.append(per_year_value_drop)
                    allifquery.depreciated_by+=per_year_value_drop
                    allifquery.save()
                else:
                    break

            value_drops_list=allifquery.annual_value_drops
            years_depreciated=allifquery.years_depreciated
            context={
            "allifquery":allifquery,
            "value_drops_list":value_drops_list,
            "years_depreciated":years_depreciated,
           
            }
            return render(request,'allifmaalcommonapp/assets/asset-details.html',context)
        
        elif depreciation_method=="Sum-of-the-Years-Digits":
            
            # we add all digits of the expected life of the asset
            # for instance, if asset life is 5yrs, then sum of the digits will be 1+2+3+4+5 =15
            # we use the depreciable base in all the years, which is asset purchase value - salvage value
            # depr = (asset_life-1/sum_of_digits)*asset_value-salvage_value
            # so first year is
                # depr = (5/15)**asset_value-salvage_value
            # year two, it will be:
                # depr = (4/15)**asset_value-salvage_value
            # it will continue like that untill it is the life years is zero
            allifquery.deposit=allifquery.value-salvage_value

            allifquery.current_value=allifquery.value-salvage_value
            allifquery.sum_years_digits=0
            allifquery.depreciated_by=0
            allifquery.per_day_value_drop=0
            allifquery.asset_life=int(asset_life_years)
            allifquery.asset_age=int(no_years_in_use)
            allifquery.life=int(asset_life_years)
            allifquery.depreciated_by=0
            allifquery.save()
            allifquery.years_depreciated=[]
            allifquery.annual_value_drops=[]
          

            for year in range(1,int(asset_life_years)+1): # get the sum of the digits of the years.
                allifquery.sum_years_digits+=year
                allifquery.save()
              
            for year in range(0,int(no_years_in_use)): # loop through the asset life years
                allifquery.years_depreciated.append(purchase_year+year)
                
                while (int(allifquery.asset_age-year))>0:
                    # formula is : depr = (asset_life-1/sum_of_digits)*asset_value-salvage_value
                    the_value_drop=round((Decimal(allifquery.asset_life-year)/(allifquery.sum_years_digits))*(allifquery.current_value),2)
                    allifquery.asset_life=allifquery.asset_life-1
                    allifquery.depreciated_by+=the_value_drop
                    allifquery.asset_age=allifquery.asset_age-1
                    
                    allifquery.annual_value_drops.append(the_value_drop)
                
                    # add a condition to check that the current asset value does not go below the salvage value
                    if (allifquery.current_value-allifquery.depreciated_by)>allifquery.salvage_value:
                        allifquery.save()
                        continue
                    else:
                        break

            allifquery.current_value=allifquery.value-allifquery.depreciated_by
            allifquery.asset_age=allifquery.asset_age=int(no_years_in_use)
            allifquery.save()
            value_drops_list=allifquery.annual_value_drops
            years_depreciated=allifquery.years_depreciated
            context={
            "allifquery":allifquery,
            "value_drops_list":value_drops_list,
            "years_depreciated":years_depreciated,
            }
            return render(request,'allifmaalcommonapp/assets/asset-details.html',context)
          
        else:
            return redirect('allifmaalcommonapp:commonAssetDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

         
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
############################################### EXPENSES ################################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonExpenses(request,*allifargs,**allifkwargs):
    try:
       
        title="Expenses"
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonExpensesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonExpensesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonExpensesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonExpensesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/expenses/expenses.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddExpense(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Expense Registeration"
        form=CommonExpensesAddForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonExpensesAddForm(allif_data.get("main_sbscrbr_entity"), request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonExpenses',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
               
        context={
            "form":form,
            
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/expenses/add-expense.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
     
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditExpense(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonExpensesModel.objects.filter(pk=pk).first()
        form=CommonExpensesAddForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery)
        title=allifquery
        if request.method=='POST':
            form=CommonExpensesAddForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=allifquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonExpenses',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonExpensesAddForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery)

        context={"title":title,"form":form,"allifquery":allifquery,}
        return render(request,'allifmaalcommonapp/expenses/add-expense.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonExpenseDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonExpensesModel.objects.filter(pk=pk).first()
       
        title="Expense Details"
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/expenses/expense-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteExpense(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonExpensesModel.objects.filter(id=pk).first()
        message="Are u sure to delete"
        context={
        "message":message,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/expenses/delete-exp-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
@logged_in_user_is_admin  
def commonDeleteExpense(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonExpensesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonExpenses',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonExpenseSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonExpensesModel.objects.filter((Q(description__icontains=allifsearch)|Q(amount__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        
        else:
            searched_data=[]

        context={
        
        "title":title,
        
        "searched_data":searched_data,
        
      
        }
        return render(request,'allifmaalcommonapp/expenses/expenses.html',context)
        
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPostExpense(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
    
        payment=CommonExpensesModel.objects.filter(id=pk).first()#very important to get id to go to particular shipment
        myamount=payment.amount#this gives the initial account
        credit_acc=payment.supplier
        debit_acc=payment.expense_account
        
        if (credit_acc and myamount)!=None:

            #credit the suppllier account...
            mycust=CommonSuppliersModel.objects.filter(id=credit_acc.id).first()
            initial_cust_acc_bal=mycust.balance
            mycust.balance= Decimal(initial_cust_acc_bal)+Decimal(myamount)
            mycust.save()

             # debit the expense account since an new expense is incurred... expense account increases.
            coa_acc=CommonChartofAccountsModel.objects.filter(id=debit_acc.id).first()
            initial_coa_acc_bal=coa_acc.balance
            coa_acc.balance= Decimal(initial_coa_acc_bal)+Decimal(myamount)
            coa_acc.save()
            
            payment.status="posted"
            payment.save()
            return redirect('allifmaalcommonapp:commonExpenses',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

        else:
            return render(request,'allifmaalapp/error.html')
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

############################## STTART OF ORDERS SECTION... ###################################3
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTransactions(request,*allifargs,**allifkwargs):
    try:
        title="Transactions"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
       
        no_of_quotes=CommonTransactionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).count()
        no_of_prospects=CommonTransactionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).count()
        prospects=CommonTransactionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:7]
        total_value_of_prospects=CommonTransactionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonTransactionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonTransactionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonTransactionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonTransactionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "no_of_quotes":no_of_quotes,
            "prospects":prospects,
            "no_of_prospects":no_of_prospects,
            "total_value_of_prospects":total_value_of_prospects,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request, 'allifmaalcommonapp/transactions/transactions.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonNewTransaction(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
       
        ###### start... UID generation ##################
        allifquery=CommonTransactionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        allifuid=str(nmbr)+"/"+str(unque)
        ###### End... UID generation ##################

        if allifquery:
            nmbr='TRANS'+"/"+str(allifuid)
        else:
            nmbr= 'TRANS/1'+"/"+str(uuid4()).split('-')[2]

        number=CommonTransactionsModel.objects.create(trans_number=nmbr,company=allif_data.get("main_sbscrbr_entity"),owner=allif_data.get("usernmeslg"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        number.save()
        return redirect('allifmaalcommonapp:commonTransactions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteTransaction(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonTransactionsModel.objects.filter(id=pk).first()
        title="Are u sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/transactions/delete_trans_confirm.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonDeleteTransaction(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonTransactionsModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonTransactions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
from allifmaalshaafiapp.models import *
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddTransactionDetails(request,pk,*allifargs,**allifkwargs):
    try:
       
        title="Transaction Details"
        
        allif_data=common_shared_data(request)
    
        allifquery=CommonTransactionsModel.objects.filter(id=pk).first()
        triages=TriagesModel.objects.filter(medical_file=allifquery)
        form=CommonAddTransactionDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
        if request.method == 'POST':
            form=CommonAddTransactionDetailsForm(allif_data.get("main_sbscrbr_entity"),request.POST,request.FILES,instance=allifquery)
            if form.is_valid():
                form.save()
                return redirect('allifmaalcommonapp:commonAddTransactionDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddTransactionDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)

        context={
            "form":form,
            "allifquery":allifquery,
            "title":title,
            "triages":triages,
            #"transaction_obj":allifquery, # <--- PASS THE CORRECT OBJECT HERE
           
        }
        return render(request,'allifmaalcommonapp/transactions/transaction_details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddTransactionItems(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Transaction Items"
        allif_data=common_shared_data(request)
       
        allifquery=CommonTransactionsModel.objects.filter(id=pk).first()
      
        form=CommonAddTransactionItemForm(allif_data.get("main_sbscrbr_entity"))
        allifqueryset=CommonTransactionItemsModel.objects.filter(trans_number=allifquery)#this line helps to
    
        if request.method=='POST':
            form=CommonAddTransactionItemForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.trans_number=allifquery
                obj.save()
                return redirect('allifmaalcommonapp:commonAddTransactionItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddTransactionItemForm(allif_data.get("main_sbscrbr_entity"))

        context={
        "form":form,
        "allifquery":allifquery,
        
        "allifqueryset":allifqueryset,
        "title":title, 
     
        }
        return render(request,'allifmaalcommonapp/transactions/add_trans_items.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditTransactionItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Item Details"
        allif_data=common_shared_data(request)
        myquery=CommonTransactionItemsModel.objects.filter(id=pk).first()
        allifquery=myquery.trans_number
        allifqueryset=CommonTransactionItemsModel.objects.filter(trans_number=allifquery)

        form=CommonAddTransactionItemForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)
        if request.method=='POST':
            form=CommonAddTransactionItemForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=myquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.trans_number=allifquery
                obj.save()
                return redirect('allifmaalcommonapp:commonAddTransactionItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddTransactionItemForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)

        context={"title":title,"form":form,"allifquery":allifquery,
                 "allifqueryset":allifqueryset,"myquery":myquery,}
        return render(request,'allifmaalcommonapp/transactions/add_trans_items.html',context)
        
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
   
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDeleteTransactionItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Delete Transaction Items"
        allif_data=common_shared_data(request)
       
        myallifquery=CommonTransactionItemsModel.objects.filter(id=pk).first()
        myquery=myallifquery.trans_number
        myallifquery.delete()
        return redirect('allifmaalcommonapp:commonAddTransactionItems',pk=myquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTransactionToPdf(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        date_today=date.today()
       
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        allifquery=CommonTransactionsModel.objects.filter(id=pk).first()
        allifqueryset=CommonTransactionItemsModel.objects.filter(trans_number=allifquery)
        title="Transaction "+str(allifquery)
        template_path = 'allifmaalcommonapp/transactions/transaction_pdf.html'
        context = {
        "allifqueryset":allifqueryset,
        "allifquery":allifquery,
        "title":title,
        "scopes":scopes,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        "usr_var":allif_data.get("usernmeslg"),
        "date_today":date_today,
            }
        
        response = HttpResponse(content_type='application/pdf')
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = f'filename="{allifquery} Quote.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTransactionsSearch(request,*allifargs,**allifkwargs):
    try: 
        title="Search Results"
        allif_data=common_shared_data(request)
       
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonTransactionsModel.objects.filter((Q(trans_number__icontains=allifsearch)|Q(comments__icontains=allifsearch)|Q(trans__trans_number__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            
        }
        return render(request, 'allifmaalcommonapp/transactions/transactions.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTransactionAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Quotes Search"
        allif_data=common_shared_data(request)
       
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonTransactionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
        lastDate=CommonTransactionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
        largestAmount=CommonTransactionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-total').first().total
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonTransactionsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(total__gte=start_value or 0) & Q(total__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/quotes/quote-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                   "datashorts":datasorts,
                   "formats":formats,
                   "scopes":scopes,
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="transactions-advanced-searched-results.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                # if excel is selected
                
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                   
                    }
                    return render(request, 'allifmaalcommonapp/transactions/transactions.html',context)
                    
            else:
                searched_data=[]
             
                context={
            "searched_data":searched_data,
                }
                return render(request, 'allifmaalcommonapp/transactions/transactions.html',context)
           
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request, 'allifmaalcommonapp/transactions/transactions.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

##############3 Spaces################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin
def commonSpaces(request,allifusr,allifslug,*allifargs,**allifkwargs):
    title="Spaces"
    try:
        
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonSpacesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonSpacesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonSpacesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonSpacesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={"title":title,"allifqueryset":allifqueryset,}
        return render(request,'allifmaalcommonapp/spaces/spaces.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
@logged_in_user_is_admin
def commonAddSpace(request,allifusr,allifslug,*allifargs,**allifkwargs):
    title="Add New Space"
    try:
        allif_data=common_shared_data(request)
        form=CommonAddSpaceForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddSpaceForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSpaces',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
               
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSpaceForm(allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/spaces/add-space.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_is_admin
def commonEditSpace(request,allifusr,pk,*allifargs,**allifkwargs):
    title="Update Space Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonSpacesModel.objects.filter(id=pk).first()
        form=CommonAddSpaceForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddSpaceForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSpaces',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSpaceForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/spaces/add-space.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def commonSpaceDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Space Details"
        allifquery=CommonSpacesModel.objects.filter(id=pk).first()
        allifqueryset=CommonSpaceUnitsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),space=allifquery)
        
        context={
            "allifquery":allifquery,
            "title":title,
            "allifqueryset":allifqueryset,
           
        }
        return render(request,'allifmaalcommonapp/spaces/space-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_departmental_delete
@logged_in_user_can_delete
def commonWantToDeleteSpace(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonSpacesModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/spaces/delete-space-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_universal_delete
@logged_in_user_can_delete
def commonDeleteSpace(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonSpacesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonSpaces',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


################################ SPACE UNITS....####################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin
def commonSpaceUnits(request,allifusr,allifslug,*allifargs,**allifkwargs):
    title="Space Units"
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonSpaceUnitsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonSpaceUnitsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonSpaceUnitsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonSpaceUnitsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={"title":title,"allifqueryset":allifqueryset,}
        return render(request,'allifmaalcommonapp/spaces/units/space_units.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
@logged_in_user_is_admin
def commonAddSpaceUnit(request,allifusr,allifslug,*allifargs,**allifkwargs):
    title="Add New Space Unit"
    try:
        allif_data=common_shared_data(request)
        form=CommonAddSpaceUnitForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddSpaceUnitForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSpaceUnits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
               
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSpaceUnitForm(allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/spaces/units/add_space_unit.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_is_admin
def commonEditSpaceUnit(request,allifusr,pk,*allifargs,**allifkwargs):
    title="Update Space Unit Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonSpaceUnitsModel.objects.filter(id=pk).first()
        form=CommonAddSpaceUnitForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddSpaceUnitForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSpaceUnits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSpaceUnitForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/spaces/units/add_space_unit.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonSpaceUnitSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonSpaceUnitsModel.objects.filter((Q(description__icontains=allifsearch)|Q(space_number__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        
        else:
            searched_data=[]

        context={
        
        "title":title,
        "searched_data":searched_data,
        
        }
        return render(request,'allifmaalcommonapp/spaces/units/space_units.html',context)
        
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def commonSpaceUnitDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Space Unit Details"
        allifquery=CommonSpaceUnitsModel.objects.filter(id=pk).first()
      
        context={
            "allifquery":allifquery,
            "title":title,
          
        }
        return render(request,'allifmaalcommonapp/spaces/units/space_unit_details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_departmental_delete
@logged_in_user_can_delete
def commonWantToDeleteSpaceUnit(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonSpacesModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/spaces/units/delete_space_unit_confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_universal_delete
@logged_in_user_can_delete
def commonDeleteSpaceUnit(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonSpaceUnitsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonSpaceUnits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

######################## space booking items... #####################3

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonSpaceBookings(request,pk,*allifargs,**allifkwargs):
    try:
        
        allif_data=common_shared_data(request)
       
        allifquery=CommonTransactionsModel.objects.filter(id=pk).first()
        title=str(allifquery) +" - "+ "Space Alloctions"
        allifqueryset=CommonSpaceBookingItemsModel.objects.filter(trans_number=allifquery)#this line helps to
    
        context={
       
        "allifquery":allifquery,
        
        "allifqueryset":allifqueryset,
        "title":title, 
     
        }
        return render(request,'allifmaalcommonapp/booking/space_bookings.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddSpaceBookingItems(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Space Allocations"
        allif_data=common_shared_data(request)
       
        allifquery=CommonTransactionsModel.objects.filter(id=pk).first()
      
        form=CommonAddSpaceBookingItemForm(allif_data.get("main_sbscrbr_entity"))
        allifqueryset=CommonSpaceBookingItemsModel.objects.filter(trans_number=allifquery)#this line helps to

        total=0
        for items in allifqueryset:
            total+=items.space_allocation_amount
        allifquery.amount=total
        allifquery.save()
        
        
        if request.method=='POST':
            form=CommonAddSpaceBookingItemForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.trans_number=allifquery
                obj.save()
                return redirect('allifmaalcommonapp:commonAddSpaceBookingItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSpaceBookingItemForm(allif_data.get("main_sbscrbr_entity"))

        context={
        "form":form,
        "allifquery":allifquery,
        
        "allifqueryset":allifqueryset,
        "title":title, 
     
        }
        return render(request,'allifmaalcommonapp/booking/add_space_booking.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditSpaceBookingItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Item Details"
        allif_data=common_shared_data(request)
        myquery_update=CommonSpaceBookingItemsModel.objects.filter(id=pk).first()
        allifquery=myquery_update.trans_number
        allifqueryset=CommonSpaceBookingItemsModel.objects.filter(trans_number=allifquery)

        form=CommonAddSpaceBookingItemForm(allif_data.get("main_sbscrbr_entity"), instance=myquery_update)
        if request.method=='POST':
            form=CommonAddSpaceBookingItemForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=myquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.save()
                return redirect('allifmaalcommonapp:commonAddSpaceBookingItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSpaceBookingItemForm(allif_data.get("main_sbscrbr_entity"), instance=myquery_update)

        context={"title":title,"form":form,"allifquery":allifquery,
                 "allifqueryset":allifqueryset,"myquery_update":myquery_update,}
        return render(request,'allifmaalcommonapp/booking/add_space_booking.html',context)
      
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonSpaceAllocationPdf(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        date_today=date.today()
       
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        allifquery=CommonTransactionsModel.objects.filter(id=pk).first()
        allifqueryset=CommonSpaceBookingItemsModel.objects.filter(trans_number=allifquery)
        title="Space Allocations For "+" "+str(allifquery)
        template_path = 'allifmaalcommonapp/booking/space_allocation_pdf.html'
        context = {
        "allifqueryset":allifqueryset,
        "allifquery":allifquery,
        "title":title,
        "scopes":scopes,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        "usr_var":allif_data.get("usernmeslg"),
        "date_today":date_today,
            }
        
        response = HttpResponse(content_type='application/pdf')
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = f'filename="{allifquery} space_allocation.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDeleteSpaceBookingItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Delete Transaction Items"
        allif_data=common_shared_data(request)
       
        myallifquery=CommonSpaceBookingItemsModel.objects.filter(id=pk).first()
        myquery=myallifquery.trans_number
        myallifquery.delete()
        return redirect('allifmaalcommonapp:commonAddSpaceBookingItems',pk=myquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)  
    
################### inventory/stock###########3
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonStocks(request,*allifargs,**allifkwargs):
    try:
        title="Stock And Inventory"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
      
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-quantity')
            
                if allif_data.get("logged_in_user_has_universal_access")==True:
                    allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
                elif allif_data.get("logged_in_user_has_divisional_access")==True:
                    allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
                elif allif_data.get("logged_in_user_has_branches_access")==True:
                    allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
                elif allif_data.get("logged_in_user_has_departmental_access")==True:
                    allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
                else:
                    allifqueryset=[]
            else:
                if allif_data.get("logged_in_user_has_universal_access")==True:
                    allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
                elif allif_data.get("logged_in_user_has_divisional_access")==True:
                    allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
                elif allif_data.get("logged_in_user_has_branches_access")==True:
                    allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
                elif allif_data.get("logged_in_user_has_departmental_access")==True:
                    allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
                else:
                    allifqueryset=[]
                
        else:
            if allif_data.get("logged_in_user_has_universal_access")==True:
                allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
            elif allif_data.get("logged_in_user_has_divisional_access")==True:
                allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
            elif allif_data.get("logged_in_user_has_branches_access")==True:
                allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
            elif allif_data.get("logged_in_user_has_departmental_access")==True:
                allifqueryset=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
            else:
                allifqueryset=[]
        
        
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request,'allifmaalcommonapp/stocks/stocks.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
from datetime import datetime
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddStockItem(request,*allifargs,**allifkwargs):
    try:
        title="Add Stock Item"
        allif_data=common_shared_data(request)
    
        sector=str(allif_data.get("main_sbscrbr_entity").sector)

        ###### start... UID generation ##################
        allifquery=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        currntyear=timezone.now().date().today()
        allifuid=str(nmbr)+"/"+str(currntyear)+"/"+str(unque)
        ###### End... UID generation ##################
        
        form=CommonStockItemAddForm(allif_data.get("main_sbscrbr_entity"))
        
        if request.method=='POST':
            form=CommonStockItemAddForm(allif_data.get("main_sbscrbr_entity"), request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                #obj.uid=allifuid
                obj.save()
                return redirect('allifmaalcommonapp:commonStocks',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            pass

        context={
            "form":form,
            "sector":sector,
        
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/stocks/add-stock.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditStockItem(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonStocksModel.objects.filter(id=pk).first()
        form=CommonStockItemAddForm(allif_data.get("main_sbscrbr_entity"), instance= allifquery_update)
        title="Edit Stock Item Details"
        if request.method=='POST':
            form=CommonStockItemAddForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance= allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonStocks',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonStockItemAddForm(allif_data.get("main_sbscrbr_entity"), instance= allifquery_update)

        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/stocks/add-stock.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
     
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonStockItemDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonStocksModel.objects.filter(pk=pk).first()
        title=allifquery
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/stocks/stock-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonStockItemSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonStocksModel.objects.filter((Q(description__icontains=allifsearch)|Q(partNumber__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        
        else:
            searched_data=[]

        context={
        
        "title":title,
        "searched_data":searched_data,
        
        }
        return render(request,'allifmaalcommonapp/stocks/stocks.html',context)
        
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonStockItemAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Stock Items Advanced Search Results"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()

        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        current_date=timezone.now().date().today()
        firstDate=current_date
        lastDate=current_date
        largestAmount=0
        searched_data=[]
        firstDepo=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first()
    
        lastDepo=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if firstDepo and lastDepo:
            firstDate=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
            lastDate=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
            largestAmount=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-quantity').first().quantity
        else:
            firstDate=current_date
            lastDate=current_date
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonStocksModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(quantity__gte=start_value or 0) & Q(quantity__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/stocks/stock-item-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                    "scopes":scopes,
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="stock-items-advanced-searched-results.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
              
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                    "formats":formats,
                    "title":title,
                     "scopes":scopes
                    }
                    return render(request,'allifmaalcommonapp/stocks/stocks.html',context)
                    
            else:
                searched_data=[]
             
            context={
           
            "formats":formats,
            "title":title,
             "scopes":scopes
            }
            return render(request,'allifmaalcommonapp/banks/withdrawals/withdrawals.html',context)
           
        else:
            context={
           
            "formats":formats,
            "title":title,
             "scopes":scopes
            }
            return render(request,'allifmaalcommonapp/banks/withdrawals/withdrawals.html',context)
          
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)      

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteStockItem(request,pk,*allifargs,**allifkwargs):
    try:
      
        allifquery=CommonStocksModel.objects.filter(id=pk).first()
        title="Are u sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/stocks/x-stock-item-cnfrm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_can_delete   
@logged_in_user_has_departmental_delete
def commonDeleteStockItem(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonStocksModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonStocks',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)



############################# STOCK PURCHASE ORDERS #####################################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPurchaseOrders(request,*allifargs,**allifkwargs):
    try:
        title="Purchases & Purchase Orders"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]

        context={
           
            "title":title,
          "formats":formats,
          "datasorts":datasorts,
            "allifqueryset":allifqueryset,

        }
        return render(request,'allifmaalcommonapp/purchases/purchaseorders.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonNewPurchaseOrder(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        ###### start... UID generation ##################
        allifquery=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        currntyear=timezone.now().date().today().year
        allifuid=str(nmbr)+"/"+str(currntyear)+"/"+str(unque)
        ###### End... UID generation ##################print()
        
        if allifquery:
            purchaseNumber='PO'+"/"+str(allifuid)
        else:
            purchaseNumber= 'PO/1'+"/"+str(currntyear)+"/"+str(uuid4()).split('-')[2]

        newPurchaseOrder= CommonPurchaseOrdersModel.objects.create(po_number=purchaseNumber,company=allif_data.get("main_sbscrbr_entity"),owner=allif_data.get("usernmeslg"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        newPurchaseOrder.save()
        return redirect('allifmaalcommonapp:commonPurchaseOrders',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeletePO(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first()
        title="Are u sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/purchases/x-po-cnfrm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonDeletePO(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonPurchaseOrdersModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonPurchaseOrders',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddPODetails(request,pk,*allifargs,**allifkwargs):
    title="Add Purchase Order Details"
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first()
        misc_costs=CommonPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=allifquery)
        form=CommonPOAddForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
        if request.method=='POST':
            #add_shipment_items_form=AddShippmentItemsForm(request.POST)
            form=CommonPOAddForm(allif_data.get("main_sbscrbr_entity"),request.POST,request.FILES,instance=allifquery)
            if form.is_valid():
                form.save()
                return redirect('allifmaalcommonapp:commonAddPODetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonPOAddForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)


        context={
            
            "form":form,
           "misc_costs":misc_costs,
            "allifquery":allifquery,
            "title":title,
            

        }
        return render(request,'allifmaalcommonapp/purchases/add-po-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddPOItems(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add items to the purchase order"
        allif_data=common_shared_data(request)
     
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first()
        allifqueryset=CommonPurchaseOrderItemsModel.objects.filter(po_item_con=allifquery).order_by('-date')
        queryset=CommonPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=allifquery)
        # calculate po total of items and taxes
      
        po_total=0
        po_tax_amount=0
        for items in allifqueryset:
            po_total+=items.purchase_order_amount
            po_tax_amount+=items.po_tax_amount
        # calculate misc costs
        miscCostotal=0
        for cost in queryset:
            miscCostotal+=cost.purchase_order_misc_cost
        # now assing the values to various columns/attributes
        allifquery.amount=po_total
        allifquery.taxamount=po_tax_amount
        allifquery.amounttaxincl=po_total+po_tax_amount
        allifquery.misccosts=miscCostotal
        allifquery.grandtotal=po_total+po_tax_amount+miscCostotal

        allifquery.save()
       
      
        form=CommonPOItemAddForm(allif_data.get("main_sbscrbr_entity"))
        add_item= None
        if request.method == 'POST':
            form=CommonPOItemAddForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.po_item_con=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddPOItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonPOItemAddForm(allif_data.get("main_sbscrbr_entity"))

        context={
                "form":form,
                "title":title,
                "allifquery":allifquery,
                
                "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/purchases/add-po-items.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonWantToDeletePOItem(request,pk,*allifargs,**allifkwargs):
    title="Are u sure to delete"
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first()#very important to get id to go to particular shipment
        myallifquery=CommonPurchaseOrderItemsModel.objects.filter(id=pk).first()
        allifquery=myallifquery.po_item_con
        form=CommonPOItemAddForm(allif_data.get("main_sbscrbr_entity"))
        allifqueryset=CommonPurchaseOrderItemsModel.objects.filter(po_item_con=allifquery).order_by('-date')
       
        add_item= None
        if request.method == 'POST':
            form=CommonPOItemAddForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.po_item_con=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddPOItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonPOItemAddForm(allif_data.get("main_sbscrbr_entity"))

        
        context={
        "title":title,
        "allifquery":allifquery,
        "form":form,
        "allifqueryset":allifqueryset,
        "myallifquery":myallifquery,
        }
        return render(request,'allifmaalcommonapp/purchases/add-po-items.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonEditPOItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Item Details"
        allif_data=common_shared_data(request)
        sector=str(allif_data.get("main_sbscrbr_entity").sector)
        myquery=CommonPurchaseOrderItemsModel.objects.filter(id=pk).first()
        allifquery=myquery.po_item_con
        allifqueryset=CommonPurchaseOrderItemsModel.objects.filter(po_item_con=allifquery).order_by('-date')

        form=CommonPOItemAddForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)
        if request.method=='POST':
            form=CommonPOItemAddForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=myquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.save()
                return redirect('allifmaalcommonapp:commonAddPOItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonPOItemAddForm(allif_data.get("main_sbscrbr_entity"),instance=myquery)
                
         
        context={"title":title,"form":form,"sector":sector,"allifquery":allifquery,
                 "allifqueryset":allifqueryset,"myquery":myquery,}
        return render(request,'allifmaalcommonapp/purchases/add-po-items.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonDeletePOItem(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonPurchaseOrderItemsModel.objects.filter(id=pk).first()
        allifqueryPOId=allifquery.po_item_con.id
        allifquery.delete()
        return redirect('allifmaalcommonapp:commonAddPOItems',pk=allifqueryPOId,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPOMiscCost(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add PO Misc. Costs"
        allif_data=common_shared_data(request)
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first() #very important to get id to go to particular shipment
        form=CommonPOMiscCostAddForm(allif_data.get("main_sbscrbr_entity"))
        allifqueryset= CommonPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=allifquery)#this line helps to
        
        
        queryset=CommonPurchaseOrderItemsModel.objects.filter(po_item_con=allifquery)
        allifqueryset=CommonPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=allifquery).order_by('-date')
        # calculate po total of items and taxes
        po_total=0
        po_tax_amount=0
        for items in queryset:
            po_total+=items.quantity*items.unitcost
            tax=(items.items.taxrate.taxrate/100)
            po_tax_amount+=items.quantity*items.unitcost*tax
        # calculate misc costs
        miscCostotal=0
        for cost in allifqueryset:
            miscCostotal+=cost.purchase_order_misc_cost
        # now assing the values to various columns/attributes
        allifquery.amount=po_total
        allifquery.taxamount=po_tax_amount
        allifquery.amounttaxincl=po_total+po_tax_amount
        allifquery.misccosts=miscCostotal
        allifquery.grandtotal=po_total+po_tax_amount+miscCostotal
        allifquery.save()


        add_item= None
        if request.method == 'POST':
            form=CommonPOMiscCostAddForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.po_misc_cost_con=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonPOMiscCost',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)

        context={
                "form":form,
                "title":title,
                "allifquery":allifquery,
                "allifqueryset":allifqueryset,
               
        }
        return render(request,'allifmaalcommonapp/purchases/add-po-misc-costs.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCalculatePOMiscCosts(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first() #very important to get id to go to particular shipment
        allifqueryset=CommonPurchaseOrderItemsModel.objects.filter(po_item_con=allifquery)
        queryset= CommonPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=allifquery)#this line helps to
        
        # calculate po total of items and taxes
        po_total=0
        po_tax_amount=0
        for items in allifqueryset:
            po_total+=items.quantity*items.unitcost
            tax=(items.items.taxrate.taxrate/100)
            po_tax_amount+=items.quantity*items.unitcost*tax
       
        # calculate misc costs
        miscCostotal=0
        for cost in queryset:
            miscCostotal+=cost.purchase_order_misc_cost
        
        # now assing the values to various columns/attributes
        allifquery.amount=po_total
        allifquery.taxamount=po_tax_amount
        allifquery.misccosts=miscCostotal
        allifquery.grandtotal=po_total+po_tax_amount+miscCostotal
        allifquery.save()
        return redirect('allifmaalcommonapp:commonAddPODetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPOMiscCostDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Misc Cost Details"
        allifquery=CommonPurchaseOrderMiscCostsModel.objects.get(id=pk)
        context={
            "title":title,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/purchases/misc-cost-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDeleteMiscCost(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        queryobj=CommonPurchaseOrderMiscCostsModel.objects.filter(id=pk).first()
        mainparent=queryobj.po_misc_cost_con.id
        queryobj.delete()
        return redirect('allifmaalcommonapp:commonPOMiscCost',pk=mainparent,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonEditPOMiscCostDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Misc. Cost Details"
        allif_data=common_shared_data(request)
        queryobj=CommonPurchaseOrderMiscCostsModel.objects.filter(id=pk).first()
        allifquery=queryobj.po_misc_cost_con
        form=CommonPOMiscCostAddForm(allif_data.get("main_sbscrbr_entity"),instance=queryobj)
        if request.method == 'POST':
            #add_shipment_items_form=AddShippmentItemsForm(request.POST)
            form=CommonPOMiscCostAddForm(allif_data.get("main_sbscrbr_entity"),request.POST,request.FILES,instance=queryobj)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.po_misc_cost_con=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonPOMiscCost',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonPOMiscCostAddForm(allif_data.get("main_sbscrbr_entity"),instance=queryobj)

        context={
            
            "form":form,
          "allifquery":allifquery,
            "title":title,
            "queryobj":queryobj,
    
        }
        return render(request,'allifmaalcommonapp/purchases/add-po-misc-costs.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPostPO(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first()
        po_amount=allifquery.amount or 1
        po_amount_taxinclusve=allifquery.amounttaxincl
        applied_uplift=allifquery.uplift
        po_misccosts=allifquery.misccosts
       
        # post the po amount including tax into the supplier account
        po_supplier=allifquery.supplier
        if po_supplier!=None:
            suplr_initial_balance=po_supplier.balance
            suplr_intial_turnover=po_supplier.turnover
            po_supplier.balance=suplr_initial_balance+po_amount_taxinclusve
            po_supplier.turnover=suplr_intial_turnover+po_amount_taxinclusve
            po_supplier.save()
            CommonLedgerEntriesModel.objects.create(supplier=po_supplier,credit=po_amount_taxinclusve,
        comments="purchase",company=allif_data.get("main_sbscrbr_entity"),owner=request.user,ledgowner="supplier")
        else:
            return HttpResponse("Please fill the missing fields")
           
       
        ################# ...start of  misc costs...credit the service provider account....###################
        misc_costs=CommonPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=allifquery)
       
        if misc_costs!=None:
            for cost in misc_costs:
                spent_amount=cost.purchase_order_misc_cost
                misc_cost_supplier_id=int(cost.supplier.id)
                misc_cost_supplier=CommonSuppliersModel.objects.filter(pk=misc_cost_supplier_id).first()# The misc cost service supplier
                supplier_acc_balance=misc_cost_supplier.balance
                supplier_acc_turnover=misc_cost_supplier.turnover
                misc_cost_supplier.balance=supplier_acc_balance-spent_amount
                misc_cost_supplier.turnover=supplier_acc_turnover+spent_amount
                misc_cost_supplier.save()
            
        ################### end of misc costs ###############
    
      
        if allifquery.posting_po_status=="waiting":
            allifquery.posting_po_status="posted"
            allifquery.save()
        else:
            allifquery.posting_po_status="waiting"
            allifquery.save()
        
        poItems =CommonPurchaseOrderItemsModel.objects.filter(po_item_con=allifquery)
        for item in poItems:

            # apportion the misc costs to each unit
            item_unit_cost=item.unitcost#this gets the new unit buying price of the individual items from the po
            quantity=item.quantity#this gets the quantity of the individual items
            tax=(item.items.taxrate.taxrate/100)
            po_tax_amount=item.quantity*item.unitcost*tax
            
            #apportioned unit cost = ((unit cost)/total_PO_value)*total_misc_cost
            apportioned_misc_unit_cost=(item_unit_cost/po_amount)*po_misccosts
            actual_item_unit_cost=apportioned_misc_unit_cost+item_unit_cost
            
            
            #we need to calculate the weighted unit cost
            #products=CommonStocksModel.objects.filter(description=item.items).first()
            products=CommonStocksModel.objects.filter(pk=item.items.id).first()
            existing_item_unit_quantity=item.items.quantity# this gives the quantities for existing items in the system
            total_new_quantity=existing_item_unit_quantity+quantity# this gives the sum of existing quantities and those in the po.
            existing_item_unit_cost=item.items.unitcost# this gives the unit cost for existing items in the system
            weighted_new_unit_cost=(existing_item_unit_cost*existing_item_unit_quantity+quantity*actual_item_unit_cost)/Decimal(total_new_quantity or 1)
            products.unitcost=weighted_new_unit_cost
            products.standardUnitCost=item.items.unitcost
            products.quantity=total_new_quantity
            
            
            # deal with buying price --- get weighted buying price
            existing_item_unit_buying_price=item.items.buyingPrice
            weighted_new_buying_price=(existing_item_unit_buying_price*existing_item_unit_quantity+quantity*item_unit_cost)/(total_new_quantity or 1)
            products.buyingPrice=weighted_new_buying_price

            # .... set the selling price .......
            products.unitPrice=applied_uplift*weighted_new_unit_cost
            products.save()

            
            #....... debit item inventory account .............
            inventory_acc_id=item.items.inventory_account
            if inventory_acc_id !=None:
                inventory_acc=CommonChartofAccountsModel.objects.filter(pk=inventory_acc_id.id).first()
                item_initial_inventory_account_balance=inventory_acc.balance
                item_new_inventory_account_balance = item_initial_inventory_account_balance + actual_item_unit_cost*quantity+po_tax_amount
                inventory_acc.balance=item_new_inventory_account_balance
                inventory_acc.save()
            
            else:
                messgeone=messages.error(request, 'Seems that the items do not have inventory accounts specified')
                messge=messages.error(request, 'Make sure every item has inventory account added')
                return render(request,'allifmaalcommonapp/error/error.html')
        
        return redirect('allifmaalcommonapp:commonAddPODetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPOToPdf(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        title="Purchase Order"
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first()
        po_suplier=allifquery.supplier
        allifqueryset=CommonPurchaseOrderItemsModel.objects.filter(po_item_con=allifquery)
        template_path = 'allifmaalcommonapp/purchases/po-pdf.html'
        context = {
        "allifqueryset":allifqueryset,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        "title":title,
        "po_suplier":po_suplier,
        "scopes":scopes,
        "allifquery":allifquery,
        "system_user":allif_data.get("usernmeslg"),
        
        }
        
        response = HttpResponse(content_type='application/pdf')
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = f'filename="{allifquery}/P.O.pdf"'
        template = get_template(template_path)
        html=template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
    ##################################33 our customers ###################################3
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPOSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonPurchaseOrdersModel.objects.filter((Q(po_number__icontains=allifsearch)|Q(amount__icontains=allifsearch)|Q(supplier__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]
        context={
        "title":title,
        
        "searched_data":searched_data,
        
    }
        return render(request,'allifmaalcommonapp/purchases/purchaseorders.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPOAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Purchase Order Advanced Search Results"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
        lastDate=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
        largestAmount=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-amount').first().amount

        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]

        current_date=timezone.now().date().today()
        firstDate=current_date
        lastDate=current_date
        largestAmount=0
        searched_data=[]
        firstDepo=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first()
    
        lastDepo=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if firstDepo and lastDepo:
            firstDate=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
            lastDate=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
            largestAmount=CommonPurchaseOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-amount').first().amount
        else:
            firstDate=current_date
            lastDate=current_date

        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonPurchaseOrdersModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/purchases/po-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                   "datashorts":datasorts,
                   "formats":formats,
                   "scopes":scopes,
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="purchase-order-advanced-searched-results.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                # if excel is selected
                
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                   
                    }
                    return render(request,'allifmaalcommonapp/purchases/purchaseorders.html',context)
                    
            else:
                searched_data=[]
              
                context={
                    "searched_data":searched_data,
            
                }
                return render(request,'allifmaalcommonapp/purchases/purchaseorders.html',context)
           
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/purchases/purchaseorders.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#################################### INTER COMAPNY STOCK TRANSFERS #####################

 ######################33 ADD WAREHOUSE ITEMS ###################
################### inventory/stock###########3
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonSpaceItems(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonSpacesModel.objects.filter(id=pk,company=allif_data.get("main_sbscrbr_entity")).first()
        title="Stock And Inventory"+str(allifquery)
        
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=CommonSpaceItemsModel.objects.filter(space=allifquery)
      
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/spaces/items/space-items.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddSpaceItems(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonSpacesModel.objects.filter(id=pk).first()
        allifqueryset=CommonSpaceItemsModel.objects.filter(space=allifquery)
        
        title="Add items"+str(allifquery)
        form=CommonAddSpaceItemForm(allif_data.get("main_sbscrbr_entity"))
        if request.method == 'POST':
            form=CommonAddSpaceItemForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.space=allifquery
                obj.save()
                return redirect('allifmaalcommonapp:commonAddSpaceItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSpaceItemForm(allif_data.get("main_sbscrbr_entity"))

        context={
                "form":form,
                "title":title,
                "allifquery":allifquery,
                
                "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/spaces/items/add-space-items.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonEditSpaceItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Item Details"
        allif_data=common_shared_data(request)
        sector=str(allif_data.get("main_sbscrbr_entity").sector)
        myquery=CommonSpaceItemsModel.objects.filter(id=pk).first()
        allifquery=myquery.space
        allifqueryset=CommonSpaceItemsModel.objects.filter(space=allifquery).order_by('-items')

        form=CommonAddSpaceItemForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)
        if request.method=='POST':
            form=CommonAddSpaceItemForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=myquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.save()
                return redirect('allifmaalcommonapp:commonAddSpaceItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSpaceItemForm(allif_data.get("main_sbscrbr_entity"),instance=myquery)
                
         
        context={"title":title,"form":form,"sector":sector,"allifquery":allifquery,
                 "allifqueryset":allifqueryset,"myquery":myquery,}
        return render(request,'allifmaalcommonapp/spaces/items/add-space-items.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonDeleteSpaceItem(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonSpaceItemsModel.objects.filter(id=pk).first()
        allifquery_id=allifquery.space.id
        allifquery.delete()
        return redirect('allifmaalcommonapp:commonAddSpaceItems',pk=allifquery_id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

############################## TRANSFER ORDERS #######################
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTransferOrders(request,*allifargs,**allifkwargs):
    try:
        title="Transfer Orders"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
       
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonStockTransferOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonStockTransferOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonStockTransferOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonStockTransferOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            
            "prospects":prospects,
           
            "formats":formats,

            "datasorts":datasorts,
        }
        return render(request, 'allifmaalcommonapp/stocks/transfers/transfer-orders.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonNewTransferOrder(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
       
        ###### start... UID generation ##################
        allifquery=CommonStockTransferOrdersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        currntyear=timezone.now().date().today().year
        allifuid=str(nmbr)+"/"+str(unque)
        ###### End... UID generation ##################

        if allifquery:
            sqnmbr='TRNSF/ORD'+"/"+str(allifuid)
        else:
            sqnmbr= 'TRNSF/ORD/1'+"/"+str(uuid4()).split('-')[2]

        newQuoteNumber=CommonStockTransferOrdersModel.objects.create(number=sqnmbr,company=allif_data.get("main_sbscrbr_entity"),owner=allif_data.get("usernmeslg"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        newQuoteNumber.save()
        return redirect('allifmaalcommonapp:commonTransferOrders',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteTransferOrder(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonStockTransferOrdersModel.objects.filter(id=pk).first()
        title="Are u sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/stocks/Transfers/delete-transfer-order-confirm.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonDeleteTransferOrder(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonStockTransferOrdersModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonTransferOrders',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddTransferOrderDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Transfer Order Details"
        allif_data=common_shared_data(request)
       
        allifquery=CommonStockTransferOrdersModel.objects.filter(id=pk).first()
        allifqueryset=CommonStockTransferOrderItemsModel.objects.filter(trans_ord_items_con=allifquery)
        form=CommonAddTransferOrderDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
        if request.method=='POST':
            form=CommonAddTransferOrderDetailsForm(allif_data.get("main_sbscrbr_entity"),request.POST,request.FILES,instance=allifquery)
            if form.is_valid():
                form.save()
                return redirect('allifmaalcommonapp:commonAddTransferOrderDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddTransferOrderDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)

        context={
            "form":form,
            "allifquery":allifquery,
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/stocks/transfers/add-transfer-order-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddTransferOrderItems(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Transfer Order Items"
        allif_data=common_shared_data(request)
       
        allifquery=CommonStockTransferOrdersModel.objects.filter(id=pk).first()
        allifquery.from_store
        
        #form=CommonAddTransferOrderItemForm(allif_data.get("main_sbscrbr_entity"))
        allifqueryset=CommonStockTransferOrderItemsModel.objects.filter(trans_ord_items_con=allifquery)#this line helps to
        #myitems=CommonWarehouseItemsModel.objects.filter(items__items=allifquery.from_store)
        #myitems=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        form=CommonAddTransferOrderItemForm(allif_data.get("main_sbscrbr_entity"))
        #form=CommonAddTransferOrderItemForm(allifquery.from_store)
        add_item= None
        if request.method=='POST':
            form=CommonAddTransferOrderItemForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.trans_ord_items_con=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddTransferOrderItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            pass
            #form=CommonAddTransferOrderItemForm(allif_data.get("main_sbscrbr_entity"))

        context={
        "form":form,
        "allifquery":allifquery,
        
        "allifqueryset":allifqueryset,
        "title":title, 
       
        }
        return render(request,'allifmaalcommonapp/stocks/transfers/add-transfer-order-item.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditTransferOrderItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Transfer Order Item Details"
        allif_data=common_shared_data(request)
        myquery=CommonStockTransferOrderItemsModel.objects.filter(id=pk).first()
        allifquery=myquery.trans_ord_items_con
        allifqueryset=CommonStockTransferOrderItemsModel.objects.filter(trans_ord_items_con=allifquery).order_by('-date')

        form=CommonAddTransferOrderItemForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)
        if request.method=='POST':
            form=CommonAddTransferOrderItemForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=myquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.save()
                return redirect('allifmaalcommonapp:commonAddTransferOrderItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddTransferOrderItemForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)

        context={"title":title,"form":form,"allifquery":allifquery,
                 "allifqueryset":allifqueryset,"myquery":myquery,}
        return render(request,'allifmaalcommonapp/stocks/transfers/add-transfer-order-item.html',context)
        
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDeleteTransferOrderItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Delete Transfer Order Items"
        allif_data=common_shared_data(request)
       
        myallifquery=CommonStockTransferOrderItemsModel.objects.filter(id=pk).first()
        myquery=myallifquery.trans_ord_items_con
        myallifquery.delete()
        return redirect('allifmaalcommonapp:commonAddTransferOrderItems',pk=myquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTransferOrderPdf(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        date_today=date.today()
       
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        allifquery=CommonStockTransferOrdersModel.objects.filter(id=pk).first()
        allifqueryset=CommonStockTransferOrderItemsModel.objects.filter(trans_ord_items_con=allifquery)
        title="TRNSF/ORD "+str(allifquery)
        template_path = 'allifmaalcommonapp/stocks/transfers/transfer-order-pdf.html'
        context = {
        "allifqueryset":allifqueryset,
        "allifquery":allifquery,
        "title":title,
        "scopes":scopes,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        "usr_var":allif_data.get("usernmeslg"),
        "date_today":date_today,
            }
        
        response = HttpResponse(content_type='application/pdf')
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = f'filename="{allifquery} Quote.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTransferOrdersSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
       
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonStockTransferOrdersModel.objects.filter((Q(number__icontains=allifsearch)|Q(to_store__name__icontains=allifsearch)|Q(from_store__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            
        }
        return render(request, 'allifmaalcommonapp/stocks/transfers/transfer-orders.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
  
# In your views.py file (e.g., allifmaalcommonapp/views.py)

from django.db import transaction # Import this at the top
from django.db.models import F # Import F for atomic updates
from django.contrib import messages # For user feedback messages
from decimal import Decimal # Ensure Decimal is imported for calculations

# ... (other imports and functions like common_shared_data, decorators) ...

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view # Assuming this permission allows posting transfers
def commonPostTransferOrder(request, pk, *allifargs, **allifkwargs):
    try:
        allif_data=common_shared_data(request)
        transfer_order=CommonStockTransferOrdersModel.objects.filter(id=pk,company=allif_data.get("main_sbscrbr_entity")).first()
        transfer_items=CommonStockTransferOrderItemsModel.objects.filter(trans_ord_items_con=transfer_order)

        # Check if the transfer order is already posted/completed
        if transfer_order.status=='posted': # Adjust status string if yours is different
            messages.warning(request,"Sorry, this was posted")
            return redirect('allifmaalcommonapp:commonAddTransferOrderDetails', pk=transfer_order.id, allifusr=allif_data.get("usrslg"), allifslug=allif_data.get("compslg"))

        elif not transfer_items.exists():
            return redirect('allifmaalcommonapp:commonAddTransferOrderItems', pk=transfer_order.id, allifusr=allif_data.get("usrslg"), allifslug=allif_data.get("compslg"))
        
        # Ensure source and destination stores are selected on the Transfer Order
        elif not transfer_order.from_store or not transfer_order.to_store:
            messages.error(request, "Please add both source and destination locations before posting.")
            return redirect('allifmaalcommonapp:commonAddTransferOrderDetails', pk=transfer_order.id, allifusr=allif_data.get("usrslg"), allifslug=allif_data.get("compslg"))
        
        # Prevent transfer to/from the same store
        elif transfer_order.from_store == transfer_order.to_store:
            messages.error(request, "Source and destination must be different")
            return redirect('allifmaalcommonapp:commonAddTransferOrderDetails', pk=transfer_order.id, allifusr=allif_data.get("usrslg"), allifslug=allif_data.get("compslg"))

        with transaction.atomic():
            for item_line in transfer_items:
                if str(item_line.items.partNumber) in str(CommonSpaceItemsModel.objects.filter(items__partNumber=item_line.items.partNumber,warehouse=transfer_order.from_store).values_list('items__partNumber')):
                    if str(item_line.items.partNumber) in str(CommonSpaceItemsModel.objects.filter(items__partNumber=item_line.items.partNumber,warehouse=transfer_order.to_store).values_list('items__partNumber')):
                        item=CommonSpaceItemsModel.objects.filter(items=item_line.items,warehouse=transfer_order.from_store).first()
                        initial_stock_quanty=item.quantity
                        
                        if item_line.quantity<initial_stock_quanty:
                            item.quantity=Decimal(initial_stock_quanty)-Decimal(item_line.quantity)
                            item.save()
                            item=CommonSpaceItemsModel.objects.filter(items=item_line.items,warehouse=transfer_order.to_store).first()
                            initial_stock_quanty=item.quantity
                            print(initial_stock_quanty)
                            item.quantity=Decimal(initial_stock_quanty)+Decimal(item_line.quantity)
                            item.save()
                        else:
                            messages.error(request, f"'{item_line.items.partNumber}' is not enough in {transfer_order.from_store.name}")
                            return redirect('allifmaalcommonapp:commonAddTransferOrderDetails', pk=transfer_order.id, allifusr=allif_data.get("usrslg"), allifslug=allif_data.get("compslg"))

                    else:
                        destination_stock_item,created=CommonSpaceItemsModel.objects.get_or_create(
                        warehouse=transfer_order.to_store, # The destination warehouse
                        items=item_line.items,
                        quantity=item_line.quantity,

                        #you can add default values as below... system will pick these over actual
                        #defaults={ # These defaults are used ONLY if a new record is created
                        #'items': item_line.items,
                        #'quantity': Decimal('00.00'), # New items start with 0 quantity before adding transferred amount
                        #}
                        )

                        item=CommonSpaceItemsModel.objects.filter(items=item_line.items,warehouse=transfer_order.from_store).first()
                        print(item)
                        initial_stock_quanty=item.quantity
                        print(initial_stock_quanty)
                        item.quantity=Decimal(initial_stock_quanty)-Decimal(item_line.quantity)
                        item.save()
                        messages.error(request, f"'{item_line.items.partNumber}' is not in {transfer_order.to_store.name}")
                   
                else:
                    messages.error(request, f"'{item_line.items.partNumber}' is not in {transfer_order.from_store.name}")
                    return redirect('allifmaalcommonapp:commonAddTransferOrderDetails', pk=transfer_order.id, allifusr=allif_data.get("usrslg"), allifslug=allif_data.get("compslg"))
            
              
            return redirect('allifmaalcommonapp:commonAddTransferOrderDetails', pk=transfer_order.id, allifusr=allif_data.get("usrslg"), allifslug=allif_data.get("compslg"))
           
    except ValueError as ve: # Catch custom validation errors (like insufficient stock)
        messages.error(request, str(ve))
        # Redirect back to the details page with the error
        return redirect('allifmaalcommonapp:commonAddTransferOrderDetails', pk=transfer_order.id, allifusr=allif_data.get("usrslg"), allifslug=allif_data.get("compslg"))

    except Exception as ex:
        # Catch any other unexpected errors and display a generic error message
        error_context = {'error_message': ex}
        return render(request, 'allifmaalcommonapp/error/error.html', error_context)
######################### QUOTATION #########################
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonQuotes(request,*allifargs,**allifkwargs):
    try:
        title="Quotations"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
       
        no_of_quotes=CommonQuotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).count()
        no_of_prospects=CommonQuotesModel.objects.filter(prospect="Likely",company=allif_data.get("main_sbscrbr_entity")).count()
        prospects=CommonQuotesModel.objects.filter(prospect='Likely',company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:7]
        total_value_of_prospects=CommonQuotesModel.objects.filter(prospect="Likely",company=allif_data.get("main_sbscrbr_entity")).aggregate(Sum('total'))['total__sum']
        
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonQuotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonQuotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonQuotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonQuotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "no_of_quotes":no_of_quotes,
            "prospects":prospects,
            "no_of_prospects":no_of_prospects,
            "total_value_of_prospects":total_value_of_prospects,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request, 'allifmaalcommonapp/quotes/quotes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonNewQuote(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
       
        ###### start... UID generation ##################
        allifquery=CommonQuotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        currntyear=timezone.now().date().today().year
        allifuid=str(nmbr)+"/"+str(unque)
        ###### End... UID generation ##################

        if allifquery:
            sqnmbr='SQ'+"/"+str(allifuid)
        else:
            sqnmbr= 'SQ/1'+"/"+str(uuid4()).split('-')[2]

        newQuoteNumber= CommonQuotesModel.objects.create(number=sqnmbr,company=allif_data.get("main_sbscrbr_entity"),owner=allif_data.get("usernmeslg"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        newQuoteNumber.save()
        return redirect('allifmaalcommonapp:commonQuotes',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteQuote(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonQuotesModel.objects.filter(id=pk).first()
        title="Are u sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/quotes/x-qt-confrm.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonDeleteQuote(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonQuotesModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonQuotes',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddQuoteDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Quote Details"
        allif_data=common_shared_data(request)
       
        allifquery=CommonQuotesModel.objects.filter(id=pk).first()
        form=CommonAddQuoteDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
        if request.method == 'POST':
            form=CommonAddQuoteDetailsForm(allif_data.get("main_sbscrbr_entity"),request.POST,request.FILES,instance=allifquery)
            if form.is_valid():
                form.save()
                return redirect('allifmaalcommonapp:commonAddQuoteDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddQuoteDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)

        context={
            "form":form,
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/quotes/add-quote-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddQuoteItems(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Quote Items"
        allif_data=common_shared_data(request)
       
        allifquery=CommonQuotesModel.objects.filter(id=pk).first()
        allif_qte_discount=allifquery.discount
        form=CommonAddQuoteItemsForm(allif_data.get("main_sbscrbr_entity"))
        allifqueryset= CommonQuoteItemsModel.objects.filter(allifquoteitemconnector=allifquery)#this line helps to
        allifquerysettotal=0
        allifqerytotalafterdiscount=0
        qte_line_tax=0
        discounttoal=0
        if len(allifqueryset)>0:
            for line in allifqueryset:
                allifquerysettotal+=line.quote_selling_price
                allifqerytotalafterdiscount+=line.quote_selling_price_with_discount
                discounttoal+=line.quote_selling_price-line.quote_selling_price_with_discount
                qte_line_tax+=line.quote_tax_amount
        
        allifquery.total=allifquerysettotal
        allifquery.taxAmount=qte_line_tax
        allifquery.discountAmount=discounttoal
        allifquery.totalwithdiscount=allifquerysettotal-discounttoal
        allifquery.grandtotal=Decimal(allifquerysettotal-discounttoal)+Decimal(qte_line_tax)
        allifquery.save()

        add_item= None
        if request.method=='POST':
            form=CommonAddQuoteItemsForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.allifquoteitemconnector=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddQuoteItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddQuoteItemsForm(allif_data.get("main_sbscrbr_entity"))

        context={
        "form":form,
        "allifquery":allifquery,
        "allifquerysettotal":allifquerysettotal,
        "allifqueryset":allifqueryset,
        "title":title, 
        "allif_qte_discount":allif_qte_discount,
        }
        return render(request,'allifmaalcommonapp/quotes/add-quote-items.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditQuoteItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Item Details"
        allif_data=common_shared_data(request)
        myquery=CommonQuoteItemsModel.objects.filter(id=pk).first()
        allifquery=myquery.allifquoteitemconnector
        allifqueryset=CommonQuoteItemsModel.objects.filter(allifquoteitemconnector=allifquery).order_by('-date')

        form=CommonAddQuoteItemsForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)
        if request.method=='POST':
            form=CommonAddQuoteItemsForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=myquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.save()
                return redirect('allifmaalcommonapp:commonAddQuoteItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddQuoteItemsForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)

        context={"title":title,"form":form,"allifquery":allifquery,
                 "allifqueryset":allifqueryset,"myquery":myquery,}
        return render(request,'allifmaalcommonapp/quotes/add-quote-items.html',context)
        
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonWantToDeleteQuoteItem(request,pk,*allifargs,**allifkwargs): 
    try:
        allif_data=common_shared_data(request)
        
        form=CommonAddQuoteItemsForm(allif_data.get("main_sbscrbr_entity"))
        myallifquery=CommonQuoteItemsModel.objects.filter(id=pk).first()
        myquery=myallifquery.allifquoteitemconnector
        allifquery=myallifquery.allifquoteitemconnector
        allifqueryset= CommonQuoteItemsModel.objects.filter(allifquoteitemconnector=myquery)#this li
        title="Are u sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        "myallifquery":myallifquery,
        "allifqueryset":allifqueryset,
        "form":form,
        }
        return render(request,'allifmaalcommonapp/quotes/add-quote-items.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDeleteQuoteItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Delete Quote Items"
        allif_data=common_shared_data(request)
       
        myallifquery=CommonQuoteItemsModel.objects.filter(id=pk).first()
        myquery=myallifquery.allifquoteitemconnector
        myallifquery.delete()
        return redirect('allifmaalcommonapp:commonAddQuoteItems',pk=myquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonQuoteToPdf(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        date_today=date.today()
       
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        allifquery=CommonQuotesModel.objects.filter(id=pk).first()
        allifqueryset=CommonQuoteItemsModel.objects.filter(allifquoteitemconnector=allifquery)
        title="Quote "+str(allifquery)
        template_path = 'allifmaalcommonapp/quotes/quote-pdf.html'
        context = {
        "allifqueryset":allifqueryset,
        "allifquery":allifquery,
        "title":title,
        "scopes":scopes,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        "usr_var":allif_data.get("usernmeslg"),
        "date_today":date_today,
            }
        
        response = HttpResponse(content_type='application/pdf')
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = f'filename="{allifquery} Quote.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

###########3 quote search 
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonSearchAjaxQuote(request,*allifargs,**allifkwargs):
    try:
        title="Data dynamic search"
        if request.method=="GET":
            data_from_front_end=request.GET.get('search_result_key')
            if (data_from_front_end!=None):
                allifquery= list(CommonQuotesModel.objects.filter( 
                    Q(number__icontains=data_from_front_end)|Q(customer__name__icontains=data_from_front_end)).values("number","id","total","customer__name"))
                
                #allifquery= list(AllifmaalQuotesModel.objects.filter(
                    #Q(customer__icontains=data_from_front_end) | 
                    #Q(number__icontains=data_from_front_end)).values("customer","number"))
                return JsonResponse(allifquery, safe=False)
            else:
                pass
                
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonQuotesSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
       
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonQuotesModel.objects.filter((Q(number__icontains=allifsearch)|Q(total__icontains=allifsearch)|Q(customer__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            
        }
        return render(request, 'allifmaalcommonapp/quotes/quotes.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonQuoteAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Quotes Search"
        allif_data=common_shared_data(request)
       
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonQuotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
        lastDate=CommonQuotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
        largestAmount=CommonQuotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-total').first().total
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonQuotesModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(total__gte=start_value or 0) & Q(total__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/quotes/quote-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                   "datashorts":datasorts,
                   "formats":formats,
                   "scopes":scopes,
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="quotes-advanced-searched-results.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                # if excel is selected
                
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                   
                    }
                    return render(request, 'allifmaalcommonapp/quotes/quotes.html',context)
                    
            else:
                searched_data=[]
             
                context={
            "searched_data":searched_data,
                }
                return render(request, 'allifmaalcommonapp/quotes/quotes.html',context)
           
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request, 'allifmaalcommonapp/quotes/quotes.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
########################### END OF QUOTATION ###############


##########################3 INVOICES #######################333
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonInvoices(request,*allifargs,**allifkwargs):
    try:
        title="Invoices"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
       
        no_invoices=CommonInvoicesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).count()
        #last_invoices=CommonInvoicesModel.objects.order_by('invoice_number')[:6]
        #latest_paid_invoices=CommonInvoicesModel.objects.filter(invoice_status='Paid').order_by('-date')[:7]
        #posted_invoices_total_value=CommonInvoicesModel.objects.filter(posting_inv_status="posted").aggregate(Sum('invoice_total'))['invoice_total__sum']
        
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonInvoicesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonInvoicesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonInvoicesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonInvoicesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]

        context={
        #"last_invoices":last_invoices,
        "title":title,
        "no_invoices":no_invoices,
        #"posted_invoices_total_value":posted_invoices_total_value,
        #"latest_paid_invoices":latest_paid_invoices,
        "allifqueryset":allifqueryset,
        "formats":formats,
        "datasorts":datasorts,
            
        }

        return render(request,'allifmaalcommonapp/invoices/invoices.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonNewInvoice(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
       
        ###### start... UID generation ##################
        allifquery=CommonInvoicesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        currntyear=timezone.now().date().today().year
        allifuid=str(nmbr)+"/"+str(unque)
        ###### End... UID generation ##################

        if allifquery:
            invnmbr='Inv'+"/"+str(allifuid)
        else:
            invnmbr= 'Inv/1'+"/"+str(currntyear)+"/"+str(uuid4()).split('-')[2]

        newinv= CommonInvoicesModel.objects.create(number=invnmbr,company=allif_data.get("main_sbscrbr_entity"),owner=allif_data.get("usernmeslg"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        newinv.save()
        return redirect('allifmaalcommonapp:commonInvoices',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonWantToDeleteInvoice(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonInvoicesModel.objects.filter(id=pk).first()
        
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        
        }
        return render(request,'allifmaalcommonapp/invoices/x-inv-confrm.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDeleteInvoice(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        
        CommonInvoicesModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonInvoices',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddInvoiceDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Invoice Details"
        allif_data=common_shared_data(request)
        
        allifquery=CommonInvoicesModel.objects.filter(id=pk).first()
        form=CommonAddInvoiceDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
        if request.method=='POST':
            form=CommonAddInvoiceDetailsForm(allif_data.get("main_sbscrbr_entity"),request.POST,request.FILES,instance=allifquery)
            if form.is_valid():
                form.save()
                return redirect('allifmaalcommonapp:commonAddInvoiceDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddInvoiceDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)

        context={
            "form":form,
            "title":title,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/invoices/add-invoice-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddInvoiceItems(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Invoice Items "
        allif_data=common_shared_data(request)
      
        allifquery=CommonInvoicesModel.objects.filter(id=pk).first()
        form=CommonAddInvoiceItemsForm(allif_data.get("main_sbscrbr_entity"))
        allifqueryset= CommonInvoiceItemsModel.objects.filter(allifinvitemconnector=allifquery)#this line helps to
        allifquerysettotal=0
        allifqerytotalafterdiscount=0
        invoice_line_tax=0
        discounttoal=0
        invitemscost=0
        
        if len(allifqueryset)>0:
            for line in allifqueryset:
                allifquerysettotal+=line.invoice_selling_price
                allifqerytotalafterdiscount+=line.invoice_selling_price_with_discount
                discounttoal+=line.invoice_selling_price-line.invoice_selling_price_with_discount
                invoice_line_tax+=line.invoice_tax_amount
                invitemscost+=line.description.unitcost
                


        allifquery.total=allifquerysettotal
        allifquery.taxAmount=invoice_line_tax
        allifquery.discountAmount=discounttoal
        allifquery.totalwithdiscount=allifquerysettotal-discounttoal
        allifquery.grandtotal=Decimal(allifquerysettotal-discounttoal)+Decimal(invoice_line_tax)
        allifquery.invoice_items_total_cost=invitemscost
        allifquery.invoice_gross_profit=Decimal(allifquerysettotal-discounttoal or 0)-Decimal(invitemscost or 0)
        allifquery.save()

        add_item= None
        if request.method=='POST':
            form=CommonAddInvoiceItemsForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.allifinvitemconnector=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddInvoiceItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            pass

        context={
    
                "form":form,
            
                "allifqueryset":allifqueryset,
                "title":title,
                "allifquery":allifquery,
               
        }
        return render(request,'allifmaalcommonapp/invoices/add-inv-items.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonEditInvoiceItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Invoice Item Details"
        allif_data=common_shared_data(request)
        
        myquery=CommonInvoiceItemsModel.objects.filter(id=pk).first()
        allifquery=myquery.allifinvitemconnector
        allifqueryset=CommonInvoiceItemsModel.objects.filter(allifinvitemconnector=allifquery).order_by('-date')

        form=CommonAddInvoiceItemsForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)
        if request.method=='POST':
            form=CommonAddInvoiceItemsForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=myquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.save()
                return redirect('allifmaalcommonapp:commonAddInvoiceItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            myquery=CommonInvoiceItemsModel.objects.filter(id=pk).first()
            allifquery=myquery.allifinvitemconnector
            allifqueryset=CommonInvoiceItemsModel.objects.filter(allifinvitemconnector=allifquery).order_by('-date')
            form=CommonAddInvoiceItemsForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)
     
        context={"title":title,"form":form,"allifquery":allifquery,
                 "allifqueryset":allifqueryset,"myquery":myquery,}
        return render(request,'allifmaalcommonapp/invoices/add-inv-items.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteInvoiceItem(request,pk,*allifargs,**allifkwargs): 
    try:
        allif_data=common_shared_data(request)
        form=CommonAddInvoiceItemsForm(allif_data.get("main_sbscrbr_entity"))
        myallifquery=CommonInvoiceItemsModel.objects.filter(id=pk).first()
        myquery=myallifquery.allifinvitemconnector
        allifquery=myallifquery.allifinvitemconnector
        allifqueryset= CommonInvoiceItemsModel.objects.filter(allifinvitemconnector=myquery)#this li
        title="Are u sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        "myallifquery":myallifquery,
        "form":form,
        }
        return render(request,'allifmaalcommonapp/invoices/add-inv-items.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDeleteInvoiceItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Quote Items"
        allif_data=common_shared_data(request)
       
        myallifquery=CommonInvoiceItemsModel.objects.filter(id=pk).first()
        myquery=myallifquery.allifinvitemconnector
        myallifquery.delete()
        return redirect('allifmaalcommonapp:commonAddInvoiceItems',pk=myquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPostInvoice(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
       
        allifqueryset=CommonBanksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
       
        allifquery=CommonInvoicesModel.objects.filter(id=pk).first()#very important to get id to go to particular shipment
        allifqueryset=CommonInvoiceItemsModel.objects.filter(allifinvitemconnector=allifquery)
        myinvid=allifquery.id
        customer=allifquery.customer
        amount=allifquery.total
        
        initial_rating=allif_data.get("usernmeslg").peformance_counter
        allif_data.get("usernmeslg").peformance_counter=Decimal(initial_rating)+Decimal(1)
        allif_data.get("usernmeslg").save()

        if customer:
            customer_id=customer.id
            for item in allifqueryset:
                invo_quantity=item.quantity # this gives the quantities in the invoice
                invoice_item_id=item.description.id #this gives the IDs of the invoice item in the main AllifmaalStocksModel database.
                per_line_cost_price=item.description.unitcost*item.quantity
                per_line_selling_price=item.description.unitPrice*item.quantity
                if item.description.inventory_account !=None:
                    inventory_acc_id=item.description.inventory_account.id
                    expense_acc_id=item.description.expense_account.id
                    income_acc_id=item.description.income_account.id
                    
                    products=CommonStocksModel.objects.filter(pk=invoice_item_id,company=allif_data.get("main_sbscrbr_entity")).first()
                    initial_item_quantity=products.quantity
                    products.quantity=initial_item_quantity-invo_quantity # reduce stock by invoice quantity
                    initial_sales_rate=products.total_units_sold
                    products.total_units_sold=Decimal(initial_sales_rate)+Decimal(1)
                    products.save()

                    # ....... debit the inventory account ..........
                    inv_acc=CommonChartofAccountsModel.objects.filter(pk=inventory_acc_id,company=allif_data.get("main_sbscrbr_entity")).first()
                    initial_inv_bal=inv_acc.balance
                    inv_acc.balance=initial_inv_bal-per_line_cost_price
                    inv_acc.save()

                   
                    # ....... record the revenue in the income account ..........
                    income_acc=CommonChartofAccountsModel.objects.filter(pk=income_acc_id,company=allif_data.get("main_sbscrbr_entity")).first()
                    initial_income_bal=income_acc.balance
                    income_acc.balance=initial_income_bal + per_line_selling_price
                    income_acc.save()

                    # ....... record the Cost of goods sold ..........
                    cost_goods_sold_acc_exist=CommonChartofAccountsModel.objects.filter(description="COGS",company=allif_data.get("main_sbscrbr_entity"),department=allif_data.get("logged_user_department")).first()
                    if cost_goods_sold_acc_exist:

                        cost_goods_sold_acc=CommonChartofAccountsModel.objects.filter(description="COGS",company=allif_data.get("main_sbscrbr_entity"),department=allif_data.get("logged_user_department")).first()
                        initial_cost_of_goods_sold_balance=cost_goods_sold_acc.balance
                        cost_goods_sold_acc.balance=initial_cost_of_goods_sold_balance+per_line_cost_price
                        cost_goods_sold_acc.save()
                    else:
                        return HttpResponse("COGS A/C is not added")
                else:
                    return HttpResponse("Please ensure invoice details are filled and that all items have been linked to the Chart of Accounts")

                    

                #increase customer turnover
                mycustomer=CommonCustomersModel.objects.filter(pk=customer_id,company=allif_data.get("main_sbscrbr_entity"),department=allif_data.get("logged_user_department")).first()
                initial_customer_acc_turnover=mycustomer.turnover or 0
               
                mycustomer.turnover=initial_customer_acc_turnover+item.description.unitPrice
                initial_customer_acc_balance=mycustomer.balance or 0
                mycustomer.balance=initial_customer_acc_balance+item.description.unitPrice

                mycustomer.save()
             
                #transaction=AllifmaalCustomerStatementModel.objects.create(customer=customer,debit=inv_total,
                        #comments="Invoice",balance=initial_customer_acc_balance+inv_total)#get the ord
            

                # ......... credit the equity account .........
                equity_acc=CommonChartofAccountsModel.objects.filter(description="Equity",company=allif_data.get("main_sbscrbr_entity"),department=allif_data.get("logged_user_department")).first()
                if equity_acc:
                    initial_equity_account_balance=equity_acc.balance
                    equity_acc.balance=initial_equity_account_balance + item.description.unitPrice-item.description.unitcost
                    equity_acc.save()
                else:
                    return HttpResponse("Please add equity account")
                   

                ######## change invoice status
                allifquery.posting_inv_status="posted"
                allifquery.save()

            # ....... record the gross profit ..........
                gross_profit_acc_exist=CommonChartofAccountsModel.objects.filter(description="Gross Profit",company=allif_data.get("main_sbscrbr_entity"),department=allif_data.get("logged_user_department")).first()
                if gross_profit_acc_exist:

                    profit_and_loss_acc=CommonChartofAccountsModel.objects.filter(description="Gross Profit",company=allif_data.get("main_sbscrbr_entity"),department=allif_data.get("logged_user_department")).first()
                    initial_profit_and_loss_balance=profit_and_loss_acc.balance
                    profit_and_loss_acc.balance=initial_profit_and_loss_balance+item.description.unitPrice-item.description.unitcost
                    profit_and_loss_acc.save()
                    
                else:
                    return HttpResponse("Please add profit account")
                   
        else:
            return HttpResponse("Please select a customer")
            
        CommonLedgerEntriesModel.objects.create(customer=customer,credit=amount,
        comments="invoice",company=allif_data.get("main_sbscrbr_entity"),owner=request.user,ledgowner="customer")
        return redirect('allifmaalcommonapp:commonAddInvoiceDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPostedInvoices(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        posted_invoices=CommonInvoicesModel.objects.filter(posting_inv_status="posted")
        posted_invoices_count=CommonInvoicesModel.objects.filter(posting_inv_status="posted").count()
        last_invoices=CommonInvoicesModel.objects.filter(posting_inv_status="posted").order_by('-invoice_total')[:7]
        
        title="Posted Invoices"
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
       
        allifqueryset=CommonInvoicesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        no_invoices=CommonInvoicesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).count()
        context={
            "posted_invoices":posted_invoices,
            "title":title,
            "last_invoices":last_invoices,
            "posted_invoices_count":posted_invoices_count,
            "allifqueryset":allifqueryset,
            "datasorts":datasorts,
            "formats":formats,

        }
        return render(request,'allifmaalcommonapp/invoices/posted-invoices.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonInvoiceToPdf(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
    
        date_today=date.today()
       
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        allifquery=CommonInvoicesModel.objects.filter(id=pk).first()
        allifqueryset=CommonInvoiceItemsModel.objects.filter(allifinvitemconnector=allifquery)
        title="Invoice "+str(allifquery)
        template_path = 'allifmaalcommonapp/invoices/invoice-pdf.html'
        context = {
        "allifqueryset":allifqueryset,
        "allifquery":allifquery,
        "title":title,
        "scopes":scopes,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        "usr_var":allif_data.get("usernmeslg"),
        "date_today":date_today,
            }
        
        response = HttpResponse(content_type='application/pdf')
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = f'filename="{allifquery} Invoice.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#########3 invoice search #####
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonSearchAjaxInvoice(request,*allifargs,**allifkwargs):
    try:
   
        if request.method=="GET":
            data_from_front_end=request.GET.get('search_result_key')
          
            if (data_from_front_end!=None):
                allifquery= list(CommonInvoicesModel.objects.filter( 
                    Q(invoice_number__icontains=data_from_front_end)).values("invoice_number","id","customer__name","invoice_total"))
                
                #allifquery= list(AllifmaalQuotesModel.objects.filter(
                    #Q(customer__icontains=data_from_front_end) | 
                    #Q(number__icontains=data_from_front_end)).values("customer","number"))
                return JsonResponse(allifquery, safe=False)
            else:
                allifquery=CommonInvoicesModel.objects.all()
                return JsonResponse(allifquery, safe=False)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonInvoicesSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
      
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonInvoicesModel.objects.filter((Q(number__icontains=allifsearch)|Q(total__icontains=allifsearch)|Q(customer__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]

        context={
        "title":title,
        "allifsearch":allifsearch,
        "searched_data":searched_data,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        }
        return render(request,'allifmaalcommonapp/invoices/invoices.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonInvoiceAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Invoices Advanced Search"
        allif_data=common_shared_data(request)
       
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonInvoicesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
        lastDate=CommonInvoicesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
        largestAmount=CommonInvoicesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-total').first().total
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonInvoicesModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(total__gte=start_value or 0) & Q(total__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/invoices/invoice-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                   "datasorts":datasorts,
                   "formats":formats,
                   "scopes":scopes,
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="Invoices-advanced-searched-result.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
              
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/invoices/invoices.html',context)
                 
            else:
                allifqueryset=CommonQuotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
         
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/invoices/invoices.html',context)
           
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/invoices/invoices.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

##########################3 credit Notes ######################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCreditNotes(request,*allifargs,**allifkwargs):
    try:
        
        title="Credit Notes"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
       
        no_invoices=CommonCreditNotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).count()
      
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonCreditNotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonCreditNotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonCreditNotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonCreditNotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]

        context={
        #"last_invoices":last_invoices,
        "title":title,
        "no_invoices":no_invoices,
        #"posted_invoices_total_value":posted_invoices_total_value,
        #"latest_paid_invoices":latest_paid_invoices,
        "allifqueryset":allifqueryset,
        "formats":formats,
        "datasorts":datasorts,
            
        }

        return render(request,'allifmaalcommonapp/creditnotes/credit-notes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonNewCreditNote(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
       
        ###### start... UID generation ##################
        allifquery=CommonCreditNotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        currntyear=timezone.now().date().today().year
        allifuid=str(nmbr)+"/"+str(currntyear)+"/"+str(unque)
        ###### End... UID generation ##################

        if allifquery:
            invnmbr='CRD/NTE'+"/"+str(allifuid)
        else:
            invnmbr= 'CRD/NTE/1'+"/"+str(currntyear)+"/"+str(uuid4()).split('-')[2]

        newinv=CommonCreditNotesModel.objects.create(number=invnmbr,company=allif_data.get("main_sbscrbr_entity"),owner=allif_data.get("usernmeslg"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        newinv.save()
        return redirect('allifmaalcommonapp:commonCreditNotes',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonWantToDeleteCreditNote(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonCreditNotesModel.objects.filter(id=pk).first()
        
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        
        }
        return render(request,'allifmaalcommonapp/creditnotes/delete-credit-note-confirm.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDeleteCreditNote(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        
        CommonCreditNotesModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonCreditNotes',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddCreditNoteDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Credit Note Details"
        allif_data=common_shared_data(request)
        
        allifquery=CommonCreditNotesModel.objects.filter(id=pk).first()
        form=CommonAddCreditNoteDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
        if request.method=='POST':
            form=CommonAddCreditNoteDetailsForm(allif_data.get("main_sbscrbr_entity"),request.POST,request.FILES,instance=allifquery)
            if form.is_valid():
                form.save()
                return redirect('allifmaalcommonapp:commonAddCreditNoteDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddCreditNoteDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)

        context={
            "form":form,
            "title":title,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/creditnotes/add-credit-note-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddCreditNoteItems(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Credit Note Items "
        allif_data=common_shared_data(request)
      
        allifquery=CommonCreditNotesModel.objects.filter(id=pk).first()
        form=CommonAddCreditNoteItemForm(allif_data.get("main_sbscrbr_entity"))
        allifqueryset=CommonCreditNoteItemsModel.objects.filter(credit_note=allifquery)#this line helps to
       
        add_item= None
        if request.method=='POST':
            form=CommonAddCreditNoteItemForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.credit_note=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddCreditNoteItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            pass

        context={
    
                "form":form,
            
                "allifqueryset":allifqueryset,
                "title":title,
                "allifquery":allifquery,
               
        }
        return render(request,'allifmaalcommonapp/creditnotes/add_credit_note_items.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonEditCreditNoteItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Credit Note Item Details"
        allif_data=common_shared_data(request)
        
        myquery=CommonCreditNoteItemsModel.objects.filter(id=pk).first()
        allifquery=myquery.credit_note
        allifqueryset=CommonCreditNoteItemsModel.objects.filter(credit_note=allifquery).order_by('-date')

        form=CommonAddCreditNoteItemForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)
        if request.method=='POST':
            form=CommonAddCreditNoteItemForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=myquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.save()
                return redirect('allifmaalcommonapp:commonAddCreditNoteItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            myquery=CommonCreditNoteItemsModel.objects.filter(id=pk).first()
            allifquery=myquery.credit_note
            allifqueryset=CommonCreditNoteItemsModel.objects.filter(credit_note=allifquery).order_by('-date')
            form=CommonAddCreditNoteItemForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)
     
        context={"title":title,"form":form,"allifquery":allifquery,
                 "allifqueryset":allifqueryset,"myquery":myquery,}
        return render(request,'allifmaalcommonapp/creditnotes/add_credit_note_items.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDeleteCreditNoteItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Quote Items"
        allif_data=common_shared_data(request)
       
        myallifquery=CommonCreditNoteItemsModel.objects.filter(id=pk).first()
        myquery=myallifquery.credit_note
        myallifquery.delete()
        return redirect('allifmaalcommonapp:commonAddCreditNoteItems',pk=myquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPostCreditNote(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
       
        allifqueryset=CommonBanksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
       
        allifquery=CommonCreditNotesModel.objects.filter(id=pk).first()#very important to get id to go to particular shipment
        allifqueryset=CommonCreditNoteItemsModel.objects.filter(credit_note=allifquery)
        myinvid=allifquery.id
        customer=allifquery.customer
        amount=allifquery.total_amount
        if customer:
            
            customer_id=customer.id
            for item in allifqueryset:
                
                invo_quantity=item.quantity # this gives the quantities in the invoice
                invoice_item_id=item.items.id #this gives the IDs of the invoice item in the main AllifmaalStocksModel database.
                per_line_cost_price=item.items.unitcost*item.quantity
                per_line_selling_price=item.items.unitPrice*item.quantity
                if item.items.inventory_account !=None:
                    inventory_acc_id=item.items.inventory_account.id
                    expense_acc_id=item.items.expense_account.id
                    income_acc_id=item.items.income_account.id
                    
                    products=CommonStocksModel.objects.filter(pk=invoice_item_id,company=allif_data.get("main_sbscrbr_entity")).first()
                    initial_item_quantity=products.quantity
                    products.quantity=initial_item_quantity-invo_quantity # reduce stock by invoice quantity
                    products.save()
                   
                    # ....... debit the inventory account ..........
                    inv_acc=CommonChartofAccountsModel.objects.filter(pk=inventory_acc_id,company=allif_data.get("main_sbscrbr_entity")).first()
                    initial_inv_bal=inv_acc.balance
                    inv_acc.balance=initial_inv_bal-per_line_cost_price
                    inv_acc.save()

                   
                    # ....... record the revenue in the income account ..........
                    income_acc=CommonChartofAccountsModel.objects.filter(pk=income_acc_id,company=allif_data.get("main_sbscrbr_entity")).first()
                    initial_income_bal=income_acc.balance
                    income_acc.balance=initial_income_bal + per_line_selling_price
                    income_acc.save()

                  
                else:
                    messages.warning(request,"Please ensure credit note details are filled and that all items have been linked to the Chart of Accounts")
                    return redirect('allifmaalcommonapp:commonAddCreditNoteDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

                
                #increase customer turnover
                mycustomer=CommonCustomersModel.objects.filter(pk=customer_id,company=allif_data.get("main_sbscrbr_entity")).first()
                initial_customer_acc_turnover=mycustomer.turnover or 0
               
                mycustomer.turnover=initial_customer_acc_turnover+item.items.unitPrice
                initial_customer_acc_balance=mycustomer.balance or 0
                mycustomer.balance=initial_customer_acc_balance+item.items.unitPrice

                mycustomer.save()
             
                #transaction=AllifmaalCustomerStatementModel.objects.create(customer=customer,debit=inv_total,
                        #comments="Invoice",balance=initial_customer_acc_balance+inv_total)#get the ord
            

               
                ######## change invoice status
                allifquery.posting_inv_status="posted"
                allifquery.save()

                   
        else:
            messages.warning(request,"Please select a customer")
            return redirect('allifmaalcommonapp:commonAddCreditNoteDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

        CommonLedgerEntriesModel.objects.create(customer=customer,credit=amount,
        comments="invoice",company=allif_data.get("main_sbscrbr_entity"),owner=request.user,ledgowner="customer")
        return redirect('allifmaalcommonapp:commonAddCreditNoteDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonPostedCreditNotes(request,*allifargs,**allifkwargs):
    try:
        title="Posted Credit Notes"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
       
        no_invoices=CommonCreditNotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).count()
      
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonCreditNotesModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonCreditNotesModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonCreditNotesModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonCreditNotesModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]

        context={
        #"last_invoices":last_invoices,
        "title":title,
        "no_invoices":no_invoices,
        #"posted_invoices_total_value":posted_invoices_total_value,
        #"latest_paid_invoices":latest_paid_invoices,
        "allifqueryset":allifqueryset,
        "formats":formats,
        "datasorts":datasorts,
            
        }

       
        context={
          
            "title":title,
          
            "allifqueryset":allifqueryset,
            "datasorts":datasorts,
            "formats":formats,

        }
        return render(request,'allifmaalcommonapp/creditnotes/posted-credit-notes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_can_approve
def commonApproveCreditNote(request,pk,*allifargs,**allifkwargs):
    try:
        title="Approve Credit Note"
        allif_data=common_shared_data(request)
        allifquery=CommonCreditNotesModel.objects.filter(id=pk,company=allif_data.get("main_sbscrbr_entity")).first()
        allifquery.approval_status='approved'
        allifquery.save()
        return redirect('allifmaalcommonapp:commonAddCreditNoteDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCreditNotePdf(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
    
        date_today=date.today()
       
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        allifquery=CommonCreditNotesModel.objects.filter(id=pk).first()
        allifqueryset=CommonCreditNoteItemsModel.objects.filter(credit_note=allifquery)
        title="Credit Note "+str(allifquery)
        template_path = 'allifmaalcommonapp/creditnotes/credit-note-pdf.html'
        context = {
        "allifqueryset":allifqueryset,
        "allifquery":allifquery,
        "title":title,
        "scopes":scopes,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        "usr_var":allif_data.get("usernmeslg"),
        "date_today":date_today,
            }
        
        response = HttpResponse(content_type='application/pdf')
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = f'filename="{allifquery} credit_note.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCreditNotesSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
      
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonCreditNotesModel.objects.filter((Q(number__icontains=allifsearch)|Q(total_amount__icontains=allifsearch)|Q(customer__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]

        context={
        "title":title,
        "allifsearch":allifsearch,
        "searched_data":searched_data,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        }
        return render(request,'allifmaalcommonapp/creditnotes/credit-notes.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCreditNotesAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Credit Note Advanced Search"
        allif_data=common_shared_data(request)
       
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonCreditNotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
        lastDate=CommonCreditNotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
        largestAmount=CommonCreditNotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-total_amount').first().total_amount
        scopes=CommonCreditNotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonCreditNotesModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(total_amount__gte=start_value or 0) & Q(total_amount__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/creditnotes/credit_notes_search_pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                   "datasorts":datasorts,
                   "formats":formats,
                   "scopes":scopes,
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="Invoices-advanced-searched-result.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
              
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/creditnotes/credit-notes.html',context)
            else:
                allifqueryset=CommonCreditNotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
         
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/creditnotes/credit-notes.html',context)
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/creditnotes/credit-notes.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
################# general ledger entris #############
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonLedgerEntries(request,*allifargs,**allifkwargs):
    try:
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        title="Ledger Entries"
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonLedgerEntriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonLedgerEntriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonLedgerEntriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonLedgerEntriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]

        context ={ 
         'allifqueryset':allifqueryset,
          "title":title,
           "formats":formats,"datasorts":datasorts, }
        
         
        return render(request,'allifmaalcommonapp/ledgerentries/ledgerentries.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonLedgerEntryDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Ledger Entry Details "
        allifquery=CommonLedgerEntriesModel.objects.filter(id=pk).first()
        context={
            "title":title,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/ledgerentries/ledger-entry-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteLedgerEntry(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonLedgerEntriesModel.objects.filter(id=pk).first()
        myallifquery=CommonLedgerEntriesModel.objects.filter(id=pk).first()
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        "myallifquery":myallifquery,
        }
        return render(request,'allifmaalcommonapp/ledgerentries/ledger-entry-details.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
@logged_in_user_has_departmental_delete
def commonDeleteLedgerEntry(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonLedgerEntriesModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonLedgerEntries',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonLedgerEntrySearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
       
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonLedgerEntriesModel.objects.filter((Q(debit__icontains=allifsearch)
            |Q(debit__icontains=allifsearch)|Q(credit__icontains=allifsearch)|Q(balance__icontains=allifsearch)|Q(customer__name__icontains=allifsearch)|Q(supplier__name__icontains=allifsearch)|Q(staff__staffNo__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]

        context={
        "title":title,
        "allifsearch":allifsearch,
        "searched_data":searched_data,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        }
        return render(request,'allifmaalcommonapp/ledgerentries/ledgerentries.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonLedgerEntryAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Ledger Entries Advanced Search Results"
        allif_data=common_shared_data(request)
       
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]

        current_date=timezone.now().date().today()
        firstDate=current_date
        lastDate=current_date
        largestAmount=0
        searched_data=[]
        firstDepo=CommonLedgerEntriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first()
    
        lastDepo=CommonLedgerEntriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if firstDepo and lastDepo:
            firstDate=CommonLedgerEntriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
            lastDate=CommonLedgerEntriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
            largestAmount=CommonLedgerEntriesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-balance').first().balance
        else:
            firstDate=current_date
            lastDate=current_date


        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonLedgerEntriesModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(balance__gte=start_value or 0) & Q(balance__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/ledgerentries/ledger-entries-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                   "datasorts":datasorts,
                   "formats":formats,
                   "scopes":scopes,
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="ledger-entries-advanced-searched-results.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                # if excel is selected
               
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/ledgerentries/ledgerentries.html',context)
                 
            else:
                searched_data=[]
              
                context={
                "searched_data":searched_data,
                }
                return render(request,'allifmaalcommonapp/ledgerentries/ledgerentries.html',context)
           
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/ledgerentries/ledgerentries.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)            

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonSupplierLedgerEntries(request,pk,*allifargs,**allifkwargs):
    try: 
        title="Supplier Ledger Entries Details"
        allif_data=common_shared_data(request)
       
        allifquery=CommonSuppliersModel.objects.filter(id=pk).first()
        allifqueryset= CommonLedgerEntriesModel.objects.filter(supplier=allifquery,company=allif_data.get("main_sbscrbr_entity")).order_by('date') 
        
        context = { 'allifquery':allifquery, 'allifqueryset':allifqueryset, 'title':title, }
        return render(request,'allifmaalcommonapp/ledgerentries/suppliers/supplier-ledger-entries.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCustomerLedgerEntries(request,pk,*allifargs,**allifkwargs):
    try: 
        title="Customer Ledger Entries Details"
        allif_data=common_shared_data(request)
    
        allifquery=CommonCustomersModel.objects.filter(id=pk).first()
        allifqueryset= CommonLedgerEntriesModel.objects.filter(customer=allifquery,company=allif_data.get("main_sbscrbr_entity")).order_by('date') 
        
        context = { 'allifquery':allifquery, 'allifqueryset':allifqueryset, 'title':title, }
        return render(request,'allifmaalcommonapp/ledgerentries/customers/customer-ledger-entries.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonStaffLedgerEntries(request,pk,*allifargs,**allifkwargs):
    try: 
        title="Staff Ledger Entries Details"
        allif_data=common_shared_data(request)
        allifquery=CommonEmployeesModel.objects.filter(id=pk).first()
        allifqueryset= CommonLedgerEntriesModel.objects.filter(supplier=allifquery,company=allif_data.get("main_sbscrbr_entity")).order_by('date') 
        
        context = { 'allifquery':allifquery, 'allifqueryset':allifqueryset, 'title':title, }
        return render(request,'allifmaalcommonapp/ledgerentries/staff/staff-ledger-entries.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
######### supplier payments section ############
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonSupplierPayments(request,*allifargs,**allifkwargs):
    title="Supplier Payments"
    try:
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifquerysetlatest=CommonSupplierPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:7]
       
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonSupplierPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonSupplierPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonSupplierPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonSupplierPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]
        context={
        "title":title,
        "allifqueryset":allifqueryset,
        "allifquerysetlatest":allifquerysetlatest,
        "allifqueryset":allifqueryset,
        "formats":formats,
        "datasorts":datasorts,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payments.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonPaySupplier(request,pk,*allifargs,**allifkwargs):
    try:
        title="Pay Supplier"
        allif_data=common_shared_data(request)
        allifquery=CommonSuppliersModel.objects.filter(id=pk).first()
        form=CommonAddSupplierPaymentForm(allif_data.get("main_sbscrbr_entity"),allif_data.get("logged_user_department"))
        if request.method=='POST':
            form=CommonAddSupplierPaymentForm(allif_data.get("main_sbscrbr_entity"),allif_data.get("logged_user_department"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.supplier=allifquery
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSupplierPayments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSupplierPaymentForm(allif_data.get("main_sbscrbr_entity"),allif_data.get("logged_user_department"))
        context={
            "form":form,  
            "title":title,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/pay-supplier.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonSupplierPaymentSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonSupplierPaymentsModel.objects.filter((Q(amount__icontains=allifsearch)
            |Q(description__icontains=allifsearch)|Q(supplier__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]
        context={
        "title":title,
        "searched_data":searched_data,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),}
        return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payments.html',context)
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonSupplierPaymentAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Supplier Payment Advanced Search Results"
        allif_data=common_shared_data(request)
       
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
    
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]

        current_date=timezone.now().date().today()
        firstDate=current_date
        lastDate=current_date
        largestAmount=0
        searched_data=[]
        firstDepo=CommonSupplierPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first()
    
        lastDepo=CommonSupplierPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if firstDepo and lastDepo:
            firstDate=CommonSupplierPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
            lastDate=CommonSupplierPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
            largestAmount=CommonSupplierPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-amount').first().amount
        else:
            firstDate=current_date
            lastDate=current_date
        
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonSupplierPaymentsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":

                    template_path = 'allifmaalcommonapp/payments/suppliers/supplier-payment-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                   "datasorts":datasorts,
                   "formats":formats,
                   "scopes":scopes,
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="supplier-payment-advanced-searched-results.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
             
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payments.html',context)
            else:
                searched_data=[]
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            "searched_data":searched_data,
            }
            return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payments.html',context)
           
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payments.html',context)
           
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)            

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteSupplierPayment(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonSupplierPaymentsModel.objects.filter(id=pk).first()
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/x-supplier-payment-confrm.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
@logged_in_user_has_departmental_delete
def commonDeleteSupplierPayment(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonSupplierPaymentsModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonSupplierPayments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_has_departmental_access
def commonSupplierPaymentDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Supplier Payment Details "
        allif_data=common_shared_data(request)
        allifquery=CommonSupplierPaymentsModel.objects.filter(id=pk).first()
        form =CommonAddSupplierPaymentForm(allif_data.get("main_sbscrbr_entity"),allif_data.get("logged_user_department"),instance=allifquery)
        if request.method=='POST':
            form=CommonAddSupplierPaymentForm(allif_data.get("main_sbscrbr_entity"),allif_data.get("logged_user_department"),request.POST, instance=allifquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSupplierPaymentDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form =CommonAddSupplierPaymentForm(allif_data.get("main_sbscrbr_entity"),allif_data.get("logged_user_department"),instance=allifquery)

        context={
            
            "title":title,
            "allifquery":allifquery,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payment-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonEditSupplierPayment(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Supplier Payment"
        allif_data=common_shared_data(request)
        allifquery_update=CommonSupplierPaymentsModel.objects.filter(id=pk).first()
        form=CommonAddSupplierPaymentForm(allif_data.get("main_sbscrbr_entity"),allif_data.get("logged_user_department"),instance=allifquery_update)
        if request.method=='POST':
            form = CommonAddSupplierPaymentForm(allif_data.get("main_sbscrbr_entity"),allif_data.get("logged_user_department"),request.POST, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSupplierPayments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSupplierPaymentForm(allif_data.get("main_sbscrbr_entity"),allif_data.get("logged_user_department"),instance=allifquery_update)

        context = {
            'form':form,
            "allifquery_update":allifquery_update,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/pay-supplier.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonPostSupplierPayment(request,pk,*allifargs,**allifkwargs):#global
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonSupplierPaymentsModel.objects.filter(id=pk).first()
        allifsup=allifquery.supplier.id
        amount=allifquery.amount#this gives the amount of salary given to the staff
        pay_from_acc_id=allifquery.account.id
        mysupp=CommonSuppliersModel.objects.filter(id=allifsup).first()
        init_balance=mysupp.balance
        mysupp.balance=init_balance + amount
        mysupp.save()

        # reduce the balance of the cash account or account salary paid from
        payfromccount=CommonChartofAccountsModel.objects.filter(pk=pay_from_acc_id).first()
        acc_balance=payfromccount.balance
        payfromccount.balance=acc_balance-amount
        payfromccount.save()
        mysign=-1

        # update the supplier statement as well.
        transaction=CommonSupplierStatementsModel.objects.create(supplier=mysupp,credit=amount*mysign,
        comments="Payment",balance= Decimal(init_balance)+Decimal(amount))#get the ord
        
        CommonLedgerEntriesModel.objects.create(supplier=mysupp,credit=amount*mysign,
        comments="Payment",balance= Decimal(init_balance)+Decimal(amount),company=allif_data.get("main_sbscrbr_entity"),owner=request.user,ledgowner="supplier")#get the ord
        legs=CommonLedgerEntriesModel.objects.all()

        allifquery.status="posted"
        allifquery.save()
        return redirect('allifmaalcommonapp:commonSupplierPayments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonPostedSupplierPayments(request,*allifargs,**allifkwargs):
    try:
        title="Posted Supplier Payments"
        allif_data=common_shared_data(request)
        allifqueryset=CommonSupplierPaymentsModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity"))
        context={
            "allifqueryset":allifqueryset,
            "title":title,
            
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/posted-payments.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonPaySupplierDirect(request,*allifargs,**allifkwargs):
    title="Direct Pay Supplier"
    try:
        allif_data=common_shared_data(request)
        form=CommonAddSupplierPaymentForm(allif_data.get("main_sbscrbr_entity"),allif_data.get("logged_user_department"))
    
        if request.method=='POST':
            form=CommonAddSupplierPaymentForm(allif_data.get("main_sbscrbr_entity"),allif_data.get("logged_user_department"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSupplierPayments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSupplierPaymentForm(allif_data.get("main_sbscrbr_entity"),allif_data.get("logged_user_department"))
    
        context={
            "form":form,  
            "title":title,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/pay-supplier-directly.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#
################ SUPPLIER STATEMENTS####################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonSupplierStatementpdf(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]

        allifquery=CommonSuppliersModel.objects.filter(id=pk).first()
        allifqueryset=CommonLedgerEntriesModel.objects.filter(supplier=allifquery,company=allif_data.get("main_sbscrbr_entity")).order_by('date') 
        total=sum(transaction.balance for transaction in allifqueryset) 
        mydate=timezone.now().date().today()
        system_user=request.user
        title="Supplier Statement "+" "+str(allifquery)
        template_path = 'allifmaalcommonapp/statements/suppliers/supplier_statement_pdf.html'
      
        context = {
        'allifquery':allifquery,
        "system_user":system_user,
        "title":title,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        
        "mydate":mydate,
        "scopes":scopes,
      
        }

        response = HttpResponse(content_type='application/pdf') # this opens on the same page
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = 'filename="Supplier-Statement.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        
      
        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
    ##################################33 our customers ###################################3
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


######################### customer payments #################3
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonCustomerPayments(request,*allifargs,**allifkwargs):
    title="Customer Payments"
    try:

        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonCustomerPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonCustomerPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonCustomerPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonCustomerPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]
        context={
            
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
            
        }
        return render(request,'allifmaalcommonapp/payments/customers/customer-payments.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTopUpCustomerAccount(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
       
        default_cash_accs=CommonChartofAccountsModel.objects.filter(description="Cash").first()
        form=CommonAddCustomerPaymentForm(allif_data.get("main_sbscrbr_entity"),initial={'account':default_cash_accs})
        customer=CommonCustomersModel.objects.get(id=pk)
        mycustid=customer.id
        title="Receive Payment From "+ str(customer)
    
        top_up_cust_account= get_object_or_404(CommonCustomersModel, id=pk)
        topups=CommonCustomerPaymentsModel.objects.filter(customer=customer)#this line helps to
      
        add_item= None
        if request.method=='POST':
            form=CommonAddCustomerPaymentForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.customer=top_up_cust_account
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                form=CommonAddCustomerPaymentForm(allif_data.get("main_sbscrbr_entity"))
                return redirect('allifmaalcommonapp:commonCustomerPayments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            pass

        context={
            "form":form,  
            "customer":customer,
            "topups":topups,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/payments/customers/add-customer-payment.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_has_departmental_access
def commonEditCustomerPayment(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Customer Payment"
        allif_data=common_shared_data(request)
        allifquery_update=CommonCustomerPaymentsModel.objects.get(id=pk)
        form=CommonAddCustomerPaymentForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)

        if request.method=='POST':
            form =CommonAddCustomerPaymentForm(allif_data.get("main_sbscrbr_entity"),request.POST, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonCustomerPayments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddCustomerPaymentForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
    
        context = {
            "form":form,
            "allifquery_update":allifquery_update,
           
            "title":title,
        }
        
        return render(request,'allifmaalcommonapp/payments/customers/add-customer-payment.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteCustomerPayment(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonCustomerPaymentsModel.objects.filter(id=pk).first()
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/payments/customers/x-cust-payment-confrm.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_has_departmental_delete
def commonDeleteCustomerPayment(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonCustomerPaymentsModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonCustomerPayments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCustomerPaymentDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Payment Details "
        allif_data=common_shared_data(request)
       
        allifquery=CommonCustomerPaymentsModel.objects.filter(id=pk).first()
        form=CommonAddCustomerPaymentForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
        if request.method=='POST':
            form =CommonAddCustomerPaymentForm(allif_data.get("main_sbscrbr_entity"),request.POST, instance=allifquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonCustomerPaymentDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            pass
        context={
            
            "title":title,
            "allifquery":allifquery,
            "form":form,
            
        }
        return render(request,'allifmaalcommonapp/payments/customers/customer-payment-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonReceiveCustomerMoney(request,*allifargs,**allifkwargs):
    try:
        title="Receive Customer Money"
        allif_data=common_shared_data(request)
        form=CommonAddCustomerPaymentForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddCustomerPaymentForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj= form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonCustomerPayments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            pass
        context={
            "form":form,  
            "title":title,
        }
        return render(request,'allifmaalcommonapp/payments/customers/receive-customer-money.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonPostCustomerPayment(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        
        payment=CommonCustomerPaymentsModel.objects.get(id=pk)#very important to get id to go to particular shipment
        myamount=payment.amount#this gives the initial account
        customer=payment.customer
        debit_acc=payment.account
        if (customer and myamount)!=None:
            mycust=CommonCustomersModel.objects.get(id=customer.id)
            initial_cust_acc_bal=mycust.balance
            mycust.balance= Decimal(initial_cust_acc_bal)-Decimal(myamount)
            mycust.status=='posted'
            mycust.save()

            # debit the asset account where the money from customer is received to
            coa_acc=CommonChartofAccountsModel.objects.get(id=debit_acc.id)
            initial_coa_acc_bal=coa_acc.balance
            coa_acc.balance= Decimal(initial_coa_acc_bal)+Decimal(myamount)
            coa_acc.save()
            CommonLedgerEntriesModel.objects.create(customer=customer,credit=myamount,
            comments="payment",company=allif_data.get("main_sbscrbr_entity"),owner=request.user,ledgowner="customer")
            return redirect('allifmaalcommonapp:commonCustomerPayments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

        else:
            return render(request,'allifmaalcommonapp/error/error.html')
           
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonPostedCustomerPayments(request,*allifargs,**allifkwargs):
    try:
        title="Posted Customer Payments"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
      
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonCustomerPaymentsModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonCustomerPaymentsModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonCustomerPaymentsModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonCustomerPaymentsModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]
        context={
            "allifqueryset":allifqueryset,
            "title":title,
            "formats":formats,
            "datasorts":datasorts,
         
        }
        return render(request,'allifmaalcommonapp/payments/customers/customer-posted-payments.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonCustomerStatementpdf(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        mydate=timezone.now().date().today()
        AllifQueryDetails=get_object_or_404(CommonCustomersModel,id=pk)
        title="Customer Statement "+" "+str(AllifQueryDetails)
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]

        AllifObject=CommonCustomersModel.objects.get(id=pk)
        PO_suplier=AllifObject.name
        AllifQueryItems= CommonCustomerStatementsModel.objects.filter(customer=AllifObject)
        template_path = 'allifmaalcommonapp/statements/customers/customer_statement_pdf.html'
     
        context = {
        'AllifQueryDetails':AllifQueryDetails,
        "AllifQueryItems":AllifQueryItems,
        #"companyDetails":companyDetails,
        "scopes":scopes, 
        "system_user":allif_data.get("usernmeslg"),
        "title":title,
        
        "PO_suplier":PO_suplier,
        "AllifObject":AllifObject,
        "mydate":mydate,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
    
        }
        
       
        response = HttpResponse(content_type='application/pdf') # this opens on the same page
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = 'filename="Customer-Statement.pdf"'
        template=get_template(template_path)
        html=template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
    ##################################33 our customers ###################################3
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonCustomerPaymentSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
       
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonCustomerPaymentsModel.objects.filter((Q(amount__icontains=allifsearch)
            |Q(description__icontains=allifsearch)|Q(customer__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]

        context={
        "title":title,
       
        "searched_data":searched_data,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
    }
        return render(request,'allifmaalcommonapp/payments/customers/customer-payments.html',context)
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonCustomerPaymentAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Customer Payment Advanced Search Results"
        allif_data=common_shared_data(request)
       
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]

        current_date=timezone.now().date().today()
        firstDate=current_date
        lastDate=current_date
        largestAmount=0
        searched_data=[]
        firstDepo=CommonCustomerPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first()
    
        lastDepo=CommonCustomerPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if firstDepo and lastDepo:
            firstDate=CommonCustomerPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
            lastDate=CommonCustomerPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
            largestAmount=CommonCustomerPaymentsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-amount').first().amount
        else:
            firstDate=current_date
            lastDate=current_date
        
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonCustomerPaymentsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":

                    template_path = 'allifmaalcommonapp/payments/customers/customer-payment-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                   "datasorts":datasorts,
                   "formats":formats,
                   "scopes":scopes,
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="customer-payment-advanced-searched-results.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                # if excel is selected
              
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/payments/customers/customer-payments.html',context)
            else:
                searched_data=[]
             
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payments.html',context)
           
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payments.html',context)
           
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

########################3 staff salaries #############
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_universal_access
def commonSalaries(request,*allifargs,**allifkwargs):
    try:
        title="Staff Salaries"
        allif_data=common_shared_data(request)
      
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
        allifqueryset=CommonSalariesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))

        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonSalariesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonSalariesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonSalariesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonSalariesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
        }

        return render(request,'allifmaalcommonapp/hrm/salaries/salaries.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_branches_access
def commonAddSalary(request,*allifargs,**allifkwargs):
    try:
        title="Initiate Salary Payment"
        allif_data=common_shared_data(request)
        form =CommonAddSalaryForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form =CommonAddSalaryForm(allif_data.get("main_sbscrbr_entity"),request.POST,request.FILES)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSalaries',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                form.non_field_errors
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSalaryForm(allif_data.get("main_sbscrbr_entity"))
       
        context = {
            "title":title,
            "form":form,}

        return render(request,'allifmaalcommonapp/hrm/salaries/add-salary.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_divisional_access
def commonSalarySearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonSalariesModel.objects.filter((Q(amount__icontains=allifsearch)
            |Q(description__icontains=allifsearch)|Q(staff__firstName__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]

        context={
        "title":title,
        "searched_data":searched_data,
        }
        return render(request,'allifmaalcommonapp/hrm/salaries/salaries.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_divisional_access
def commonSalaryAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        allif_data=common_shared_data(request)
       
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]

        current_date=timezone.now().date().today()
        firstDate=current_date
        lastDate=current_date
        largestAmount=0
        searched_data=[]
        firstDepo=CommonSalariesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first()
    
        lastDepo=CommonSalariesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if firstDepo and lastDepo:
            firstDate=CommonSalariesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
            lastDate=CommonSalariesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
            largestAmount=CommonSalariesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-amount').first().amount
        else:
            firstDate=current_date
            lastDate=current_date

        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonSalariesModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":

                    template_path = 'allifmaalcommonapp/hrm/salaries/salaries_search_pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                   "datasorts":datasorts,
                   "formats":formats,
                   "scopes":scopes,
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="searched-result.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                # if excel is selected
               
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/hrm/salaries/salaries.html',context)
                   
            else:
                searched_data=[]
             
                context={
                "allifqueryset":allifqueryset,
                "formats":formats,
                "title":title,
                "datashorts":datasorts,
                "formats":formats,
                }
                return render(request,'allifmaalcommonapp/hrm/salaries/salaries.html',context)
           
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/hrm/salaries/salaries.html',context)
          
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_divisional_access
def commonSalaryDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Salary Details"
        allifquery=CommonSalariesModel.objects.filter(id=pk).first()
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/hrm/salaries/salary-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_divisional_access
def commonEditSalaryDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Salary Details"
        allif_data=common_shared_data(request)
        allifquery_update=CommonSalariesModel.objects.get(id=pk)
        form=CommonAddSalaryForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)#insert the content of the table stored in the selected id in the update form
        #we could have used the add customer form but the validation will refuse us to update since fields may exist
        if request.method=='POST':
            form =CommonAddSalaryForm(allif_data.get("main_sbscrbr_entity"),request.POST, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonSalaries',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                form.non_field_errors
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddSalaryForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context = {
            'form':form,
            "allifquery_update":allifquery_update,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/hrm/salaries/add-salary.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_divisional_access
def commonWantToDeleteSalary(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonSalariesModel.objects.filter(id=pk).first()
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
       
        }
        return render(request,'allifmaalcommonapp/hrm/salaries/x-salary-confirm.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_divisional_access
@logged_in_user_has_divisional_delete
def commonDeleteSalary(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonSalariesModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonSalaries',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_divisional_access
def commonPostSalary(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonSalariesModel.objects.get(id=pk)
        emp_no=allifquery.staff.staffNo
        normal_salary=allifquery.amount#this gives the amount of salary given to the staff
        month_salary=allifquery.salary_payable
        pay_from_acc_id=allifquery.account.id
       
        CommonLedgerEntriesModel.objects.create(credit=month_salary,
        comments="payment",company=allif_data.get("main_sbscrbr_entity"),owner=request.user,ledgowner="staff")
    
        # first get the salaries account
        salaries_balance=CommonChartofAccountsModel.objects.filter(description="Salaries")
        equityacc=CommonChartofAccountsModel.objects.filter(description="Equity")
        if salaries_balance and equityacc:

            # increase the salaries expense account
            sal_balances=CommonChartofAccountsModel.objects.get(description="Salaries")
            init_balance=sal_balances.balance
            sal_balances.balance=init_balance +month_salary
            sal_balances.save()

            # reduce the balance of the cash account or account salary paid from
            salaryaccount=CommonChartofAccountsModel.objects.get(pk=pay_from_acc_id)
            acc_balance=salaryaccount.balance
            salaryaccount.balance=acc_balance-month_salary
            salaryaccount.save()

            # reduce the balance of the equity account to balance the accounting equation...
            equityaccount=CommonChartofAccountsModel.objects.get(description="Equity")
            acc_balance=equityaccount.balance
            equityaccount.balance=acc_balance-month_salary
            equityaccount.save()

            # increase the value in the accommulation in the hrm model
            allifstaff=CommonEmployeesModel.objects.get(staffNo=emp_no)
            salary_accommulation=allifstaff.total_salary_paid
            allifstaff.total_salary_paid=salary_accommulation+(month_salary)

            # also the salary balance account is affected depending on whether the amount paid is more than 
            # or less than the normal salary
            init_salary_balance=allifstaff.salary_balance
            allifstaff.salary_balance=(month_salary-normal_salary)+init_salary_balance
            allifstaff.save()

            #
            allifquery.status="posted"
            allifquery.save()
            return redirect('allifmaalcommonapp:commonSalaries',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

        else:

            messgeone=messages.error(request, 'Please note that either Equity or Salaries or both accounts are missing in the chart of accounts.')
            messgetwo=messages.error(request, 'Add Equity and Salaries accounts in the Equity and Expenses categories respectively, if they are not already there, then post again.')
           
            return render(request,'allifmaalcommonapp/error/error.html')
            
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_divisional_access
def commonPostedSalaries(request,*allifargs,**allifkwargs):
    try:
        title="Posted Staff Salaries"
        allif_data=common_shared_data(request)
      
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
       
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonSalariesModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonSalariesModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonSalariesModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonSalariesModel.objects.filter(status="posted",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
        }

        return render(request,'allifmaalcommonapp/hrm/salaries/posted-salaries.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

################################ JOBS ############################
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonJobs(request,*allifargs,**allifkwargs):
    try:
        title="Jobs"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
     
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonJobsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonJobsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonJobsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonJobsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]
        context={
            "allifqueryset":allifqueryset,
            "title":title,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request,'allifmaalcommonapp/jobs/jobs.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonNewJobs(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        current_datetime=timezone.now().date().today()
        job_year=current_datetime.year
        last_job= CommonJobsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('id').last()
        last_obj=CommonJobsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if last_obj:
            last_obj_id=last_obj.id
            last_obj_incremented=last_obj_id+1
            jobNo= 'Job/'+str(uuid4()).split('-')[1]+'/'+str(last_obj_incremented)+'/'+str(job_year)
        else:
            jobNo= 'First/Job/'+str(uuid4()).split('-')[1]
        newJobRef=CommonJobsModel.objects.create(job_number=jobNo,description="Job Description",company=allif_data.get("main_sbscrbr_entity"),owner=allif_data.get("usernmeslg") or None,
                    division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        newJobRef.save()
        return redirect('allifmaalcommonapp:commonJobs',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonJobSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
      
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonJobsModel.objects.filter((Q(job_number__icontains=allifsearch)
            |Q(description__icontains=allifsearch)|Q(customer__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
           
        }
        return render(request,'allifmaalcommonapp/jobs/jobs.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonJobAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        allif_data=common_shared_data(request)
      
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]

        current_date=timezone.now().date().today()
        firstDate=current_date
        lastDate=current_date
        largestAmount=0
        searched_data=[]
        firstDepo=CommonJobsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first()
    
        lastDepo=CommonJobsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if firstDepo and lastDepo:
            firstDate=CommonJobsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
            lastDate=CommonJobsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
            largestAmount=CommonJobsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        else:
            firstDate=current_date
            lastDate=current_date
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonJobsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate)  & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":

                    template_path='allifmaalcommonapp/jobs/job-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                   "datasorts":datasorts,
                   "formats":formats,
                   "scopes":scopes,
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="searched-result.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
               
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/jobs/jobs.html',context)
                    
                   
            else:
                searched_data=[]
                context={
                 "searched_data":searched_data,
                "formats":formats,
                "title":title,
                "datashorts":datasorts,
                "formats":formats,
                }
                return render(request,'allifmaalcommonapp/jobs/jobs.html',context)
            
        else:
            searched_data=[]
            context={
            "searched_data":searched_data,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/jobs/jobs.html',context)
           
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
@logged_in_user_has_departmental_delete
def commonDeleteJob(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonJobsModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonJobs',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
   
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_access
def commonAddJobDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Job Details"
        allif_data=common_shared_data(request)
       
        allifquery=CommonJobsModel.objects.filter(id=pk).first()
        form=CommonAddJobDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
        if request.method =='POST':
            form=CommonAddJobDetailsForm(allif_data.get("main_sbscrbr_entity"),request.POST,instance=allifquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonAddJobDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddJobDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
        context={
            "form":form,
            "title":title,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/jobs/add-job-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
 
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_departmental_delete
def commonAddJobItems(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Job Items"
        allif_data=common_shared_data(request)
       
        allifquery=CommonJobsModel.objects.filter(id=pk).first()
        form=CommonAddJobItemsForm(allif_data.get("main_sbscrbr_entity"))
        allifqueryset= CommonJobItemsModel.objects.filter(jobitemconnector=allifquery)#this line helps to
    
        add_item= None
        if request.method=='POST':
            form=CommonAddJobItemsForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.jobitemconnector=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddJobItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddJobItemsForm(allif_data.get("main_sbscrbr_entity"))

        context={
            
            "form":form,
            "title":title,
            "allifquery":allifquery,
            "allifqueryset":allifqueryset
        }
        return render(request,'allifmaalcommonapp/jobs/add-job-items.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_can_delete
def commonWantToDeleteJob(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonJobsModel.objects.filter(id=pk).first()
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/jobs/delete_job_confirm.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteJobItem(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonJobItemsModel.objects.filter(id=pk).first()
        
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
       
        }
        return render(request,'allifmaalcommonapp/jobs/add-job-items.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDeleteJobItem(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        myallifquery=CommonJobItemsModel.objects.filter(id=pk).first()
        allifquery=myallifquery.jobitemconnector
        myallifquery.delete()
        return redirect('allifmaalcommonapp:commonAddJobItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonInvoiceJob(request,pk,*allifargs,**allifkwargs):
    try:
        title="Invoice Job"
        allif_data=common_shared_data(request)
        form=CommonAddJobItemsForm(allif_data.get("main_sbscrbr_entity"))
     
        allifquery=CommonJobsModel.objects.filter(id=pk).first()
       
        allifqueryset=CommonJobItemsModel.objects.filter(jobitemconnector=allifquery)
    
        context={
        "allifquery":allifquery,
        "allifqueryset":allifqueryset,
        "title":title,
        "form":form,
            
        }
        
        return render(request,'allifmaalcommonapp/jobs/invoice-job.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonJobInvoicePdf(request,pk,*allifargs,**allifkwargs):
    try:
        title="Job Invoice Pdf"
        allif_data=common_shared_data(request)
        system_user=request.user
        my_job_id=CommonJobsModel.objects.get(id=pk)
        job_Items =CommonJobItemsModel.objects.filter(jobitemconnector=my_job_id)
        myuplift=0
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]

    
        template_path = 'allifmaalcommonapp/jobs/job-inv-pdf.html'
    
        context={
            "my_job_id":my_job_id,
            "job_Items":job_Items,
            "myuplift":myuplift,
        
            "system_user":system_user,
            "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
            "title":title,
            "scopes":scopes,

            
        }
        
        
     
        response = HttpResponse(content_type='application/pdf') # this opens on the same page
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = 'filename="searched-result.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonJobTransactionReportpdf(request,pk,*allifargs,**allifkwargs):
    try:
        title="Job Invoice Pdf"
        allif_data=common_shared_data(request)
        system_user=request.user
        my_job_id=CommonJobsModel.objects.get(id=pk)
        job_Items =CommonJobItemsModel.objects.filter(jobitemconnector=my_job_id)
        myuplift=0
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        allif_data=common_shared_data(request)
        system_user=request.user
        my_job_id=CommonJobsModel.objects.get(id=pk)
        job_Items =CommonJobItemsModel.objects.filter(jobitemconnector=my_job_id)
        myuplift=0
    
        template_path = 'allifmaalcommonapp/jobs/job-trans-report-pdf.html'
    
        context={
            "my_job_id":my_job_id,
            "job_Items":job_Items,
            "myuplift":myuplift,
        
            "system_user":system_user,
            "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
            "title":title,
            "scopes":scopes,

            
        }
        
        
     
        response = HttpResponse(content_type='application/pdf') # this opens on the same page
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = 'filename="searched-result.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


################################## TASKS ###########################################
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTasks(request,*allifargs,**allifkwargs):
    try:
        title="To do list"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
    
        form =CommonAddTasksForm(allif_data.get("main_sbscrbr_entity"))
       
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(status="incomplete",company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(status="incomplete",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(status="incomplete",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(status="incomplete",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]
        if request.method=='POST':
            form=CommonAddTasksForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
               
                #form=CommonAddTasksForm(allif_data.get("main_sbscrbr_entity"))#this clears out the form after adding the product
                return redirect('allifmaalcommonapp:commonTasks',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
               
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form =CommonAddTasksForm(allif_data.get("main_sbscrbr_entity"))
           
        context = {
            "form":form,
            "allifqueryset":allifqueryset,
            "title":title,
           
            "datasorts":datasorts,
            
        }

        return render(request,'allifmaalcommonapp/tasks/tasks.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTaskBasicSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
       
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonTasksModel.objects.filter((Q(task__icontains=allifsearch)
            |Q(status__icontains=allifsearch)|Q(assignedto__firstName__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        }
        return render(request,'allifmaalcommonapp/tasks/tasks.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTasksSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
      
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonTasksModel.objects.filter((Q(task__icontains=allifsearch)
            |Q(status__icontains=allifsearch)|Q(assignedto__firstName__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        }
        return render(request,'allifmaalcommonapp/tasks/tasks.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddSeeTaskDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add And See Task Details"
        allif_data=common_shared_data(request)
      
        allifquery=CommonTasksModel.objects.filter(id=pk).first()
        form=CommonAddTasksForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
        if request.method =='POST':
            form=CommonAddTasksForm(allif_data.get("main_sbscrbr_entity"),request.POST,instance=allifquery)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.company=allif_data.get("main_sbscrbr_entity")
                add_item.owner=allif_data.get("usernmeslg")
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddSeeTaskDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

                
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
                
        context={
            "form":form,
            "title":title,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/tasks/add-task-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonMarkTaskComplete(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
      
        mark_complete=CommonTasksModel.objects.filter(id=pk).first()
        if mark_complete.status=="incomplete":
            mark_complete.status="complete"
            mark_complete.save()
        
        else:
            mark_complete.status="incomplete"
            mark_complete.save()
        return redirect('allifmaalcommonapp:commonTasks',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view 
def commonCompletedTasks(request,*allifargs,**allifkwargs):
    try:
        title="Completed Tasks"
        allif_data=common_shared_data(request)
    
        allifqueryset=CommonTasksModel.objects.filter(status="complete",company=allif_data.get("main_sbscrbr_entity"))
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(status="complete",company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(status="complete",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(status="complete",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(status="complete",company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]
        
        context = {
           
            "title":title,
            "allifqueryset":allifqueryset,
        }

        return render(request,'allifmaalcommonapp/tasks/finished-tasks.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDeleteTask(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
       
        CommonTasksModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonTasks',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonEditTask(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Task"
        allif_data=common_shared_data(request)
        
      
        allifquery=CommonTasksModel.objects.filter(id=pk).first()
        allifqueryset=CommonTasksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
      
        form =CommonAddTasksForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
        if request.method == 'POST':
            form = CommonAddTasksForm(allif_data.get("main_sbscrbr_entity"),request.POST, instance=allifquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
               
                return redirect('allifmaalcommonapp:commonTasks',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                form.non_field_errors
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        context = {
            'form':form,
            "allifquery":allifquery,
            "allifqueryset":allifqueryset,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/tasks/tasks.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)




###################### profit and loss section ###################3
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_has_universal_access
def commonProfitAndLoss(request,*allifargs,**allifkwargs):
    try:
        title="Profit And Loss"
        allif_data=common_shared_data(request)
     
        latest=CommonInvoicesModel.objects.order_by('-date').filter(posting_inv_status='posted')[:7]
        totalsales=CommonInvoicesModel.objects.filter(posting_inv_status='posted').order_by('-invoice_total').aggregate(Sum('invoice_total'))['invoice_total__sum']
        totalrevenue=CommonChartofAccountsModel.objects.filter(code__lt=49999,code__gt=39999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        totalgoodscost=CommonInvoicesModel.objects.filter(posting_inv_status='posted').order_by('-invoice_items_total_cost').aggregate(Sum('invoice_items_total_cost'))['invoice_items_total_cost__sum']
        grossprofitorloss=(totalsales or 0)-(totalgoodscost or 0)
        #totalexpenses=totalgoodscost=AllifmaalExpensesModel.objects.all().order_by('-amount').aggregate(Sum('amount'))['amount__sum']
        totexpenses=CommonChartofAccountsModel.objects.filter(code__lt=59999,code__gt=49999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        netprofitorloss=grossprofitorloss-(totexpenses or 0)
        totalrevenue=CommonChartofAccountsModel.objects.filter(code__lt=49999,code__gt=39999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        #order_by('-amount').aggregate(Sum('amount'))['amount__sum']
        exps=CommonChartofAccountsModel.objects.filter(code__lt=59999,code__gt=49999)

        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]
        context={
            "title":title,
            "totalsales":totalsales,
            "totalgoodscost":totalgoodscost,
            "grossprofitorloss":grossprofitorloss,
            "netprofitorloss":netprofitorloss,
            "totexpenses":totexpenses,
            "totalrevenue":totalrevenue,
            "latest":latest,
        }
        
        return render(request,'allifmaalcommonapp/statements/financial/p&l-statement.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
        
######################################### REPORTS SECTION ############33
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonMainReports(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]

        title="Main Reports"
        context={
        "title":title,
        }
        return render(request,'allifmaalcommonapp/reports/reports.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDebtorsReport(request,*allifargs,**allifkwargs):
    try:
        
        allif_data=common_shared_data(request)
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonCustomersModel.objects.filter(balance__gte=1,company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(balance__gte=1,company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(balance__gte=1,company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonTasksModel.objects.filter(balance__gte=1,company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]
        mydate=date.today()
        title="Debtors List"
        template_path = 'allifmaalcommonapp/reports/debtors-report.html'#this is the template to be converted to pdf
        
        context = {
       "allifqueryset":allifqueryset,
        "mydate":mydate,
        "title":title,
        "scopes":scopes,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity")
        }
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = 'filename="debtors-list.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
            
        return response
        #return render(request,'example.html',context)#this can be used also
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonCreditorsReportpdf(request,*allifargs,**allifkwargs):
    try:
        title="Creditors List"
        allif_data=common_shared_data(request)
        template_path = 'allifmaalcommonapp/reports/creditors-report.html'
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]

        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonSuppliersModel.objects.filter(balance__gte=1,company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonSuppliersModel.objects.filter(balance__gte=1,company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonSuppliersModel.objects.filter(balance__gte=1,company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonSuppliersModel.objects.filter(balance__gte=1,company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]
       
        context = {
            "allifqueryset":allifqueryset,

        "scopes":scopes,
        "title":title,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
    
        }
        
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = 'filename="creditors-list.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAvailableStockpdf(request,*allifargs,**allifkwargs):
    try:
        title="Available Stock List"
        allif_data=common_shared_data(request)
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        allifqueryset=[]

        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonStocksModel.objects.filter(quantity__gte=1,company=allif_data.get("main_sbscrbr_entity")).order_by('date')
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonStocksModel.objects.filter(quantity__gte=1,company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division")).order_by('date')
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonStocksModel.objects.filter(quantity__gte=1,company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch")).order_by('date')
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonStocksModel.objects.filter(quantity__gte=1,company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department")).order_by('date')
        else:
            allifqueryset=[]
            
        template_path = 'allifmaalcommonapp/reports/available-stock-report.html'
        context = {
        "title":title,
        "scopes":scopes,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        "allifqueryset":allifqueryset,
        }
        
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = 'filename="available-stock-report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#####################################3 shipments ##########################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTransits(request,*allifargs,**allifkwargs):
    try:
        title="Transportations"
        allif_data=common_shared_data(request)
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
       
        no_of_quotes=CommonTransitModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).count()
      
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonTransitModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonTransitModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonTransitModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonTransitModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "no_of_quotes":no_of_quotes,
            "prospects":prospects,
          
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request, 'allifmaalcommonapp/transport/transits.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonNewTransit(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
       
        ###### start... UID generation ##################
        allifquery=CommonTransitModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        currntyear=timezone.now().date().today().year
        allifuid=str(nmbr)+"/"+str(unque)
        ###### End... UID generation ##################

        if allifquery:
            sqnmbr='SHP'+"/"+str(allifuid)
        else:
            sqnmbr= 'SHP/1'+"/"+str(uuid4()).split('-')[2]

        newQuoteNumber=CommonTransitModel.objects.create(shipment_number=sqnmbr,company=allif_data.get("main_sbscrbr_entity"),owner=allif_data.get("usernmeslg"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        newQuoteNumber.save()
        return redirect('allifmaalcommonapp:commonTransits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonWantToDeleteTransit(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonTransitModel.objects.filter(id=pk).first()
        title="Are u sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/transport/delete-transit-confirm.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonDeleteTransit(request,pk,*allifargs,**allifkwargs):
    try: 
        allif_data=common_shared_data(request)
        CommonTransitModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonTransits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddTransitDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Shipment Details"
        allif_data=common_shared_data(request)
       
        allifquery=CommonTransitModel.objects.filter(id=pk).first()
        allifqueryset=CommonTransitItemsModel.objects.filter(shipment=allifquery)
        form=CommonAddTransitDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
        if request.method == 'POST':
            form=CommonAddTransitDetailsForm(allif_data.get("main_sbscrbr_entity"),request.POST,request.FILES,instance=allifquery)
            if form.is_valid():
                form.save()
                return redirect('allifmaalcommonapp:commonAddTransitDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddTransitDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)

        context={
            "form":form,
            "allifquery":allifquery,
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/transport/add_transit_details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddShipmentItems(request,pk,*allifargs,**allifkwargs):
    try:
        
        title="Add Shipment Items"
        allif_data=common_shared_data(request)
       
        allifquery=CommonTransitModel.objects.filter(id=pk).first()

        form=CommonAddTransitItemsForm(allif_data.get("main_sbscrbr_entity"))
        allifqueryset= CommonTransitItemsModel.objects.filter(shipment=allifquery)#this line helps to
    
        if request.method=='POST':
            form=CommonAddTransitItemsForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.shipment=allifquery
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.shipment=allifquery
                obj.save()
                return redirect('allifmaalcommonapp:commonAddShipmentItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddTransitItemsForm(allif_data.get("main_sbscrbr_entity"))

        context={
        "form":form,
        "allifquery":allifquery,
       
        "allifqueryset":allifqueryset,
        "title":title, 
       
        }
        return render(request,'allifmaalcommonapp/transport/shipments/add_shipment_items.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditShipmentItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Item Details"
        allif_data=common_shared_data(request)
        myquery=CommonTransitItemsModel.objects.filter(id=pk).first()
        allifquery=myquery.shipment
        allifqueryset=CommonTransitItemsModel.objects.filter(shipment=allifquery)

        form=CommonAddTransitItemsForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)
        if request.method=='POST':
            form=CommonAddTransitItemsForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=myquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.shipment=allifquery
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonAddShipmentItems',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddTransitItemsForm(allif_data.get("main_sbscrbr_entity"), instance=myquery)

        context={"title":title,"form":form,"allifquery":allifquery,
                 "allifqueryset":allifqueryset,"myquery":myquery,}
        return render(request,'allifmaalcommonapp/transport/shipments/add_shipment_items.html',context)
        
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
     
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def commonShipmentItemDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        
        allifquery=CommonTransitItemsModel.objects.filter(id=pk).first()
        title=str(allifquery)+" "+ "Shipment Item Details"
      
        context={
            "allifquery":allifquery,
            "title":title,
          
        }
        return render(request,'allifmaalcommonapp/transport/shipments/shipment_item_details.html',context)
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonDeleteShipmentItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Delete Quote Items"
        allif_data=common_shared_data(request)
       
        myallifquery=CommonTransitItemsModel.objects.filter(id=pk).first()
        myquery=myallifquery.shipment
        myallifquery.delete()
        return redirect('allifmaalcommonapp:commonAddShipmentItems',pk=myquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTransitToPdf(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        date_today=date.today()
       
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        allifquery=CommonTransitModel.objects.filter(id=pk).first()
        allifqueryset=CommonTransitItemsModel.objects.filter(shipment=allifquery)
        title="Shipment "+str(allifquery)
        template_path = 'allifmaalcommonapp/transport/shipment_pdf.html'
        context = {
        "allifqueryset":allifqueryset,
        "allifquery":allifquery,
        "title":title,
        "scopes":scopes,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        "usr_var":allif_data.get("usernmeslg"),
        "date_today":date_today,
            }
        
        response = HttpResponse(content_type='application/pdf')
        response = HttpResponse(content_type='application/doc')
        response['Content-Disposition'] = f'filename="{allifquery} Quote.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        try:
            pisa_status = pisa.CreatePDF(
        html, dest=response)
        except:
            return HttpResponse("Something went wrong!")
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTransitSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
      
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonTransitModel.objects.filter((Q(shipment_number__icontains=allifsearch)|Q(items__icontains=allifsearch)|Q(customer__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]

        context={
        "title":title,
        "allifsearch":allifsearch,
        "searched_data":searched_data,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        }
        return render(request,'allifmaalcommonapp/transit/transits.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonTransitAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Shipment Search"
        allif_data=common_shared_data(request)
       
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonSalariesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
        lastDate=CommonTransitModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
        largestAmount=CommonTransitModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-total').first().total
        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonQuotesModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(total__gte=start_value or 0) & Q(total__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/shipments/shipment_advanced_search.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                   "datashorts":datasorts,
                   "formats":formats,
                   "scopes":scopes,
                    }
                    
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
                    response = HttpResponse(content_type='application/doc')
                    response['Content-Disposition'] = 'filename="shipments-advanced-searched-results.pdf"'
                    template = get_template(template_path)
                    html = template.render(allifcontext)
                    try:
                        pisa_status=pisa.CreatePDF(html, dest=response)
                    except Exception as ex:
                        error_context={'error_message': ex,}
                        return render(request,'allifmaalcommonapp/error/error.html',error_context)
                    # if error then show some funy view
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                # if excel is selected
                
                else:
                    searched_data=[]
                    context = {
                    "searched_data":searched_data,
                   
                    }
                    return render(request, 'allifmaalcommonapp/quotes/quotes.html',context)
                    
            else:
                searched_data=[]
             
                context={
            "searched_data":searched_data,
                }
                return render(request, 'allifmaalcommonapp/quotes/quotes.html',context)
           
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request, 'allifmaalcommonapp/quotes/quotes.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
########################### END OF QUOTATION ###############


########################## progress reporting/recording

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin
def commonProgress(request,pk,*allifargs,**allifkwargs):
    title="Progress Records"
    try:
        allifquery=CommonTransactionsModel.objects.filter(id=pk).first()
        allif_data=common_shared_data(request)
        allifqueryset=CommonProgressModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),trans_number=allifquery)
        context={"title":title,"allifqueryset":allifqueryset,"allifquery":allifquery,}
        return render(request,'allifmaalcommonapp/records/progress/progress.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
@logged_in_user_is_admin
def commonAddProgress(request,pk,*allifargs,**allifkwargs):
    title="Add New Progress Record"
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonTransactionsModel.objects.filter(id=pk).first()
        form=CommonAddProgressForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddProgressForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.trans_number=allifquery
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonAddProgress',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
               
          

            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddProgressForm(allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "form":form,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/records/progress/add_progress.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_is_admin
def commonEditProgress(request,pk,*allifargs,**allifkwargs):
    title="Update Progress Record Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonProgressModel.objects.filter(id=pk).first()
        allifquery=allifquery_update.trans_number
        form=CommonAddProgressForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddProgressForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonProgress',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddProgressForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context={"title":title,"form":form,"allifquery_update":allifquery_update,"allifquery":allifquery}
        return render(request,'allifmaalcommonapp/records/progress/add_progress.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonProgressSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonProgressModel.objects.filter((Q(description__icontains=allifsearch)|Q(trans_number__number__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        
        else:
            searched_data=[]

        context={
        
        "title":title,
        "searched_data":searched_data,
        
        }
        return render(request,'allifmaalcommonapp/records/progress/progress.html',context)
        
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def commonProgressDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Space Unit Details"
        allifquery=CommonProgressModel.objects.filter(id=pk).first()
      
        context={
            "allifquery":allifquery,
            "title":title,
          
        }
        return render(request,'allifmaalcommonapp/records/progress/progress_details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_departmental_delete
@logged_in_user_can_delete
def commonWantToDeleteProgress(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonProgressModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/records/progress/delete_progress_confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_universal_delete
@logged_in_user_can_delete
def commonDeleteProgress(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        
        allifdata=CommonProgressModel.objects.filter(id=pk).first()
        trans_id=allifdata.trans_number.id
        allifdata.delete()
      
        return redirect('allifmaalcommonapp:commonProgress',pk=trans_id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

###################3 customer contacts messages ###################3
def commonCustomerContacts(request):
    try:
        if request.method=='POST':
            name=request.POST.get('name')
            subject=request.POST.get('subject')
            email=request.POST.get('email')
            message=request.POST.get('message')
            custom_info=CommonContactsModel(name=name,subject=subject,email=email,message=message)
            custom_info.save()
            return redirect("allifmaalcommonapp:commonWebsite")
        else:
            pass
        return render(request,"allifmaalcommonapp/website/website.html")
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)

































#######3 you might delete all below if not used .... #####################

################3 common programs... ######################33

@logged_in_user_must_have_profile
@logged_in_user_can_view
def commonPrograms(request,*allifargs,**allifkwargs):
    title="Programs"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonProgramsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/operations/programs/programs.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddProgram(request,*allifargs,**allifkwargs):
    try:
        title="Add New Program"
        allif_data=common_shared_data(request)
        form=CommonAddProgramForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddProgramForm(allif_data.get("main_sbscrbr_entity"),request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonPrograms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddProgramForm(allif_data.get("main_sbscrbr_entity"))

        context={
            "form":form,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/operations/programs/add_program.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_edit
def commonEditProgram(request,pk,*allifargs,**allifkwargs):
    title="Edit The Program Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonProgramsModel.objects.filter(id=pk).first()
        form=CommonAddProgramForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddProgramForm(allif_data.get("main_sbscrbr_entity"),request.POST, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonPrograms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddProgramForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context = {
            'form':form,
            "allifquery_update":allifquery_update,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/operations/programs/add_program.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile  
@logged_in_user_can_delete
def commonDeleteProgram(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonProgramsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonPrograms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonProgramDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Program Details"
        allif_data=common_shared_data(request)
        allifquery=CommonProgramsModel.objects.filter(id=pk).first()
        allifqueryset=CommonServicesModel.objects.filter(program=allifquery,company=allif_data.get("main_sbscrbr_entity"))
        
        context={
            "allifquery":allifquery,
            "title":title,
            "allifqueryset":allifqueryset,
           
        }
        return render(request,'allifmaalcommonapp/operations/programs/program_details.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_can_delete  
def commonWantToDeleteProgram(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonProgramsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/operations/programs/delete_program_confirm.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view 
def commonProgramSearch(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Search Results"
        searched_data=[]
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            if allif_data.get("logged_in_user_has_universal_access")==True:
                searched_data=CommonProgramsModel.objects.filter((Q(name__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(description__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
            elif allif_data.get("logged_in_user_has_divisional_access")==True:
                searched_data=CommonProgramsModel.objects.filter((Q(name__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(description__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")) & Q(division=allif_data.get("logged_user_division")))
            elif allif_data.get("logged_in_user_has_branches_access")==True:
                searched_data=CommonProgramsModel.objects.filter((Q(name__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(description__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")) & Q(division=allif_data.get("logged_user_division")) & Q(branch=allif_data.get("logged_user_branch")))
            elif allif_data.get("logged_in_user_has_departmental_access")==True:
                searched_data=CommonProgramsModel.objects.filter((Q(name__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(description__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")) & Q(division=allif_data.get("logged_user_division")) & Q(department=allif_data.get("logged_user_department")) & Q(branch=allif_data.get("logged_user_branch")))
            else:
                searched_data=[]
        else:
            searched_data=[]

        context={"title":title,"allifsearch":allifsearch,"searched_data":searched_data,}
        return render(request,'allifmaalcommonapp/operations/programs/programs.html',context)
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)  

###############################3 common services/subjects/etc ##############

@logged_in_user_must_have_profile
@logged_in_user_can_view
def commonServices(request,*allifargs,**allifkwargs):
    title="Offerred Programs and Services"
    try:
        allif_data=common_shared_data(request)
        allifqueryset=CommonServicesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/operations/programs/services/services.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonAddService(request,*allifargs,**allifkwargs):
    try:
        title="Add New Service - Program "
        allif_data=common_shared_data(request)
        form=CommonAddServiceForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonAddServiceForm(allif_data.get("main_sbscrbr_entity"),request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonServices',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddServiceForm(allif_data.get("main_sbscrbr_entity"))

        context={
            "form":form,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/operations/programs/services/add_service.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@logged_in_user_can_edit
def commonEditService(request,pk,*allifargs,**allifkwargs):
    title="Edit The Service Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=CommonServicesModel.objects.filter(id=pk).first()
        form=CommonAddServiceForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonAddServiceForm(allif_data.get("main_sbscrbr_entity"),request.POST, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonServices',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddServiceForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context = {
            'form':form,
            "allifquery_update":allifquery_update,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/operations/programs/services/add_service.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile  
@logged_in_user_can_delete
def commonDeleteService(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonServicesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonServices',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonServiceDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Program Details"
        allif_data=common_shared_data(request)
        allifquery=CommonServicesModel.objects.filter(id=pk).first()
        #allifqueryset=CommonServicesModel.objects.filter(program=allifquery,company=allif_data.get("main_sbscrbr_entity"))
        
        context={
            "allifquery":allifquery,
            "title":title,
            #"allifqueryset":allifqueryset,
           
        }
        return render(request,'allifmaalcommonapp/operations/programs/services/service_details.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_can_delete  
def commonWantToDeleteService(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonServicesModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/operations/programs/services/delete_service_confirm.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view 
def commonServiceSearch(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Search Results"
        searched_data=[]
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            if allif_data.get("logged_in_user_has_universal_access")==True:
                searched_data=CommonServicesModel.objects.filter((Q(name__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(description__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
            elif allif_data.get("logged_in_user_has_divisional_access")==True:
                searched_data=CommonServicesModel.objects.filter((Q(name__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(description__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")) & Q(division=allif_data.get("logged_user_division")))
            elif allif_data.get("logged_in_user_has_branches_access")==True:
                searched_data=CommonServicesModel.objects.filter((Q(name__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(description__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")) & Q(division=allif_data.get("logged_user_division")) & Q(branch=allif_data.get("logged_user_branch")))
            elif allif_data.get("logged_in_user_has_departmental_access")==True:
                searched_data=CommonServicesModel.objects.filter((Q(name__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(description__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")) & Q(division=allif_data.get("logged_user_division")) & Q(department=allif_data.get("logged_user_department")) & Q(branch=allif_data.get("logged_user_branch")))
            else:
                searched_data=[]
        else:
            searched_data=[]

        context={"title":title,"allifsearch":allifsearch,"searched_data":searched_data,}
        return render(request,'allifmaalcommonapp/operations/programs/services/services.html',context)
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)     
    
    
    