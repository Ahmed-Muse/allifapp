from django.shortcuts import render,redirect,get_object_or_404
from.models import *
from datetime import date
from django.core.mail import send_mail
from .allifutils import common_shared_data
from django.db import IntegrityError, transaction # Import transaction for atomicity
from django.http import Http404
from typing import Optional # Import Optional for type hinting
from django.db import transaction # For transactions
from django.core.cache import cache # For caching
from django.forms import modelformset_factory # For formsets

from allifmaalcommonapp.utils import  (allif_filtered_and_sorted_queryset,allif_common_detail_view,allif_main_models_registry,allif_delete_hanlder,allif_common_form_submission_and_save,
allif_common_form_edit_and_save,allif_redirect_based_on_sector,allif_delete_confirm,allif_excel_upload_handler,allif_search_handler, allif_advance_search_handler,allif_document_pdf_handler)
# ... (existing imports) ...
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Import your navigation links configuration
from .searchable_links import allifmaal_general_links, allifmaal_sector_specific_links 

import logging
logger = logging.getLogger('allifmaalcommonapp')

# ... (your existing views) ...
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
from .decorators import logged_in_user_can_approve,allif_view_exception_handler,allif_base_view_wrapper, subscriber_company_status, logged_in_user_must_have_profile,logged_in_user_has_universal_delete,logged_in_user_has_divisional_delete,logged_in_user_has_branches_delete,logged_in_user_has_departmental_delete,logged_in_user_has_universal_access,logged_in_user_has_divisional_access,logged_in_user_has_branches_access,logged_in_user_has_departmental_access,allifmaal_admin,allifmaal_admin_supperuser, unauthenticated_user,allowed_users,logged_in_user_is_owner_ceo,logged_in_user_can_add,logged_in_user_can_view,logged_in_user_can_edit,logged_in_user_can_delete,logged_in_user_is_admin
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
from django.contrib.auth.decorators import login_required, permission_required 

def audit_log_list_view(request, *allifargs, **allifkwargs):
    title = "System Audit Logs"
    current_company = None # Initialize to None to be safe
    allifqueryset=CommonAuditLogsModel.objects.all()
   
    try:
        allif_data = common_shared_data(request)
        # CRITICAL: Ensure 'main_sbscrbr_entity' is the CommonCompanyDetailsModel instance
        # The previous error "Cannot query 'Barasho International Ltd': Must be 'User' instance"
        # was misleading. The main issue was the lookup name 'company_profile'.
        # However, it's still vital that current_company is the actual object, not just its string.
        current_company = allif_data.get("main_sbscrbr_entity")

        logger.debug(f"Audit Log View: User: {request.user.email}")
        if current_company:
            logger.debug(f"Audit Log View: Current Company Type: {type(current_company)}, ID: {current_company.pk}, Name: {current_company.company}")
        else:
            logger.debug(f"Audit Log View: current_company is None.")

        base_query = CommonAuditLogsModel.objects.select_related('user', 'content_type')

        if current_company:
            # --- THE FIX: Use 'user__usercompany' (your CharField) and compare to current_company.company (string) ---
            # This directly compares the 'usercompany' CharField on the User model
            # with the 'company' CharField on the CommonCompanyDetailsModel instance.
            audit_logs = base_query.filter(
                Q(user__usercompany=current_company.company) | Q(user__isnull=True)
            ).order_by('-action_time')[:100]
            logger.debug(f"Audit logs filtered by user's usercompany (CharField) for {current_company.company}. Count: {audit_logs.count()}")
        else:
            # If no current_company is identified, show only logs where the user is NULL (system actions).
            audit_logs = base_query.filter(user__isnull=True).order_by('-action_time')[:100]
            logger.warning(f"No current company found for user {request.user.email} in audit log view. Showing only system logs.")

        context = {
            "title": title,
            "audit_logs": audit_logs,
            "user_var": allif_data.get("usrslg"),
            "glblslug": allif_data.get("compslg"),
            "allifqueryset":allifqueryset,
        }
        return render(request, 'allifmaalcommonapp/logs/audit_log_list.html', context)

    except Exception as ex:
        # --- CRITICAL DEBUGGING STEP: Log the actual exception with traceback ---
        logger.exception(f"Error viewing audit logs for user {request.user.email} (Company: {current_company}): {ex}")
        # Provide a user-friendly error message, but the detailed error is in logs
        error_context = {'error_message': "Could not retrieve audit logs. An unexpected error occurred. Please check the server logs for more details."}
        return render(request, 'allifmaalcommonapp/error/error.html', error_context)


@login_required
def search_erp_features(request, allifusr, allifslug):
    """
    API endpoint to search for ERP features/links, filtered by company sector.
    """
    query = request.GET.get('q', '').lower().strip()
    
    # Get current company and its sector
    current_company = None
    try:
        # Assuming allif_data.get("main_sbscrbr_entity") provides the CommonCompanyDetailsModel instance
        # If not, you might need to fetch it using allifslug:
        # current_company = CommonCompanyDetailsModel.objects.get(companyslug=allifslug)
        allif_data = common_shared_data(request) # You need to ensure this function is accessible and works
        current_company = allif_data.get("main_sbscrbr_entity")

    except Exception as e:
        logger.error(f"Could not retrieve current company for feature search: {e}")
        # Fallback if company data is missing, maybe return only general links
        current_company = None
    
    # Determine the company's sector name
    company_sector_name = None
    if current_company and current_company.sector:
        company_sector_name = current_company.sector.name # Assuming sector.name is the string key in your dict
    
    # --- Combine General and Sector-Specific Links ---
    available_features = list(allifmaal_general_links) # Start with all general links

    if company_sector_name and company_sector_name in allifmaal_sector_specific_links:
        # Add links specific to the company's sector
        available_features.extend(allifmaal_sector_specific_links[company_sector_name])
        logger.debug(f"Including sector-specific links for: {company_sector_name}")
    else:
        logger.info(f"No specific sector links found for sector: {company_sector_name}. Only general links will be available.")

    results = []
    if query:
        for feature in available_features:
            # Check if query matches name, description, or category
            # Add 'category' to ERP_FEATURES in navigation_links.py if you want to search by it
            search_text = f"{feature.get('name', '')} {feature.get('description', '')} {feature.get('category', '')}".lower()
            
            if query in search_text:
                # --- Generate the full URL here in Python ---
                try:
                    if feature['url_name'] == 'allifmaalcommonapp:commonWebsite':
                        full_url = reverse(feature['url_name'])
                    else:
                        # For all other URLs, pass allifusr and allifslug
                        # Ensure all features in ERP_FEATURES are resolvable with these two args
                        full_url = reverse(feature['url_name'], args=[allifusr, allifslug])
                except Exception as e:
                    logger.warning(f"Could not reverse URL for feature '{feature['name']}' ({feature['url_name']}): {e}")
                    full_url = "#" # Fallback to a non-functional link if URL cannot be resolved

                feature_data = {
                    'name': feature['name'],
                    'description': feature.get('description', ''), # Ensure description is always present
                    'category': feature.get('category', 'General'), # Ensure category is always present
                    'url': full_url,
                }
                results.append(feature_data)
                
                if len(results) >= 10: # Max 10 suggestions
                    break
    
    logger.debug(f"Feature search by {request.user.email} for '{query}' (Sector: {company_sector_name}): found {len(results)} results.")
    return JsonResponse({'features': results})


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
    
def commonForTesting(request,*allifargs,**allifkwargs):
    title="Update Scope Details"
   
    allif_data=common_shared_data(request)
    allifquery=CommonCompanyScopeModel.objects.get(pk=2)
    form=CommonAddCompanyScopeForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery)
    #allifquery = get_object_or_404(CommonCompanyScopeModel, id=allifquery)
    
    # Initialize the form
    # Assuming glblslug can be used as allifmaalparameter (company_id)
    company_instance = CommonCompanyDetailsModel.objects.get(pk=1)
    
    if request.method == 'POST':
        form = CommonAddCompanyScopeForm(company_instance.id, request.POST, instance=allifquery)
        if form.is_valid():
            scope_instance = form.save(commit=False)
            # These are handled by auto_now_add/auto_now or set in view's save() hook
            # scope_instance.owner = request.user
            # scope_instance.updated_by = request.user
            scope_instance.save()
            return redirect('success_url_for_scope') # Replace with actual URL
    else:
        form = CommonAddCompanyScopeForm(company_instance.id, instance=allifquery)

    context = {
        'title': f'Scope: {allifquery.name}',
        'allifquery': allifquery, # The model instance itself is enough for display tags
        'form': form, # The form instance itself is enough for form tags
       
    }
    return render(request,'allifmaalcommonapp/base/company_scope_detail.html',context)
      
    
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
   
@allif_view_exception_handler 
@login_required(login_url='allifmaalusersapp:userLoginPage')
def CommonDecisionPoint(request, *allifargs, **allifkwargs):
    allif_data = common_shared_data(request)
    company_entity = allif_data.get("main_sbscrbr_entity")
    if not company_entity or not allif_data.get("compslg"):
        # If company entity is not set or company slug is missing, redirect to company creation
        return redirect('allifmaalcommonapp:commonAddnewEntity', allifusr=allif_data.get("usrslg"))
    else:
        # Company exists, redirect based on sector to the 'home' type URL
        return allif_redirect_based_on_sector(request, allif_data, 'home')


@allif_view_exception_handler 
@login_required(login_url='allifmaalusersapp:userLoginPage')
def commonHome(request, *allifargs, **allifkwargs):
    allif_data = common_shared_data(request)
    if request.user.email.endswith("info@allifmaal.com"):
        pass
    company_entity = allif_data.get("main_sbscrbr_entity")
    if company_entity:
        return allif_redirect_based_on_sector(request, allif_data, 'home')
    else:
        # Fallback if company_entity is unexpectedly None here (should be caught by decorators/DecisionPoint)
        logger.warning("commonHome called without a main_sbscrbr_entity. Redirecting to CommonDecisionPoint.")
        return redirect('allifmaalcommonapp:CommonDecisionPoint')

@allif_view_exception_handler 
@login_required(login_url='allifmaalusersapp:userLoginPage')
def commonSpecificDashboard(request, *allifargs, **allifkwargs):
    allif_data = common_shared_data(request)
    company_entity = allif_data.get("main_sbscrbr_entity")
    if company_entity:
        # Company exists, redirect based on sector to the 'dashboard' type URL
        return allif_redirect_based_on_sector(request, allif_data, 'dashboard')
    else:
        # Fallback if company_entity is unexpectedly None here
        logger.warning("commonSpecificDashboard called without a main_sbscrbr_entity. Redirecting to CommonDecisionPoint.")
        return redirect('allifmaalcommonapp:CommonDecisionPoint')
     
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


########################## upload excel function ###########################
def commonUploadExcel(request, model_config_key, *allifargs, **allifkwargs):
    """
    Handles the Excel upload process by delegating to the centralized handler.
    The `model_config_key` will determine which model's data is being uploaded.
    """
    # Determine the redirect URL based on the model being uploaded
    # You might want to make this more dynamic, e.g., from EXCEL_UPLOAD_CONFIGS
    if model_config_key == 'CommonCurrenciesModel':
        success_redirect_url_name = 'commonCurrencies'
    elif model_config_key == 'CommonStocksModel':
        success_redirect_url_name = 'commonStocks' # Assuming you have a commonStocks list view
    elif model_config_key == 'CommonCustomersModel':
        success_redirect_url_name = 'commonCustomers' # Assuming you have a commonCustomers list view
    elif model_config_key == 'CommonSuppliersModel':
        success_redirect_url_name = 'commonSuppliers' # Assuming you have a commonSuppliers list view
    else:
        messages.error(request, f'No specific redirect URL defined for model config key: {model_config_key}.')
        # Fallback to a generic home page or error page
        allif_data = common_shared_data(request)
        return redirect('allifmaalcommonapp:commonHome', allifusr=allif_data.get("usrslg"), allifslug=allif_data.get("compslg"))

    return allif_excel_upload_handler(request, model_config_key, success_redirect_url_name)

# ... (rest of your views.py) ...

########################3 currencies ######################
@allif_base_view_wrapper
def commonCurrencies(request,*allifargs,**allifkwargs):
    title="Currencies"
    allif_data=common_shared_data(request)
    formats=CommonDocsFormatModel.objects.all() # Assuming this is needed for the advanced search form
    allifqueryset=allif_filtered_and_sorted_queryset(request, allif_main_models_registry['CommonCurrenciesModel'], allif_data)
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonCurrenciesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/currencies/currencies.html',context)


@allif_base_view_wrapper
def commonAddCurrency(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddCurrencyForm,"Add New Currency","commonCurrencies",'allifmaalcommonapp/currencies/add-currency.html')

@allif_base_view_wrapper
def commonEditCurrency(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddCurrencyForm,"Edit Currency","commonCurrencies",'allifmaalcommonapp/currencies/add-currency.html')


@allif_base_view_wrapper
def commonWantToDeleteCurrency(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonCurrenciesModel,"Delete this item",'allifmaalcommonapp/currencies/delete-currency-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteCurrency(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonCurrenciesModel',pk=pk,success_redirect_url_name='commonCurrencies')


@allif_base_view_wrapper
def commonCurrencySearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonCurrenciesModel',search_fields_key='CommonCurrenciesModel',
        template_path='allifmaalcommonapp/currencies/currencies.html', # The template to render results
        search_input_name='allifsearchcommonfieldname', # The name of your search input field
        )

@allif_base_view_wrapper
def commonCurrencyAdvanceSearch(request,*allifargs,**allifkwargs):
    # This view now simply calls the centralized advanced search handler
    return allif_advance_search_handler(request,model_name='CommonCurrenciesModel',advanced_search_config_key='CommonCurrenciesModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/currencies/currencies.html', # Template for HTML results
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html', # <-- CRITICAL: Pass the PDF template path
    )

@allif_base_view_wrapper
def common_currency_pdf(request, pk, *allifargs, **allifkwargs):
    return allif_document_pdf_handler(request,pk=pk,document_config_key='CommonCurrenciesModel',)
 
 
########################3 Payment terms ######################
@allif_base_view_wrapper
def commonPaymentTerms(request,*allifargs,**allifkwargs):
    title="Payment Terms"
    allif_data=common_shared_data(request)
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonPaymentTermsModel,allif_data)
    context={"title":title,"allifqueryset":allifqueryset,}
    return render(request,'allifmaalcommonapp/payments/terms/payment_terms.html',context)

@allif_base_view_wrapper
def commonAddPaymentTerm(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddPaymentTermForm,"New Payment Term","commonPaymentTerms",'allifmaalcommonapp/payments/terms/add_payment_term.html')

@allif_base_view_wrapper
def commonEditPaymentTerm(request,pk,*allifargs,**allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddPaymentTermForm,"Edit","commonPaymentTerms",'allifmaalcommonapp/payments/terms/add_payment_term.html')

@allif_base_view_wrapper
def commonDeletePaymentTerm(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonPaymentTermsModel',pk=pk,success_redirect_url_name='commonPaymentTerms')


@allif_base_view_wrapper
def commonWantToDeletePaymentTerm(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonPaymentTermsModel,"Delete this item",'allifmaalcommonapp/payments/terms/delete-payment-term-confirm.html')


  
############################ units of measure section #########
@allif_base_view_wrapper
def commonUnits(request,*allifargs,**allifkwargs):
    title="Units of Measure"
    allif_data=common_shared_data(request)
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonUnitsModel,allif_data)
    context={"title":title,"allifqueryset":allifqueryset,}
    return render(request,'allifmaalcommonapp/units/units.html',context)

@allif_base_view_wrapper
def commonAddUnit(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddUnitForm,"Add Unit","commonUnits",'allifmaalcommonapp/units/add_unit.html')

@allif_base_view_wrapper
def commonEditUnit(request,pk,*allifargs,**allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddUnitForm,"Edit Unit","commonUnits",'allifmaalcommonapp/units/add_unit.html')

@allif_base_view_wrapper
def commonDeleteUnit(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonUnitsModel',pk=pk,success_redirect_url_name='commonUnits')

@allif_base_view_wrapper
def commonConfirmDeleteUnits(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonUnitsModel,"Delete this item",'allifmaalcommonapp/units/delete-unit-confirm.html')


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
                obj.updated_by=allif_data.get("usernmeslg")
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
                
                obj.updated_by=allif_data.get("usernmeslg")
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
    

    

   
########################################33 categories ####################3
@allif_base_view_wrapper
def commonCategories(request,*allifargs,**allifkwargs):
    title="Main Categories"
    allif_data=common_shared_data(request)
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonCategoriesModel,allif_data)
    
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,}
    return render(request,'allifmaalcommonapp/operations/categories/categories.html',context)

@allif_base_view_wrapper
def commonAddCategory(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonCategoryAddForm,"Add Category","commonCategories",'allifmaalcommonapp/operations/categories/add-category.html')

@allif_base_view_wrapper
def commonEditCategory(request,pk,*allifargs,**allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonCategoryAddForm,"Edit Category","commonCategories",'allifmaalcommonapp/operations/categories/add-category.html')

@allif_base_view_wrapper
def commonDeleteCategory(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonCategoriesModel',pk=pk,success_redirect_url_name='commonCategories')

@allif_base_view_wrapper
def commonWantToDeleteCategory(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonCategoriesModel,"Delete this item",'allifmaalcommonapp/operations/categories/x-category-cnfrm.html')


@allif_base_view_wrapper
def commonCategorySearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonCategoriesModel',search_fields_key='CommonCategoriesModel',
        template_path='allifmaalcommonapp/operations/categories/categories.html', # The template to render results
        search_input_name='allifsearchcommonfieldname', )
@allif_base_view_wrapper
def commonCategoryDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=CommonCategoriesModel,pk=pk,
        template_name='allifmaalcommonapp/operations/categories/category-details.html',)

#############################3 CODES #########################3

   
########################################33 codes ####################3
@allif_base_view_wrapper
def commonCodes(request,*allifargs,**allifkwargs):
    title="Main Codes"
    allif_data=common_shared_data(request)
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonCodesModel,allif_data)
    
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,}
    return render(request,'allifmaalcommonapp/operations/codes/codes.html',context)

@allif_base_view_wrapper
def commonAddCode(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddCodeForm,"Add Code","commonCodes",'allifmaalcommonapp/operations/codes/add_code.html')

@allif_base_view_wrapper
def commonEditCode(request,pk,*allifargs,**allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddCodeForm,"Edit Code","commonCodes",'allifmaalcommonapp/operations/codes/add_code.html')

@allif_base_view_wrapper
def commonDeleteCode(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonCodesModel',pk=pk,success_redirect_url_name='commonCodes')

@allif_base_view_wrapper
def commonWantToDeleteCode(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonCodesModel,"Delete this item",'allifmaalcommonapp/operations/codes/delete-code-confirm.html')

@allif_base_view_wrapper
def commonCodeSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonCodesModel',search_fields_key='CommonCodesModel',
        template_path='allifmaalcommonapp/operations/codes/codes.html', # The template to render results
        search_input_name='allifsearchcommonfieldname', )
@allif_base_view_wrapper
def commonCodeDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=CommonCodesModel,pk=pk,
        template_name='allifmaalcommonapp/operations/codes/code_details.html',)
  
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

#############################3 company scopes ###################3
@allif_base_view_wrapper
def commonCompanyScopes(request,*allifargs,**allifkwargs):
    title="Scopes"
    allif_data=common_shared_data(request)
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonCompanyScopeModel,allif_data)
    
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,}
    return render(request,'allifmaalcommonapp/scopes/scopes.html',context)

@allif_base_view_wrapper
def commonAddCompanyScope(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddCompanyScopeForm,"Add Scope","commonCompanyScopes",'allifmaalcommonapp/scopes/add-scope.html')

@allif_base_view_wrapper
def commonEditCompanyScope(request,pk,*allifargs,**allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddCompanyScopeForm,"Edit Scope","commonCompanyScopes",'allifmaalcommonapp/scopes/add-scope.html')

@allif_base_view_wrapper
def commonDeleteCompanyScope(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonCompanyScopeModel',pk=pk,success_redirect_url_name='commonCompanyScopes')

@allif_base_view_wrapper
def commonWantToDeleteScope(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonCompanyScopeModel,"Delete this item",'allifmaalcommonapp/scopes/delete-scope-confirm.html')

    

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
        form=CommonAddDivisionForm()
        allifquery=CommonDivisionsModel.objects.filter(id=pk).first()
        relatedqueryset=CommonBranchesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allifquery)
        context={
        "allifquery":allifquery,
        "relatedqueryset": relatedqueryset,
        "title":title,
        "form":form,
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
        #allifqueryset=CommonBranchesModel.objects.all()
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
    
def commonEditStaffProfile(request,pk,*allifargs,**allifkwargs):
    title="Update Staff Profile Details"
    try:
        allif_data=common_shared_data(request)
        updateItem= CommonEmployeesModel.all_objects.filter(id=pk).first()
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

def commonStaffProfileDetails(request, pk, *allifargs, **allifkwargs):
    """
    Shows details of a General Ledger account, including its related Chart of Accounts entries.
    """
    return allif_common_detail_view(
        request,
        model_class=CommonEmployeesModel,
        pk=pk,
        template_name='allifmaalcommonapp/hrm/profiles/profile-details.html',
        title_map={'default': 'Staff Profile Details'},
       
    )



@logged_in_user_must_have_profile
@subscriber_company_status
def commonWantToDeleteProfile(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonEmployeesModel.all_objects.filter(id=pk).first()
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
@allif_base_view_wrapper
def commonApprovers(request,*allifargs,**allifkwargs):
    title="Approvers"
    allif_data=common_shared_data(request)
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonApproversModel,allif_data)
    
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,}
    return render(request,'allifmaalcommonapp/approvers/approvers.html',context)

@allif_base_view_wrapper
def commonAddApprover(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddApproverForm,"Add Approver","commonApprovers",'allifmaalcommonapp/approvers/add-approver.html')

@allif_base_view_wrapper
def commonEditApprover(request,pk,*allifargs,**allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddApproverForm,"Edit Approver","commonApprovers",'allifmaalcommonapp/approvers/add-approver.html')

@allif_base_view_wrapper
def commonDeleteApprover(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonApproversModel',pk=pk,success_redirect_url_name='commonApprovers')

@allif_base_view_wrapper
def commonWantToDeleteApprover(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonApproversModel,"Delete this item",'allifmaalcommonapp/approvers/delete-approver-confirm.html')

@allif_base_view_wrapper
def commonApproverDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=CommonApproversModel,pk=pk,
        template_name='allifmaalcommonapp/approvers/approver-details.html',)
    
    

###################333 tax parameters settings ###############

@allif_base_view_wrapper
@permission_required('allifmaalcommonapp.add_tax_parameter', raise_exception=True)
@login_required
def commonTaxParameters(request,*allifargs,**allifkwargs):
    title="Tax Parameters"
    allif_data=common_shared_data(request)
    current_company = allif_data.get("main_sbscrbr_entity")
    
    allifqueryset = CommonTaxParametersModel.objects.filter(company=current_company).select_related(
        'company', 'division', 'branch', 'department', 'owner', 'operation_year', 'operation_term', 'updated_by'
    ).order_by('-date')

    # --- Principle 7: Caching Strategy (Example: Caching latest taxes) ---
    # Analogy: Keeping frequently used documents on your desk instead of retrieving from archive.
    cache_key = f'latest_taxes_company_{current_company.pk}'
    latest = cache.get(cache_key)
    if not latest:
        latest = allifqueryset[:3] # Use the optimized queryset
        cache.set(cache_key, latest, 60 * 5) # Cache for 5 minutes
        logger.info(f"Cache MISS for {cache_key}, data fetched from DB.")
    elif latest:
        logger.info("Tax parameter  saved successfully.")
    else:
        logger.info(f"Cache HIT for {cache_key}.")

    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonTaxParametersModel,allif_data)
    
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,}
    return render(request,'allifmaalcommonapp/taxes/taxes.html',context)

@allif_base_view_wrapper
def commonAddATaxParameter(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddTaxParameterForm,"Add Tax","commonTaxParameters",'allifmaalcommonapp/taxes/add-update-tax.html')

@allif_base_view_wrapper
def CommonUpdateTaxDetails(request,pk,*allifargs,**allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddTaxParameterForm,"Edit Tax","commonTaxParameters",'allifmaalcommonapp/taxes/add-update-tax.html')

@allif_base_view_wrapper
def CommonDeleteTaxParameter(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonTaxParametersModel',pk=pk,success_redirect_url_name='commonTaxParameters')

@allif_base_view_wrapper
def commonWantToDeleteTaxParameter(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonTaxParametersModel,"Delete this item",'allifmaalcommonapp/taxes/delete-tax-confirm.html')



#####################3 supplier tax parameters ##########


@allif_base_view_wrapper
#@permission_required('allifmaalcommonapp.add_tax_parameter', raise_exception=True)
#@login_required
def commonSupplierTaxParameters(request,*allifargs,**allifkwargs):
    title="Supplier Tax Parameters"
    allif_data=common_shared_data(request)
    current_company = allif_data.get("main_sbscrbr_entity")
    
    allifqueryset = CommonSupplierTaxParametersModel.objects.filter(company=current_company).select_related(
        'company', 'division', 'branch', 'department', 'owner', 'operation_year', 'operation_term', 'updated_by'
    ).order_by('-date')

    # --- Principle 7: Caching Strategy (Example: Caching latest taxes) ---
    # Analogy: Keeping frequently used documents on your desk instead of retrieving from archive.
    cache_key = f'latest_taxes_company_{current_company.pk}'
    latest = cache.get(cache_key)
    if not latest:
        latest = allifqueryset[:3] # Use the optimized queryset
        cache.set(cache_key, latest, 60 * 5) # Cache for 5 minutes
        logger.info(f"Cache MISS for {cache_key}, data fetched from DB.")
    elif latest:
        logger.info("Tax parameter  saved successfully.")
    else:
        logger.info(f"Cache HIT for {cache_key}.")

    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonSupplierTaxParametersModel,allif_data)
    
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,}
    return render(request,'allifmaalcommonapp/taxes/suppliertaxes.html',context)

@allif_base_view_wrapper
def commonAddSupplierTaxParameter(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonSupplierAddTaxParameterForm,"Add Supplier Tax","commonSupplierTaxParameters",'allifmaalcommonapp/taxes/add-supplier-tax.html')

@allif_base_view_wrapper
def CommonSupplierUpdateTaxDetails(request,pk,*allifargs,**allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonSupplierAddTaxParameterForm,"Edit Supplier Tax","commonSupplierTaxParameters",'allifmaalcommonapp/taxes/add-supplier-tax.html')

@allif_base_view_wrapper
def CommonSupplierDeleteTaxParameter(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonSupplierTaxParametersModel',pk=pk,success_redirect_url_name='commonSupplierTaxParameters')

@allif_base_view_wrapper
def commonWantToDeleteSupplierTaxParameter(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonSupplierTaxParametersModel,"Delete this item",'allifmaalcommonapp/taxes/delete-supplier-tax-confirm.html')


################################3 GENERAL LEDGER ACCOUNTS ###########################
@allif_base_view_wrapper
def commonGeneralLedgers(request,*allifargs,**allifkwargs):
    title="General Ledger Accounts"
    allif_data=common_shared_data(request)
    
    #allifqueryset=allif_filtered_and_sorted_queryset(request, allif_main_models_registry['CommonCurrenciesModel'], allif_data)
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonGeneralLedgersModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,}
    return render(request,'allifmaalcommonapp/accounts/genledgers.html',context)


@allif_base_view_wrapper
def commonAddGeneralLedger(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddGeneralLedgerForm,"New General Ledger","commonGeneralLedgers",'allifmaalcommonapp/accounts/add-gl.html')

@allif_base_view_wrapper
def commonEditGeneralLedger(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddGeneralLedgerForm,"Edit Currency","commonGeneralLedgers",'allifmaalcommonapp/accounts/add-gl.html')

def commonGeneralLedgerDetails(request, pk, *allifargs, **allifkwargs):
    """
    Shows details of a General Ledger account, including its related Chart of Accounts entries.
    """
    return allif_common_detail_view(
        request,
        model_class=CommonGeneralLedgersModel,
        pk=pk,
        template_name='allifmaalcommonapp/accounts/gl-details.html',
        title_map={'default': 'General Ledger Details'},
        related_data_configs=[
            {
                # IMPORTANT: Change 'context_key' to something unique, NOT 'allifqueryset'
                'context_key': 'allifqueryset', # This will be available in template as {{ related_chart_accounts }}
                'related_model': 'CommonChartofAccountsModel', # String name of the related model
                # IMPORTANT: This filter_field MUST be the name of the ForeignKey field
                # on CommonChartofAccountsModel that points to CommonGeneralLedgersModel.
                # Common examples: 'general_ledger', 'gl_account', 'parent_gl'
                'filter_field': 'category', # <--- YOU MUST VERIFY THIS FIELD NAME
                'order_by': ['code'], # Order the related items by their account number
                # 'prefetch_related': [], # Add prefetch if CommonChartofAccountsModel has FKs you display (e.g., 'currency')
            }
        ]
    )


@allif_base_view_wrapper
def commonWantToDeleteGenLedger(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonGeneralLedgersModel,"Delete this item",'allifmaalcommonapp/accounts/delete-gl-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteGeneralLedger(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonGeneralLedgersModel',pk=pk,success_redirect_url_name='commonGeneralLedgers')

def commonSynchGLAccount(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonGeneralLedgersModel.all_objects.filter(id=pk,company=allif_data.get("main_sbscrbr_entity")).first()
        related_coa_accs=CommonChartofAccountsModel.all_objects.filter(category=allifquery,company=allif_data.get("main_sbscrbr_entity"))
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

"""
def commonCustomerDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(
        request,
        model_class=CommonCustomersModel,
        pk=pk,
        template_name='allifmaalcommonapp/customers/customer-details.html',
        title_map={
            "Healthcare": "Patient Details",
            "Education": "Student Details",
            "default": "Customer Details",
        },
        # Example: If you want to show customer's recent invoices
        # related_data_configs=[
        #     {
        #         'context_key': 'customer_invoices',
        #         'related_model': 'CommonInvoicesModel',
        #         'filter_field': 'customer', # Field on CommonInvoicesModel linking to CommonCustomersModel
        #         'order_by': ['-invoice_date'],
        #         'prefetch_related': ['invoice_items'], # Prefetch related invoice items for each invoice
        #     }
        # ]
    )
"""
# ... (Continue for other detail views) ...
####################### chart of accounts ########################

@allif_base_view_wrapper
def commonChartofAccounts(request,*allifargs,**allifkwargs):
    title="Chart of Accounts"
    allif_data=common_shared_data(request)
    formats=CommonDocsFormatModel.objects.all() # Assuming this is needed for the advanced search form
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
    form=CommonFilterCOAForm(allif_data.get("main_sbscrbr_entity"))
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonChartofAccountsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,
              "assets_tot_val":assets_tot_val,
            "liablts_tot_val":liablts_tot_val,
            "equity_tot_val":equity_tot_val,
            "sum_liablts_and_equity":sum_liablts_and_equity,
            "datasorts":datasorts,
            "formats":formats,
            "form":form,
            }
    return render(request,'allifmaalcommonapp/accounts/chart-of-accs.html',context)


@allif_base_view_wrapper
def commonAddChartofAccount(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddChartofAccountForm,"Add New Account","commonChartofAccounts",'allifmaalcommonapp/accounts/add-coa.html')

@allif_base_view_wrapper
def commonEditChartofAccount(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddChartofAccountForm,"Edit Account","commonChartofAccounts",'allifmaalcommonapp/accounts/add-coa.html')

@allif_base_view_wrapper
def commonWantToDeleteCoA(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonChartofAccountsModel,"Delete this item",'allifmaalcommonapp/accounts/delete-coa-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteChartofAccount(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonChartofAccountsModel',pk=pk,success_redirect_url_name='commonChartofAccounts')


@allif_base_view_wrapper
def commonChartofAccountSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonChartofAccountsModel',search_fields_key='CommonChartofAccountsModel',
        template_path='allifmaalcommonapp/accounts/chart-of-accs.html', # The template to render results
        search_input_name='allifsearchcommonfieldname', # The name of your search input field
        )

@allif_base_view_wrapper
def commonChartofAccAdvanceSearch(request,*allifargs,**allifkwargs):
    # This view now simply calls the centralized advanced search handler
    return allif_advance_search_handler(request,model_name='CommonChartofAccountsModel',advanced_search_config_key='CommonChartofAccountsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/accounts/chart-of-accs.html', # Template for HTML results
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html', # <-- CRITICAL: Pass the PDF template path
        #accounts/coa-search-pdf.html
    )


@allif_base_view_wrapper
def commonChartofAccountDetails(request, pk, *allifargs, **allifkwargs):
    """
    Shows details of an invoice, including its related invoice items.
    """
    return allif_common_detail_view(
        request,
        model_class=CommonChartofAccountsModel,
        pk=pk,
        template_name='allifmaalcommonapp/accounts/coa-details.html', # Create this template
        title_map={'default': 'Chart of A/C Details'},
        #related_data_configs=[
            #{
                #'context_key': 'allifqueryset', # This will be available in template as {{ invoice_items }}
                #'related_model': 'CommonChartofAccountsModel', # Name of the related model
                #'filter_field': 'name', # Field on CommonInvoiceItemsModel that links to CommonInvoicesModel
                #'order_by': ['number'], # Order the items
                #'prefetch_related': ['product'], # If CommonInvoiceItemsModel has a 'product' ForeignKey, prefetch it
            #}
        #]
    )



@allif_base_view_wrapper
def commonSelectedRelatedAccs(request,*allifargs,**allifkwargs):
    
    allif_data=common_shared_data(request)
    if request.method=="GET":
        selectedoption=request.GET.get('allifidforselecteditem')
        selectedcategoryid=CommonGeneralLedgersModel.all_objects.filter(pk=selectedoption,company=allif_data.get("main_sbscrbr_entity")).first()
        catid=selectedcategoryid.id
        allifquery=CommonChartofAccountsModel.all_objects.filter(category=catid,company=allif_data.get("main_sbscrbr_entity"))#this is a queryset that will be sent to the backend.
        allifqueryrelatedlist=list(CommonChartofAccountsModel.all_objects.filter(category=catid,company=allif_data.get("main_sbscrbr_entity")))#this is a list
        serialized_data = serialize("json", allifqueryrelatedlist)
        myjsondata= json.loads(serialized_data)
        allifqueryset=list(CommonChartofAccountsModel.all_objects.filter(category=catid,company=allif_data.get("main_sbscrbr_entity")).values("category","description","id","code","balance"))
        allifrelatedserlized= json.loads(serialize('json', allifquery))#this is a list
        mystringjsondata=json.dumps(allifrelatedserlized)#this is string
        return JsonResponse(allifqueryset,safe=False)
    else:
        allifqueryset=[]
   
@allif_base_view_wrapper
def commonClearAcc(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    acc=CommonChartofAccountsModel.all_objects.filter(id=pk).first()
    acc.balance=0
    acc.save()
    return redirect('allifmaalcommonapp:commonChartofAccounts',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
   


############################################# BANKS ##############################3
@allif_base_view_wrapper
def commonBanks(request,*allifargs,**allifkwargs):
    title="Banks"
    allif_data=common_shared_data(request)
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonBanksModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,}
    return render(request,'allifmaalcommonapp/banks/banks.html',context)

@allif_base_view_wrapper
def commonAddBank(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddBankForm,"Add Bank","commonBanks",'allifmaalcommonapp/banks/add-bank.html')

@allif_base_view_wrapper
def commonEditBank(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddBankForm,"Edit Bank","commonBanks",'allifmaalcommonapp/banks/add-bank.html')

@allif_base_view_wrapper
def commonWantToDeleteBank(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonBanksModel,"Delete this item",'allifmaalcommonapp/banks/delete-bank-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteBank(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonBanksModel',pk=pk,success_redirect_url_name='commonBanks')

@allif_base_view_wrapper
def commonBankSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonBanksModel',search_fields_key='CommonBanksModel',
    template_path='allifmaalcommonapp/banks/banks.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonBankDetails(request, pk, *allifargs, **allifkwargs):
    allif_data=common_shared_data(request)
    allifquery=CommonBanksModel.all_objects.filter(id=pk).first()
    allifqueryset=CommonBankWithdrawalsModel.objects.filter(bank=allifquery,company=allif_data.get("main_sbscrbr_entity"))
    deposits=CommonShareholderBankDepositsModel.objects.filter(bank=allifquery)
   
    return allif_common_detail_view(
        request,
        model_class=CommonBanksModel,
        pk=pk,
        template_name='allifmaalcommonapp/banks/bank-details.html', # Create this template
        title_map={'default': 'Bank Details'},
        related_data_configs=[
            {
            'context_key': 'allifqueryset', # This will be available in template
            'related_model': 'CommonBankWithdrawalsModel', # Name of the related model
            'filter_field': 'bank', # Field on CommonInvoiceItemsModel that links to CommonInvoicesModel
            'order_by': ['number'], # Order the items
            #'prefetch_related': ['product'], # If CommonInvoiceItemsModel has a 'product' ForeignKey, prefetch it
            },
            
            {
            'context_key': 'deposits', # This will be available in template 
            'related_model': 'CommonShareholderBankDepositsModel', # Name of the related model
            'filter_field': 'bank', # Field on CommonInvoiceItemsModel that links to CommonInvoicesModel
            'order_by': ['number'], # Order the items
            #'prefetch_related': ['product'], # If CommonInvoiceItemsModel has a 'product' ForeignKey, prefetch it
        }
        ]
    )


    
############################################### BANK DEPOSITS ################################
@allif_base_view_wrapper
def commonBankShareholderDeposits(request,*allifargs,**allifkwargs):
    title="Shareholder Bank Deposits"
    allif_data=common_shared_data(request)
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonShareholderBankDepositsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/banks/deposits/shareholders/deposits-sh.html',context)

@allif_base_view_wrapper
def commonAddBankShareholderDeposit(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonBankDepositAddForm,"Add Deposit","commonBankShareholderDeposits",'allifmaalcommonapp/banks/deposits/shareholders/add-deposit-sh.html')

@allif_base_view_wrapper
def commonEditBankShareholderDeposit(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonBankDepositAddForm,"Edit Deposit","commonBankShareholderDeposits",'allifmaalcommonapp/banks/deposits/shareholders/add-deposit-sh.html')

@allif_base_view_wrapper
def commonWantToDeleteDeposit(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonShareholderBankDepositsModel,"Delete this item",'allifmaalcommonapp/banks/deposits/shareholders/delete-deposit-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteBankShareholderDeposit(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonShareholderBankDepositsModel',pk=pk,success_redirect_url_name='commonBankShareholderDeposits')

@allif_base_view_wrapper
def commonDepositSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonShareholderBankDepositsModel',search_fields_key='CommonShareholderBankDepositsModel',
    template_path='allifmaalcommonapp/banks/deposits/shareholders/deposits-sh.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonDepositAdvanceSearch(request,*allifargs,**allifkwargs):
    # This view now simply calls the centralized advanced search handler
    return allif_advance_search_handler(request,model_name='CommonShareholderBankDepositsModel',advanced_search_config_key='CommonShareholderBankDepositsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/banks/deposits/shareholders/deposits-sh.html', # Template for HTML results
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html', # <-- CRITICAL: Pass the PDF template path
        #accounts/coa-search-pdf.html
    )
    
@allif_base_view_wrapper      
def commonPostShareholderDeposit(request,pk,*allifargs,**allifkwargs):
   
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
      

############################################### BANK WITHDRAWALS ################################

@allif_base_view_wrapper
def commonBankWithdrawals(request,*allifargs,**allifkwargs):
    title="Money Withdrawals"
    allif_data=common_shared_data(request)
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonBankWithdrawalsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/banks/withdrawals/withdrawals.html',context)

@allif_base_view_wrapper
def commonAddBankWithdrawal(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonBankWithdrawalsAddForm,"New Withdrawal","commonBankWithdrawals",'allifmaalcommonapp/banks/withdrawals/add-withdrawal.html')

@allif_base_view_wrapper
def commonEditBankWithdrawal(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonBankWithdrawalsAddForm,"Edit withdrawal","commonBankWithdrawals",'allifmaalcommonapp/banks/withdrawals/add-withdrawal.html')

@allif_base_view_wrapper
def commonWantToDeleteWithdrawal(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonBankWithdrawalsModel,"Delete this item",'allifmaalcommonapp/banks/withdrawals/delete-withdrawal-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteBankWithdrawal(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonBankWithdrawalsModel',pk=pk,success_redirect_url_name='commonBankWithdrawals')

@allif_base_view_wrapper
def commonWithdrawalSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonBankWithdrawalsModel',search_fields_key='CommonBankWithdrawalsModel',
    template_path='allifmaalcommonapp/banks/withdrawals/withdrawals.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonWithdrawalAdvanceSearch(request,*allifargs,**allifkwargs):
    # This view now simply calls the centralized advanced search handler
    return allif_advance_search_handler(request,model_name='CommonBankWithdrawalsModel',advanced_search_config_key='CommonBankWithdrawalsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/banks/withdrawals/withdrawals.html', # Template for HTML results
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html', # <-- CRITICAL: Pass the PDF template path
        #accounts/coa-search-pdf.html
    )

       
##############################33 suppliers section ###############3
@allif_base_view_wrapper
def commonSuppliers(request,*allifargs,**allifkwargs):
    title="Suppliers"
    allif_data=common_shared_data(request)
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonSuppliersModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/suppliers/suppliers.html',context)

@allif_base_view_wrapper
def commonAddSupplier(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddSupplierForm,"New Supplier","commonSuppliers",'allifmaalcommonapp/suppliers/add-supplier.html')

@allif_base_view_wrapper
def commonEditSupplier(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddSupplierForm,"Edit Supplier","commonSuppliers",'allifmaalcommonapp/suppliers/add-supplier.html')
@allif_base_view_wrapper
def commonSupplierDetails(request, pk, *allifargs, **allifkwargs):
    allif_data=common_shared_data(request)
    allifquery=CommonSuppliersModel.all_objects.filter(id=pk).first()
    return allif_common_detail_view(
        request,
        model_class=CommonSuppliersModel,
        pk=pk,
        template_name='allifmaalcommonapp/suppliers/supplier-details.html', # Create this template
        title_map={'default': 'Supplier Details'},
       
    )

@allif_base_view_wrapper
def commonWantToDeleteSupplier(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonSuppliersModel,"Delete this item",'allifmaalcommonapp/suppliers/delete-supplier-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteSupplier(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonSuppliersModel',pk=pk,success_redirect_url_name='commonSuppliers')

@allif_base_view_wrapper
def commonSupplierSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonSuppliersModel',search_fields_key='CommonSuppliersModel',
    template_path='allifmaalcommonapp/suppliers/suppliers.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonSupplierAdvanceSearch(request,*allifargs,**allifkwargs):
    # This view now simply calls the centralized advanced search handler
    return allif_advance_search_handler(request,model_name='CommonSuppliersModel',advanced_search_config_key='CommonSuppliersModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/suppliers/suppliers.html', # Template for HTML results
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html', # <-- CRITICAL: Pass the PDF template path
        #accounts/coa-search-pdf.html
    )

    
############################################ CUSTOMERS ######################
@allif_base_view_wrapper
def commonCustomers(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title=""
    sector=str(allif_data.get("main_sbscrbr_entity").sector)
    if sector == "Healthcare":
        title="Registered Patients"
    elif sector=="Education":
        title="Registered Students"
    else:
        title="Registered Customers"
    
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonCustomersModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/customers/customers.html',context)

@allif_base_view_wrapper
def commonAddCustomer(request, *allifargs, **allifkwargs):
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
    return allif_common_form_submission_and_save(request,CommonCustomerAddForm,"New Customer","commonCustomers",'allifmaalcommonapp/customers/add-customer.html')

@allif_base_view_wrapper
def commonEditCustomer(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonCustomerAddForm,"Edit Customer","commonCustomers",'allifmaalcommonapp/customers/add-customer.html')
@allif_base_view_wrapper
def commonCustomerDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=CommonCustomersModel,pk=pk,
        template_name='allifmaalcommonapp/customers/customer-details.html', # Create this template
        title_map={'default': 'Customer Details'},)

@allif_base_view_wrapper
def commonWantToDeleteCustomer(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonCustomersModel,"Delete this item",'allifmaalcommonapp/customers/cust-delete-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteCustomer(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonCustomersModel',pk=pk,success_redirect_url_name='commonCustomers')

@allif_base_view_wrapper
def commonCustomerSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonCustomersModel',search_fields_key='CommonCustomersModel',
    template_path='allifmaalcommonapp/customers/customers.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonCustomerAdvanceSearch(request,*allifargs,**allifkwargs):
    # This view now simply calls the centralized advanced search handler
    return allif_advance_search_handler(request,model_name='CommonCustomersModel',advanced_search_config_key='CommonCustomersModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/customers/customers.html', # Template for HTML results
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html', # <-- CRITICAL: Pass the PDF template path
        #accounts/coa-search-pdf.html
    )


    ############################ ASSETS ##########################3
@allif_base_view_wrapper
def commonAssets(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Assets"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonAssetsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/assets/assets.html',context)

@allif_base_view_wrapper
def commonAddAsset(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAssetsAddForm,"New Asset","commonAssets",'allifmaalcommonapp/assets/add-asset.html')

@allif_base_view_wrapper
def commonEditAsset(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAssetsAddForm,"Edit Asset","commonAssets",'allifmaalcommonapp/assets/add-asset.html')
@allif_base_view_wrapper
def commonAssetDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=CommonAssetsModel,pk=pk,
        template_name='allifmaalcommonapp/assets/asset-details.html', # Create this template
        title_map={'default': 'Asset Details'},)

@allif_base_view_wrapper
def commonWantToDeleteAsset(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonAssetsModel,"Delete this item",'allifmaalcommonapp/assets/asset-delete-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteAsset(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonAssetsModel',pk=pk,success_redirect_url_name='commonAssets')

@allif_base_view_wrapper
def commonAssetSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonAssetsModel',search_fields_key='CommonAssetsModel',
    template_path='allifmaalcommonapp/assets/assets.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonAssetAdvanceSearch(request,*allifargs,**allifkwargs):
    # This view now simply calls the centralized advanced search handler
    return allif_advance_search_handler(request,model_name='CommonAssetsModel',advanced_search_config_key='CommonAssetsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/assets/assets.html', # Template for HTML results
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html', # <-- CRITICAL: Pass the PDF template path
        #accounts/coa-search-pdf.html
    )

@allif_base_view_wrapper
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
  


############################3 ASSET DEPRECIATIONS #############3

@allif_base_view_wrapper
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

@allif_base_view_wrapper
def commonExpenses(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Expenses"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonExpensesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/expenses/expenses.html',context)

@allif_base_view_wrapper
def commonAddExpense(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonExpensesAddForm,"New Expense","commonExpenses",'allifmaalcommonapp/expenses/add-expense.html')

@allif_base_view_wrapper
def commonEditExpense(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonExpensesAddForm,"Edit Asset","commonExpenses",'allifmaalcommonapp/expenses/add-expense.html')
@allif_base_view_wrapper
def commonExpenseDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=CommonExpensesModel,pk=pk,
        template_name='allifmaalcommonapp/expenses/expense-details.html', # Create this template
        title_map={'default': 'Expense Details'},)

@allif_base_view_wrapper
def commonWantToDeleteExpense(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonExpensesModel,"Delete this item",'allifmaalcommonapp/expenses/delete-exp-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteExpense(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonExpensesModel',pk=pk,success_redirect_url_name='commonExpenses')

@allif_base_view_wrapper
def commonExpenseSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonExpensesModel',search_fields_key='CommonExpensesModel',
    template_path='allifmaalcommonapp/expenses/expenses.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonExpenseAdvancedSearch(request,*allifargs,**allifkwargs):
    # This view now simply calls the centralized advanced search handler
    return allif_advance_search_handler(request,model_name='CommonExpensesModel',advanced_search_config_key='CommonExpensesModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/expenses/expenses.html', # Template for HTML results
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html', # <-- CRITICAL: Pass the PDF template path
        #accounts/coa-search-pdf.html
    )
@allif_base_view_wrapper
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
@allif_base_view_wrapper
def commonTransactions(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Transactions"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonTransactionsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/transactions/transactions.html',context)

@allif_base_view_wrapper
def commonAddTransactionDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddTransactionDetailsForm,"Edit Transaction","commonTransactions",
    'allifmaalcommonapp/transactions/add-transaction-details.html')

@allif_base_view_wrapper
def commonWantToDeleteTransaction(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonTransactionsModel,"Delete this item",
    'allifmaalcommonapp/transactions/delete_trans_confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteTransaction(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonTransactionsModel',pk=pk,success_redirect_url_name='commonTransactions')

@allif_base_view_wrapper
def commonTransactionsSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonTransactionsModel',search_fields_key='CommonTransactionsModel',
    template_path='allifmaalcommonapp/transactions/transactions.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonTransactionAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='CommonTransactionsModel',advanced_search_config_key='CommonTransactionsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/transactions/transactions.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def commonNewTransaction(request,*allifargs,**allifkwargs):
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

    number=CommonTransactionsModel.objects.create(number=nmbr,company=allif_data.get("main_sbscrbr_entity"),owner=allif_data.get("usernmeslg"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
    number.save()
    return redirect('allifmaalcommonapp:commonTransactions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

@allif_base_view_wrapper
def commonTransactionDetails(request, pk, *allifargs, **allifkwargs):
    allif_data=common_shared_data(request)
    #parent_transaction = get_object_or_404(CommonTransactionsModel, id=pk) 
    allifquery=CommonTransactionsModel.all_objects.filter(id=pk).first()
    allifqueryset = CommonTransactionItemsModel.objects.filter(trans_number=allifquery)
    return allif_common_detail_view(request,model_class=CommonTransactionsModel,pk=pk,
        template_name='allifmaalcommonapp/transactions/transaction_details.html', # Create this template
        title_map={'default': 'Transaction Details'},
        related_data_configs=[
            {
            'context_key': 'allifqueryset', # This will be available in template
            'related_model': 'CommonTransactionItemsModel', # Name of the related model
            'filter_field': 'trans_number', # Field on CommonInvoiceItemsModel that links to CommonInvoicesModel
            'order_by': ['number'], # Order the items
            },
            ]
        )

@allif_base_view_wrapper
def commonTransactionToPdf(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    date_today=date.today()
    
    scopes=CommonCompanyScopeModel.all_objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
    allifquery=CommonTransactionsModel.all_objects.filter(id=pk).first()
    allifqueryset=CommonTransactionItemsModel.all_objects.filter(trans_number=allifquery)
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
  
##########################3 transaction items.. #############
@allif_base_view_wrapper
def commonAddTransactionItems(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery= get_object_or_404(CommonTransactionsModel, id=pk) 
    allifquery=CommonTransactionsModel.all_objects.filter(id=pk).first()
    allifqueryset = CommonTransactionItemsModel.objects.filter(trans_number=allifquery)
    def transaction_item_pre_save(obj, request, allif_data):
        obj.trans_number = allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset,"myid": pk,}
    return allif_common_form_submission_and_save(request,form_class=CommonAddTransactionItemForm,
        title_text="Add Transaction Items",
        success_redirect_url_name='commonAddTransactionItems', # This URL expects a PK
        template_path='allifmaalcommonapp/transactions/add_trans_items.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)
    
@allif_base_view_wrapper
def commonEditTransactionItem(request,pk,*allifargs,**allifkwargs):
   
    """
    this function was not refactored...
    """
    title="Edit Item Details"
    allif_data=common_shared_data(request)
    myquery=CommonTransactionItemsModel.all_objects.filter(id=pk).first()
    allifquery=myquery.trans_number
    allifqueryset=CommonTransactionItemsModel.all_objects.filter(trans_number=allifquery)

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
        
@allif_base_view_wrapper
def commonDeleteTransactionItem(request,pk,*allifargs,**allifkwargs):
    """
    this was not refactored as well....
    """
    title="Delete Transaction Items"
    allif_data=common_shared_data(request)
    
    myallifquery=CommonTransactionItemsModel.objects.filter(id=pk).first()
    myquery=myallifquery.trans_number
    myallifquery.delete()
    return redirect('allifmaalcommonapp:commonAddTransactionItems',pk=myquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
##############3 Spaces################
@allif_base_view_wrapper
def commonSpaces(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Spaces"
   
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonSpacesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/spaces/spaces.html',context)

@allif_base_view_wrapper
def commonAddSpace(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddSpaceForm,"New Space","commonSpaces",'allifmaalcommonapp/spaces/add-space.html')

@allif_base_view_wrapper
def commonEditSpace(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddSpaceForm,"Edit Space","commonSpaces",'allifmaalcommonapp/spaces/add-space.html')
@allif_base_view_wrapper
def commonSpaceDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=CommonSpacesModel,pk=pk,
        template_name='allifmaalcommonapp/spaces/space-details.html', # Create this template
        title_map={'default': 'Space Details'},
        
        related_data_configs=[
            {
            'context_key': 'allifqueryset', # This will be available in template
            'related_model': 'CommonSpaceUnitsModel', # Name of the related model
            'filter_field': 'space', # Field on CommonInvoiceItemsModel that links to CommonInvoicesModel
            'order_by': ['number'], # Order the items
            },
            ]
        
        )

@allif_base_view_wrapper
def commonWantToDeleteSpace(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonSpacesModel,"Delete this item",'allifmaalcommonapp/spaces/delete-space-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteSpace(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonSpacesModel',pk=pk,success_redirect_url_name='commonSpaces')


################################ SPACE UNITS....####################
@allif_base_view_wrapper
def commonSpaceUnits(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Space Units"
   
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonSpaceUnitsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/spaces/units/space_units.html',context)

@allif_base_view_wrapper
def commonAddSpaceUnit(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddSpaceUnitForm,"Add Space Unit",
    "commonSpaceUnits",'allifmaalcommonapp/spaces/units/add_space_unit.html')

@allif_base_view_wrapper
def commonEditSpaceUnit(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddSpaceUnitForm,"Edit Space Unit",
                                           "commonSpaceUnits",'allifmaalcommonapp/spaces/units/add_space_unit.html')
@allif_base_view_wrapper
def commonSpaceUnitDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=CommonSpaceUnitsModel,pk=pk,
        template_name='allifmaalcommonapp/spaces/units/space_unit_details.html', # Create this template
        title_map={'default': 'Space Unit Details'},
      
        )

@allif_base_view_wrapper
def commonWantToDeleteSpaceUnit(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonSpaceUnitsModel,"Delete this item",
                                'allifmaalcommonapp/spaces/units/delete_space_unit_confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteSpaceUnit(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonSpaceUnitsModel',pk=pk,success_redirect_url_name='commonSpaceUnits')


@allif_base_view_wrapper
def commonSpaceUnitSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonSpaceUnitsModel',search_fields_key='CommonSpaceUnitsModel',
    template_path='allifmaalcommonapp/spaces/units/space_units.html',search_input_name='allifsearchcommonfieldname',)


######################## space booking items... #####################3
@allif_base_view_wrapper
def commonSpaceBookings(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    allifquery=CommonTransactionsModel.objects.filter(id=pk).first()
    title=str(allifquery) +" - "+ "Space Alloctions"
    allifqueryset=CommonSpaceBookingItemsModel.objects.filter(trans_number=allifquery)#this line helps to
   
    context={"allifquery":allifquery,"allifqueryset":allifqueryset,"title":title,}
    return render(request,'allifmaalcommonapp/booking/space_bookings.html',context)

@allif_base_view_wrapper
def commonAddSpaceBookingItems(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery= get_object_or_404(CommonTransactionsModel, id=pk)
    allifquery=CommonTransactionsModel.all_objects.filter(id=pk).first()
    allifqueryset = CommonSpaceBookingItemsModel.objects.filter(trans_number=allifquery)
    initial_amount=0
    for items in allifqueryset:
        initial_amount+=items.space_allocation_amount
    allifquery.amount=initial_amount
    allifquery.save()
    
    def transaction_item_pre_save(obj, request, allif_data):
        obj.trans_number = allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset,"myid": pk,}
    return allif_common_form_submission_and_save(request,form_class=CommonAddSpaceBookingItemForm,
        title_text="Add Space Allocations",
        success_redirect_url_name='commonAddSpaceBookingItems', # This URL expects a PK
        template_path='allifmaalcommonapp/booking/add_space_booking.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)

@allif_base_view_wrapper
def commonEditSpaceBookingItem(request,pk,*allifargs,**allifkwargs):
    title="Edit Item Details"
    allif_data=common_shared_data(request)
    myquery_update=CommonSpaceBookingItemsModel.all_objects.filter(id=pk).first()
    allifquery=myquery_update.trans_number
    allifqueryset=CommonSpaceBookingItemsModel.all_objects.filter(trans_number=allifquery)

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


@allif_base_view_wrapper
def commonSpaceAllocationPdf(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    date_today=date.today()
    
    scopes=CommonCompanyScopeModel.all_objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
    allifquery=CommonTransactionsModel.all_objects.filter(id=pk).first()
    allifqueryset=CommonSpaceBookingItemsModel.all_objects.filter(trans_number=allifquery)
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
@allif_base_view_wrapper
def commonDeleteSpaceBookingItem(request,pk,*allifargs,**allifkwargs):
    title="Delete Transaction Items"
    allif_data=common_shared_data(request)
    myallifquery=CommonSpaceBookingItemsModel.all_objects.filter(id=pk).first()
    myquery=myallifquery.trans_number
    myallifquery.delete()
    return redirect('allifmaalcommonapp:commonAddSpaceBookingItems',pk=myquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))


    
################### inventory/stock###########3
@allif_base_view_wrapper
def commonStocks(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Stock and Inventory"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonStocksModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/stocks/stocks.html',context)


@allif_base_view_wrapper
def commonAddStockItem(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonStockItemAddForm,"Add Stock Item",
    "commonStocks",'allifmaalcommonapp/stocks/add-stock.html')

@allif_base_view_wrapper
def commonEditStockItem(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonStockItemAddForm,"Edit Item",
    "commonStocks",'allifmaalcommonapp/stocks/add-stock.html')
    
@allif_base_view_wrapper
def commonWantToDeleteStockItem(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonStocksModel,"Delete this item",
    'allifmaalcommonapp/stocks/x-stock-item-cnfrm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteStockItem(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonStocksModel',pk=pk,success_redirect_url_name='commonTransactions')

@allif_base_view_wrapper
def commonStockItemSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonStocksModel',search_fields_key='CommonStocksModel',
    template_path='allifmaalcommonapp/stocks/stocks.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonStockItemAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='CommonStocksModel',advanced_search_config_key='CommonStocksModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/stocks/stocks.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def commonStockItemDetails(request, pk, *allifargs, **allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery = get_object_or_404(CommonStocksModel, id=pk) 
    allifquery=CommonStocksModel.all_objects.filter(id=pk).first()
    return allif_common_detail_view(request,model_class=CommonStocksModel,pk=pk,
        template_name='allifmaalcommonapp/stocks/stock-details.html', # Create this template
        title_map={'default': 'Stock Details'},)



############################# STOCK PURCHASE ORDERS #####################################
@allif_base_view_wrapper
def commonPurchaseOrders(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Purchase Orders"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonPurchaseOrdersModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/purchases/purchaseorders.html',context)

@allif_base_view_wrapper
def commonAddPODetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonPOAddForm,"Add PO Details",
    'commonAddPODetails','allifmaalcommonapp/purchases/add-po-details.html',
    redirect_with_pk=True,redirect_pk_value=pk,)

@allif_base_view_wrapper
def commonWantToDeletePO(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonPurchaseOrdersModel,"Delete this item",
    'allifmaalcommonapp/purchases/x-po-cnfrm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeletePO(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonPurchaseOrdersModel',pk=pk,success_redirect_url_name='commonPurchaseOrders')

@allif_base_view_wrapper
def commonPOSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonPurchaseOrdersModel',search_fields_key='CommonPurchaseOrdersModel',
    template_path='allifmaalcommonapp/purchases/purchaseorders.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonPOAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='CommonPurchaseOrdersModel',advanced_search_config_key='CommonPurchaseOrdersModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/purchases/purchaseorders.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')


@allif_base_view_wrapper
def commonNewPurchaseOrder(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    ###### start... UID generation ##################
    allifquery=CommonPurchaseOrdersModel.all_objects.filter(company=allif_data.get("main_sbscrbr_entity"))
    unque=str(uuid4()).split('-')[2]
    nmbr=int(allifquery.count())+int(1)
    currntyear=timezone.now().date().today().year
    allifuid=str(nmbr)+"/"+str(currntyear)+"/"+str(unque)
    ###### End... UID generation ##################print()
    
    if allifquery:
        purchaseNumber='PO'+"/"+str(allifuid)
    else:
        purchaseNumber= 'PO/1'+"/"+str(currntyear)+"/"+str(uuid4()).split('-')[2]

    newPurchaseOrder= CommonPurchaseOrdersModel.all_objects.create(number=purchaseNumber,company=allif_data.get("main_sbscrbr_entity"),owner=allif_data.get("usernmeslg"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
    newPurchaseOrder.save()
    return redirect('allifmaalcommonapp:commonPurchaseOrders',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))


@allif_base_view_wrapper
def common_purchase_order_pdf(request, pk, *allifargs, **allifkwargs):
    return allif_document_pdf_handler(request,pk=pk,document_config_key='CommonPurchaseOrdersModel',)
  

@allif_base_view_wrapper
def commonPOMiscCost(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery= get_object_or_404(CommonPurchaseOrdersModel, id=pk)
    allifquery=CommonPurchaseOrdersModel.all_objects.filter(id=pk).first()
    allifqueryset = CommonPurchaseOrderMiscCostsModel.all_objects.filter(po_misc_cost_con=allifquery)
    queryset=CommonPurchaseOrderItemsModel.all_objects.filter(po_item_con=allifquery)
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
        
    def transaction_item_pre_save(obj, request, allif_data):
        obj.po_misc_cost_con = allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset,"myid": pk,}
    return allif_common_form_submission_and_save(request,form_class=CommonPOMiscCostAddForm,
        title_text="Add Transaction Items",
        success_redirect_url_name='commonPOMiscCost', # This URL expects a PK
        template_path='allifmaalcommonapp/purchases/add-po-misc-costs.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)
    
@allif_base_view_wrapper    
def commonCalculatePOMiscCosts(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    allifquery=CommonPurchaseOrdersModel.all_objects.filter(id=pk).first() #very important to get id to go to particular shipment
    allifqueryset=CommonPurchaseOrderItemsModel.all_objects.filter(po_item_con=allifquery)
    queryset= CommonPurchaseOrderMiscCostsModel.all_objects.filter(po_misc_cost_con=allifquery)#this line helps to
    
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


@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteMiscCost(request,pk,*allifargs,**allifkwargs):
    #query=get_object_or_404(CommonPurchaseOrderMiscCostsModel, id=pk)
    query=CommonPurchaseOrderMiscCostsModel.all_objects.filter(id=pk).first()
    allifquery=query.po_misc_cost_con.id
    return allif_delete_hanlder(request,model_name='CommonPurchaseOrderMiscCostsModel',
    pk=pk,success_redirect_url_name='commonPOMiscCost',redirect_with_pk=True,redirect_pk_value=allifquery)

@allif_base_view_wrapper
def commonEditPOMiscCostDetails(request,pk,*allifargs,**allifkwargs):
    """
    Not refactored because the edit handler is yet to have presave for specific items like the one below..
    add_item.po_misc_cost_con=allifquery
    """
    
    title="Update Misc. Cost Details"
    allif_data=common_shared_data(request)
    queryobj=CommonPurchaseOrderMiscCostsModel.all_objects.filter(id=pk).first()
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

@allif_base_view_wrapper
def commonPostPO(request,pk,*allifargs,**allifkwargs):
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

###########33 purchaser order items

@allif_base_view_wrapper
def commonAddPOItems(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery= get_object_or_404(CommonPurchaseOrdersModel, id=pk) 
    allifquery=CommonPurchaseOrdersModel.all_objects.filter(id=pk).first()
    allifqueryset =CommonPurchaseOrderItemsModel.objects.filter(po_item_con=allifquery)
    queryset=CommonPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=allifquery)
    
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
    def transaction_item_pre_save(obj, request, allif_data):
        obj.po_item_con=allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset,"queryset": queryset,}
    return allif_common_form_submission_and_save(request,form_class=CommonPOItemAddForm,
        title_text="Add PO Items",
        success_redirect_url_name='commonAddPOItems', # This URL expects a PK
        template_path='allifmaalcommonapp/purchases/add-po-items.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)
 

@allif_base_view_wrapper
def commonEditPOItem(request, pk, *allifargs, **allifkwargs):
    
    #query=get_object_or_404(CommonPurchaseOrderItemsModel, id=pk) 
    query=CommonPurchaseOrderItemsModel.all_objects.filter(id=pk).first()
    allifquery=query.po_item_con.id
    return allif_common_form_edit_and_save(request,pk,CommonPOItemAddForm,"Edit PO Item Details",
    'commonAddPOItems','allifmaalcommonapp/purchases/add-po-items.html',
    redirect_with_pk=True,redirect_pk_value=allifquery,)


@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeletePOItem(request,pk,*allifargs,**allifkwargs):
    #query=get_object_or_404(CommonPurchaseOrderItemsModel, id=pk)
    query=CommonPurchaseOrderItemsModel.all_objects.filter(id=pk).first()
    allifquery=query.po_item_con.id
    return allif_delete_hanlder(request,model_name='CommonPurchaseOrderItemsModel',
    pk=pk,success_redirect_url_name='commonAddPOItems',redirect_with_pk=True,redirect_pk_value=allifquery)
    

############################## TRANSFER ORDERS #######################
@allif_base_view_wrapper
def commonTransferOrders(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Stock Transfer Orders"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonStockTransferOrdersModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/stocks/transfers/transfer-orders.html',context)

@allif_base_view_wrapper
def commonAddTransferOrderDetails(request, pk, *allifargs, **allifkwargs):
    #allifquery= get_object_or_404(CommonStockTransferOrdersModel, id=pk) 
    allifquery=CommonStockTransferOrdersModel.all_objects.filter(id=pk).first()
    allifqueryset=CommonStockTransferOrderItemsModel.objects.filter(trans_ord_items_con=allifquery)
        
    return allif_common_form_edit_and_save(request,pk,CommonAddTransferOrderDetailsForm,"Add Transfer Order Details",
    'commonAddTransferOrderDetails','allifmaalcommonapp/stocks/transfers/add-transfer-order-details.html',
    redirect_with_pk=True,redirect_pk_value=pk,)

@allif_base_view_wrapper
def commonWantToDeleteTransferOrder(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonStockTransferOrdersModel,"Delete this item",
    'allifmaalcommonapp/stocks/Transfers/delete-transfer-order-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteTransferOrder(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonStockTransferOrdersModel',pk=pk,success_redirect_url_name='commonTransferOrders')

@allif_base_view_wrapper
def commonTransferOrdersSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonStockTransferOrdersModel',search_fields_key='CommonStockTransferOrdersModel',
    template_path='allifmaalcommonapp/stocks/transfers/transfer-orders.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonTRFAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='CommonStockTransferOrdersModel',advanced_search_config_key='CommonStockTransferOrdersModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/stocks/transfers/transfer-orders.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')


@allif_base_view_wrapper
def commonTransferOrderPdf(request, pk, *allifargs, **allifkwargs):
    return allif_document_pdf_handler(request,pk=pk,document_config_key='CommonStockTransferOrdersModel',)
  

@allif_base_view_wrapper
def commonAddTransferOrderItems(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery= get_object_or_404(CommonStockTransferOrdersModel, id=pk) 
    allifquery=CommonStockTransferOrdersModel.all_objects.filter(id=pk).first()
    allifqueryset=CommonStockTransferOrderItemsModel.objects.filter(trans_ord_items_con=allifquery)
  
    def transaction_item_pre_save(obj, request, allif_data):
        obj.trans_ord_items_con=allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset}
    return allif_common_form_submission_and_save(request,form_class=CommonAddTransferOrderItemForm,
        title_text="Add TRF Items",
        success_redirect_url_name='commonAddTransferOrderItems', # This URL expects a PK
        template_path='allifmaalcommonapp/stocks/transfers/add-transfer-order-item.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)
 

@allif_base_view_wrapper
def commonEditTransferOrderItem(request, pk, *allifargs, **allifkwargs):
    """
    this function needs to be improved... when items are edited, they lose connection to TRF and therefore,
    the edit handler needs to be added special pre-save function like its add counterpart to handle such instances...
    
    """
    
    #query=get_object_or_404(CommonStockTransferOrderItemsModel, id=pk) 
    query=CommonStockTransferOrderItemsModel.all_objects.filter(id=pk).first()
    allifquery=query.trans_ord_items_con.id
    return allif_common_form_edit_and_save(request,pk,CommonAddTransferOrderItemForm,"Edit TRF Item Details",
    'commonAddTransferOrderItems','allifmaalcommonapp/stocks/transfers/add-transfer-order-item.html',
    redirect_with_pk=True,redirect_pk_value=allifquery,)


@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteTransferOrderItem(request,pk,*allifargs,**allifkwargs):
    #query=get_object_or_404(CommonStockTransferOrderItemsModel, id=pk)
    query=CommonStockTransferOrderItemsModel.all_objects.filter(id=pk).first()
    allifquery=query.trans_ord_items_con.id
    return allif_delete_hanlder(request,model_name='CommonStockTransferOrderItemsModel',
    pk=pk,success_redirect_url_name='commonAddTransferOrderItems',redirect_with_pk=True,redirect_pk_value=allifquery)
    

@allif_base_view_wrapper   
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
    
@allif_base_view_wrapper
def commonEditTransferOrderItem(request,pk,*allifargs,**allifkwargs):
    """
    remove this function and its similar name function is already up there after imporving on edit handler..
    """
  
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
            obj.trans_ord_items_con=allifquery
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
 
@allif_base_view_wrapper
def commonPostTransferOrder(request, pk, *allifargs, **allifkwargs):
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
    
######################### QUOTATION #########################
@allif_base_view_wrapper
def commonQuotes(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Quotations"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonQuotesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/quotes/quotes.html',context)

@allif_base_view_wrapper
def commonAddQuoteDetails(request, pk, *allifargs, **allifkwargs):
    #allifquery= get_object_or_404(CommonQuotesModel, id=pk) 
    allifquery=CommonQuotesModel.all_objects.filter(id=pk).first()
    return allif_common_form_edit_and_save(request,pk,CommonAddQuoteDetailsForm,"Add Quote Details",
    'commonAddQuoteDetails','allifmaalcommonapp/quotes/add-quote-details.html',
    redirect_with_pk=True,redirect_pk_value=pk,)

@allif_base_view_wrapper
def commonWantToDeleteQuote(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonQuotesModel,"Delete this item",
    'allifmaalcommonapp/quotes/x-qt-confrm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteQuote(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonQuotesModel',pk=pk,success_redirect_url_name='commonQuotes')

@allif_base_view_wrapper
def commonQuotesSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonQuotesModel',search_fields_key='CommonQuotesModel',
    template_path='allifmaalcommonapp/quotes/quotes.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonQuoteAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='CommonQuotesModel',advanced_search_config_key='CommonQuotesModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/quotes/quotes.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')


@allif_base_view_wrapper
def commonQuoteToPdf(request, pk, *allifargs, **allifkwargs):
    return allif_document_pdf_handler(request,pk=pk,document_config_key='CommonQuotesModel',)
  

@allif_base_view_wrapper
def commonAddQuoteItems(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery= get_object_or_404(CommonQuotesModel, id=pk) 
    allifquery=CommonQuotesModel.all_objects.filter(id=pk).first()
    allifqueryset=CommonQuoteItemsModel.objects.filter(allifquoteitemconnector=allifquery)
    allif_qte_discount=allifquery.discount
    
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
  
    def transaction_item_pre_save(obj, request, allif_data):
        obj.allifquoteitemconnector=allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset}
    return allif_common_form_submission_and_save(request,form_class=CommonAddQuoteItemsForm,
        title_text="Add Quote Items",
        success_redirect_url_name='commonAddQuoteItems', # This URL expects a PK
        template_path='allifmaalcommonapp/quotes/add-quote-items.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)
 
@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteQuoteItem(request,pk,*allifargs,**allifkwargs):
    #query=get_object_or_404(CommonQuoteItemsModel, id=pk)
    query=CommonQuoteItemsModel.all_objects.filter(id=pk).first()
    allifquery=query.allifquoteitemconnector.id
    return allif_delete_hanlder(request,model_name='CommonQuoteItemsModel',
    pk=pk,success_redirect_url_name='commonAddQuoteItems',redirect_with_pk=True,redirect_pk_value=allifquery)
    
@allif_base_view_wrapper
def commonNewQuote(request,*allifargs,**allifkwargs):
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

@allif_base_view_wrapper
def commonEditQuoteItem(request,pk,*allifargs,**allifkwargs):
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

########################### END OF QUOTATION ###############


##########################3 INVOICES #######################333
@allif_base_view_wrapper
def commonInvoices(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Invoices"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonInvoicesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/invoices/invoices.html',context)

@allif_base_view_wrapper
def commonAddInvoiceDetails(request, pk, *allifargs, **allifkwargs):
    #allifquery= get_object_or_404(CommonInvoicesModel, id=pk) 
    allifquery=CommonInvoicesModel.all_objects.filter(id=pk).first()
    return allif_common_form_edit_and_save(request,pk,CommonAddInvoiceDetailsForm,"Add Invoice Details",
    'commonAddInvoiceDetails','allifmaalcommonapp/invoices/add-invoice-details.html',
    redirect_with_pk=True,redirect_pk_value=pk,)

@allif_base_view_wrapper
def commonWantToDeleteInvoice(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonInvoicesModel,"Delete this item",
    'allifmaalcommonapp/invoices/x-inv-confrm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteInvoice(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonInvoicesModel',pk=pk,success_redirect_url_name='commonInvoices')


@allif_base_view_wrapper
def commonNewInvoice(request,*allifargs,**allifkwargs):
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


@allif_base_view_wrapper
def commonAddInvoiceItems(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery= get_object_or_404(CommonInvoicesModel, id=pk) 
    allifquery=CommonInvoicesModel.all_objects.filter(id=pk).first()
    allifqueryset=CommonInvoiceItemsModel.objects.filter(allifinvitemconnector=allifquery)
    allif_qte_discount=allifquery.discount
    
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
            invitemscost+=line.items.unitcost
            


    allifquery.total=allifquerysettotal
    allifquery.taxAmount=invoice_line_tax
    allifquery.discountAmount=discounttoal
    allifquery.totalwithdiscount=allifquerysettotal-discounttoal
    allifquery.grandtotal=Decimal(allifquerysettotal-discounttoal)+Decimal(invoice_line_tax)
    allifquery.invoice_items_total_cost=invitemscost
    allifquery.invoice_gross_profit=Decimal(allifquerysettotal-discounttoal or 0)-Decimal(invitemscost or 0)
    allifquery.save()

  
    def transaction_item_pre_save(obj, request, allif_data):
        obj.allifinvitemconnector=allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset}
    return allif_common_form_submission_and_save(request,form_class=CommonAddInvoiceItemsForm,
        title_text="Add Invoice Items",
        success_redirect_url_name='commonAddInvoiceItems', # This URL expects a PK
        template_path='allifmaalcommonapp/invoices/add-inv-items.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)

@allif_base_view_wrapper
def commonEditInvoiceItem(request,pk,*allifargs,**allifkwargs):
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
 
 
 
@allif_base_view_wrapper
def commonDeleteInvoiceItem(request,pk,*allifargs,**allifkwargs):
    #query=get_object_or_404(CommonInvoiceItemsModel, id=pk)
    query=CommonInvoiceItemsModel.all_objects.filter(id=pk).first()
    allifquery=query.allifinvitemconnector.id
    return allif_delete_hanlder(request,model_name='CommonInvoiceItemsModel',
    pk=pk,success_redirect_url_name='commonAddInvoiceItems',redirect_with_pk=True,redirect_pk_value=allifquery)

@allif_base_view_wrapper
def commonPostInvoice(request,pk,*allifargs,**allifkwargs):
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
            
            mycustomer.turnover=initial_customer_acc_turnover+item.items.unitPrice
            initial_customer_acc_balance=mycustomer.balance or 0
            mycustomer.balance=initial_customer_acc_balance+item.items.unitPrice

            mycustomer.save()
            
            #transaction=AllifmaalCustomerStatementModel.objects.create(customer=customer,debit=inv_total,
                    #comments="Invoice",balance=initial_customer_acc_balance+inv_total)#get the ord
        

            # ......... credit the equity account .........
            equity_acc=CommonChartofAccountsModel.objects.filter(description="Equity",company=allif_data.get("main_sbscrbr_entity"),department=allif_data.get("logged_user_department")).first()
            if equity_acc:
                initial_equity_account_balance=equity_acc.balance
                equity_acc.balance=initial_equity_account_balance + item.items.unitPrice-item.items.unitcost
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

@allif_base_view_wrapper
def commonPostedInvoices(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Posted Invoices"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonInvoicesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/invoices/posted-invoices.html',context)


@allif_base_view_wrapper
def commonInvoicesSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonInvoicesModel',search_fields_key='CommonInvoicesModel',
    template_path='allifmaalcommonapp/invoices/invoices.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonInvoiceAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='CommonInvoicesModel',advanced_search_config_key='CommonInvoicesModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/invoices/invoices.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')


@allif_base_view_wrapper
def commonInvoiceToPdf(request, pk, *allifargs, **allifkwargs):
    return allif_document_pdf_handler(request,pk=pk,document_config_key='CommonInvoicesModel',)
@allif_base_view_wrapper
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

##########################3 credit Notes ######################
@allif_base_view_wrapper
def commonCreditNotes(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Credit Notes"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonCreditNotesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/creditnotes/credit-notes.html',context)

@allif_base_view_wrapper
def commonAddCreditNoteDetails(request, pk, *allifargs, **allifkwargs):
    #allifquery= get_object_or_404(CommonCreditNotesModel, id=pk) 
    allifquery=CommonCreditNotesModel.all_objects.filter(id=pk).first()
    return allif_common_form_edit_and_save(request,pk,CommonAddCreditNoteDetailsForm,"Add CN Details",
    'commonAddCreditNoteDetails','allifmaalcommonapp/creditnotes/add-credit-note-details.html',
    redirect_with_pk=True,redirect_pk_value=pk,)

@allif_base_view_wrapper
def commonWantToDeleteCreditNote(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonCreditNotesModel,"Delete this item",
    'allifmaalcommonapp/creditnotes/delete-credit-note-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteCreditNote(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonCreditNotesModel',pk=pk,success_redirect_url_name='commonCreditNotes')

@allif_base_view_wrapper
def commonNewCreditNote(request,*allifargs,**allifkwargs):
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

@allif_base_view_wrapper
def commonAddCreditNoteItems(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery= get_object_or_404(CommonCreditNotesModel, id=pk) 
    allifquery=CommonCreditNotesModel.all_objects.filter(id=pk).first()
    allifqueryset=CommonCreditNoteItemsModel.objects.filter(credit_note=allifquery)
   
    def transaction_item_pre_save(obj, request, allif_data):
        obj.credit_note=allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset}
    return allif_common_form_submission_and_save(request,form_class=CommonAddCreditNoteItemForm,
        title_text="Add Credit Note Items",
        success_redirect_url_name='commonAddCreditNoteItems', # This URL expects a PK
        template_path='allifmaalcommonapp/creditnotes/add_credit_note_items.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)

@allif_base_view_wrapper
def commonEditCreditNoteItem(request,pk,*allifargs,**allifkwargs):
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


 
@allif_base_view_wrapper
def commonDeleteCreditNoteItem(request,pk,*allifargs,**allifkwargs):
    #query=get_object_or_404(CommonCreditNoteItemsModel, id=pk)
    query=CommonCreditNoteItemsModel.all_objects.filter(id=pk).first()
    allifquery=query.credit_note.id
    return allif_delete_hanlder(request,model_name='CommonCreditNoteItemsModel',
    pk=pk,success_redirect_url_name='commonAddCreditNoteItems',redirect_with_pk=True,redirect_pk_value=allifquery)


@allif_base_view_wrapper   
def commonPostCreditNote(request,pk,*allifargs,**allifkwargs):
  
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
            allifquery.posting_inv_status="posted"
            allifquery.save()

    else:
        messages.warning(request,"Please select a customer")
        return redirect('allifmaalcommonapp:commonAddCreditNoteDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    CommonLedgerEntriesModel.objects.create(customer=customer,credit=amount,
    comments="invoice",company=allif_data.get("main_sbscrbr_entity"),owner=request.user,ledgowner="customer")
    return redirect('allifmaalcommonapp:commonAddCreditNoteDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

@allif_base_view_wrapper
def commonPostedCreditNotes(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Posted Credit Notes"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonCreditNotesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/creditnotes/posted-credit-notes.html',context)

@allif_base_view_wrapper
def commonApproveCreditNote(request,pk,*allifargs,**allifkwargs):
    title="Approve Credit Note"
    allif_data=common_shared_data(request)
    allifquery=CommonCreditNotesModel.all_objects.filter(id=pk,company=allif_data.get("main_sbscrbr_entity")).first()
    allifquery.approval_status='approved'
    allifquery.save()
    return redirect('allifmaalcommonapp:commonAddCreditNoteDetails',pk=allifquery.id,allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

@allif_base_view_wrapper
def commonCreditNotesSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonCreditNotesModel',search_fields_key='CommonCreditNotesModel',
    template_path='allifmaalcommonapp/creditnotes/credit-notes.html',search_input_name='allifsearchcommonfieldname',)

@allif_base_view_wrapper
def commonCreditNotesAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='CommonCreditNotesModel',advanced_search_config_key='CommonCreditNotesModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/creditnotes/credit-notes.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def commonCreditNotePdf(request, pk, *allifargs, **allifkwargs):
    return allif_document_pdf_handler(request,pk=pk,document_config_key='CommonCreditNotesModel',)

################# general ledger entris #############
@allif_base_view_wrapper
def commonLedgerEntries(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Ledger Entries"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonLedgerEntriesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/ledgerentries/ledgerentries.html',context)

@allif_base_view_wrapper
def commonLedgerEntryDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=CommonLedgerEntriesModel,pk=pk,
        template_name='allifmaalcommonapp/ledgerentries/ledger-entry-details.html', # Create this template
        title_map={'default': 'Ledger Entry Details'},)


@allif_base_view_wrapper
def commonWantToDeleteLedgerEntry(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonLedgerEntriesModel,"Delete this item",
    'allifmaalcommonapp/ledgerentries/ledger-entry-delete-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteLedgerEntry(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonLedgerEntriesModel',pk=pk,success_redirect_url_name='commonLedgerEntries')


@allif_base_view_wrapper
def commonLedgerEntrySearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonLedgerEntriesModel',search_fields_key='CommonLedgerEntriesModel',
    template_path='allifmaalcommonapp/ledgerentries/ledgerentries.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonLedgerEntryAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='CommonLedgerEntriesModel',advanced_search_config_key='CommonLedgerEntriesModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/ledgerentries/ledgerentries.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def commonSupplierLedgerEntries(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(
        request,
        model_class=CommonSuppliersModel,
        pk=pk,
        template_name='allifmaalcommonapp/ledgerentries/suppliers/supplier-ledger-entries.html',
        title_map={'default': 'Supplier Ledger Entries'},
        related_data_configs=[
            {
            'context_key': 'allifqueryset',
            'related_model': 'CommonLedgerEntriesModel', 
            'filter_field': 'supplier', 
            'order_by': ['code'],
            }
        ]
    )

@allif_base_view_wrapper
def commonCustomerLedgerEntries(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(
        request,
        model_class=CommonCustomersModel,
        pk=pk,
        template_name='allifmaalcommonapp/ledgerentries/customers/customer-ledger-entries.html',
        title_map={'default': 'Customer Ledger Entries'},
        related_data_configs=[
            {
            'context_key': 'allifqueryset',
            'related_model': 'CommonLedgerEntriesModel', 
            'filter_field': 'customer', 
            'order_by': ['code'],
            }
        ]
    )



@allif_base_view_wrapper
def commonStaffLedgerEntries(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(
        request,
        model_class=CommonEmployeesModel,
        pk=pk,
        template_name='allifmaalcommonapp/ledgerentries/staff/staff-ledger-entries.html',
        title_map={'default': 'Staff Ledger Entries'},
        related_data_configs=[
            {
            'context_key': 'allifqueryset',
            'related_model': 'CommonLedgerEntriesModel', 
            'filter_field': 'staff', 
            'order_by': ['code'],
            }
        ]
    )


##############################3 PAYMENTS #############################
######### supplier payments section ############
@allif_base_view_wrapper
def commonSupplierPayments(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Supplier Payments"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonSupplierPaymentsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payments.html',context)

@allif_base_view_wrapper
def commonSupplierPaymentDetails(request, pk, *allifargs, **allifkwargs):
    #allifquery= get_object_or_404(CommonSupplierPaymentsModel, id=pk) 
    allifquery=CommonSupplierPaymentsModel.all_objects.filter(id=pk).first()
    return allif_common_form_edit_and_save(request,pk,CommonAddSupplierPaymentForm,"Supplier Payment Details",
    'commonSupplierPaymentDetails','allifmaalcommonapp/payments/suppliers/supplier-payment-details.html',
    redirect_with_pk=True,redirect_pk_value=pk,)


def commonPaySupplier(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    
    allifquery=CommonSuppliersModel.all_objects.filter(id=pk).first()
    def transaction_item_pre_save(obj, request, allif_data):
        obj.supplier=allifquery
    my_extra_context={"allifquery":allifquery}
    return allif_common_form_submission_and_save(request,form_class=CommonAddSupplierPaymentForm,
        title_text="Add Supplier Payment",
        success_redirect_url_name='commonSupplierPayments', # This URL expects a PK
        template_path='allifmaalcommonapp/payments/suppliers/pay-supplier.html',
        pre_save_callback=transaction_item_pre_save,
        extra_context=my_extra_context,)
   

@allif_base_view_wrapper
def commonWantToDeleteSupplierPayment(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonSupplierPaymentsModel,"Delete this item",
    'allifmaalcommonapp/payments/suppliers/x-supplier-payment-confrm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteSupplierPayment(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonSupplierPaymentsModel',pk=pk,success_redirect_url_name='commonSupplierPayments')


@allif_base_view_wrapper
def commonSupplierPaymentSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonSupplierPaymentsModel',search_fields_key='CommonSupplierPaymentsModel',
    template_path='allifmaalcommonapp/payments/suppliers/supplier-payments.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonSupplierPaymentAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='CommonSupplierPaymentsModel',advanced_search_config_key='CommonSupplierPaymentsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/payments/suppliers/supplier-payments.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')
@allif_base_view_wrapper
def commonPostSupplierPayment(request,pk,*allifargs,**allifkwargs):#global
    allif_data=common_shared_data(request)
    allifquery=CommonSupplierPaymentsModel.all_objects.filter(id=pk).first()
    allifsup=allifquery.supplier.id
    amount=allifquery.amount#this gives the amount of salary given to the staff
    pay_from_acc_id=allifquery.account.id
    mysupp=CommonSuppliersModel.all_objects.filter(id=allifsup).first()
    init_balance=mysupp.balance
    mysupp.balance=init_balance + amount
    mysupp.save()

    # reduce the balance of the cash account or account salary paid from
    payfromccount=CommonChartofAccountsModel.all_objects.filter(pk=pay_from_acc_id).first()
    acc_balance=payfromccount.balance
    payfromccount.balance=acc_balance-amount
    payfromccount.save()
    mysign=-1

    # update the supplier statement as well.
    transaction=CommonSupplierStatementsModel.all_objects.create(supplier=mysupp,credit=amount*mysign,
    comments="Payment",balance= Decimal(init_balance)+Decimal(amount))#get the ord
    
    CommonLedgerEntriesModel.all_objects.create(supplier=mysupp,credit=amount*mysign,
    comments="Payment",balance= Decimal(init_balance)+Decimal(amount),company=allif_data.get("main_sbscrbr_entity"),owner=request.user,ledgowner="supplier")#get the ord
    legs=CommonLedgerEntriesModel.all_objects.all()

    allifquery.status="posted"
    allifquery.save()
    return redirect('allifmaalcommonapp:commonSupplierPayments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

@allif_base_view_wrapper
def commonPostedSupplierPayments(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Posted Supplier Payments"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonSupplierPaymentsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/payments/suppliers/posted-payments.html',context)


@allif_base_view_wrapper
def commonPaySupplierDirect(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddSupplierPaymentForm,
    "Supplier Payment Initiations","commonSupplierPayments",'allifmaalcommonapp/payments/suppliers/pay-supplier-directly.html')

#
################ SUPPLIER STATEMENTS####################
@allif_base_view_wrapper
def commonSupplierStatementpdf(request, pk, *allifargs, **allifkwargs):
    return allif_document_pdf_handler(request,pk=pk,document_config_key='CommonSuppliersModel',)


######################### customer payments #################3
@allif_base_view_wrapper
def commonCustomerPayments(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Customer Payments"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonCustomerPaymentsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/payments/customers/customer-payments.html',context)

def commonTopUpCustomerAccount(request,pk,*allifargs,**allifkwargs):
    allif_data = common_shared_data(request)
    customer_instance = get_object_or_404(CommonCustomersModel.all_objects, id=pk)
    def customer_payment_pre_save(obj, request, allif_data):
        obj.customer = customer_instance
    default_cash_accs = CommonChartofAccountsModel.objects.filter(description="Cash").first()
    initial_form_data = {'account': default_cash_accs} if default_cash_accs else {}
    topups_queryset = CommonCustomerPaymentsModel.objects.filter(customer=customer_instance)
    extra_context={"customer": customer_instance,"topups": topups_queryset,}
    return allif_common_form_submission_and_save(request,CommonAddCustomerPaymentForm,
        f"Receive Payment From {customer_instance}", # Dynamic title
        "commonCustomerPayments", # The URL name for customer payments list
        'allifmaalcommonapp/payments/customers/add-customer-payment.html',
        pre_save_callback=customer_payment_pre_save,
        initial_data=initial_form_data,)
    

@allif_base_view_wrapper
def commonWantToDeleteCustomerPayment(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonCustomerPaymentsModel,"Delete this item",
    'allifmaalcommonapp/payments/customers/x-cust-payment-confrm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteCustomerPayment(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonCustomerPaymentsModel',pk=pk,success_redirect_url_name='commonCustomerPayments')


@allif_base_view_wrapper
def commonCustomerPaymentSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonCustomerPaymentsModel',search_fields_key='CommonCustomerPaymentsModel',
    template_path='allifmaalcommonapp/payments/customers/customer-payments.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonCustomerPaymentAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='CommonCustomerPaymentsModel',advanced_search_config_key='CommonCustomerPaymentsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/payments/customers/customer-payments.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def commonCustomerPaymentDetails(request, pk, *allifargs, **allifkwargs):
    allifquery= get_object_or_404(CommonCustomerPaymentsModel, id=pk) 
    return allif_common_form_edit_and_save(request,pk,CommonAddCustomerPaymentForm,"Customer Payment Details",
    'commonCustomerPaymentDetails','allifmaalcommonapp/payments/customers/customer-payment-details.html',
    redirect_with_pk=True,redirect_pk_value=pk,)
 

@allif_base_view_wrapper
def commonReceiveCustomerMoney(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddCustomerPaymentForm,"Receipt Customer Money",
    "commonTaxParameters",'allifmaalcommonapp/payments/customers/receive-customer-money.html')

@allif_base_view_wrapper
def commonPostCustomerPayment(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    payment=CommonCustomerPaymentsModel.all_objects.get(id=pk)#very important to get id to go to particular shipment
    myamount=payment.amount#this gives the initial account
    customer=payment.customer
    debit_acc=payment.account
    if (customer and myamount)!=None:
        mycust=CommonCustomersModel.all_objects.get(id=customer.id)
        initial_cust_acc_bal=mycust.balance
        mycust.balance= Decimal(initial_cust_acc_bal)-Decimal(myamount)
        mycust.status=='posted'
        mycust.save()

        # debit the asset account where the money from customer is received to
        coa_acc=CommonChartofAccountsModel.all_objects.get(id=debit_acc.id)
        initial_coa_acc_bal=coa_acc.balance
        coa_acc.balance= Decimal(initial_coa_acc_bal)+Decimal(myamount)
        coa_acc.save()
        CommonLedgerEntriesModel.all_objects.create(customer=customer,credit=myamount,
        comments="payment",company=allif_data.get("main_sbscrbr_entity"),owner=request.user,ledgowner="customer")
        return redirect('allifmaalcommonapp:commonCustomerPayments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

    else:
        return render(request,'allifmaalcommonapp/error/error.html')

@allif_base_view_wrapper
def commonPostedCustomerPayments(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Posted Customer Payments"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonCustomerPaymentsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/payments/customers/customer-posted-payments.html',context)

@allif_base_view_wrapper
def commonCustomerStatementpdf(request, pk, *allifargs, **allifkwargs):
    return allif_document_pdf_handler(request,pk=pk,document_config_key='CommonCustomersModel',)


########################3 staff salaries #############
@allif_base_view_wrapper
def commonSalaries(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Salaries"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonSalariesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/hrm/salaries/salaries.html',context)

@allif_base_view_wrapper
def commonAddSalary(request, *allifargs, **allifkwargs):
    return allif_common_form_submission_and_save(request,CommonAddSalaryForm,"New Salary","commonSalaries",'allifmaalcommonapp/hrm/salaries/add-salary.html')

@allif_base_view_wrapper
def commonEditSalaryDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddSalaryForm,"Edit Salary","commonSalaries",'allifmaalcommonapp/hrm/salaries/add-salary.html')
@allif_base_view_wrapper
def commonSalaryDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=CommonSalariesModel,pk=pk,
        template_name='allifmaalcommonapp/hrm/salaries/salary-details.html', # Create this template
        title_map={'default': 'Salary Details'},)

@allif_base_view_wrapper
def commonWantToDeleteSalary(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonSalariesModel,"Delete this item",'allifmaalcommonapp/hrm/salaries/x-salary-confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def commonDeleteSalary(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonSalariesModel',pk=pk,success_redirect_url_name='commonSalaries')

@allif_base_view_wrapper
def commonSalarySearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonSalariesModel',search_fields_key='CommonSalariesModel',
    template_path='allifmaalcommonapp/hrm/salaries/salaries.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonSalaryAdvanceSearch(request,*allifargs,**allifkwargs):
    # This view now simply calls the centralized advanced search handler
    return allif_advance_search_handler(request,model_name='CommonSalariesModel',advanced_search_config_key='CommonSalariesModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/hrm/salaries/salaries.html', # Template for HTML results
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html', # <-- CRITICAL: Pass the PDF template path
        #accounts/coa-search-pdf.html
    )
    

def commonPostSalary(request,pk,*allifargs,**allifkwargs):

    allif_data=common_shared_data(request)
    allifquery=CommonSalariesModel.all_objects.get(id=pk)
    emp_no=allifquery.staff.number
    normal_salary=allifquery.amount#this gives the amount of salary given to the staff
    month_salary=allifquery.salary_payable
    pay_from_acc_id=allifquery.account.id
    
    CommonLedgerEntriesModel.all_objects.create(credit=month_salary,
    comments="payment",company=allif_data.get("main_sbscrbr_entity"),owner=request.user,ledgowner="staff")

    # first get the salaries account
    salaries_balance=CommonChartofAccountsModel.all_objects.filter(description="Salaries")
    equityacc=CommonChartofAccountsModel.all_objects.filter(description="Equity")
    if salaries_balance and equityacc:

        # increase the salaries expense account
        sal_balances=CommonChartofAccountsModel.all_objects.get(description="Salaries")
        init_balance=sal_balances.balance
        sal_balances.balance=init_balance +month_salary
        sal_balances.save()

        # reduce the balance of the cash account or account salary paid from
        salaryaccount=CommonChartofAccountsModel.all_objects.get(pk=pay_from_acc_id)
        acc_balance=salaryaccount.balance
        salaryaccount.balance=acc_balance-month_salary
        salaryaccount.save()

        # reduce the balance of the equity account to balance the accounting equation...
        equityaccount=CommonChartofAccountsModel.all_objects.get(description="Equity")
        acc_balance=equityaccount.balance
        equityaccount.balance=acc_balance-month_salary
        equityaccount.save()

        # increase the value in the accommulation in the hrm model
        allifstaff=CommonEmployeesModel.all_objects.get(number=emp_no)
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
        
     
@allif_base_view_wrapper
def commonPostedSalaries(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Posted Salaries"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonSalariesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/hrm/salaries/posted-salaries.html',context)

################################ JOBS ############################
@allif_base_view_wrapper
def commonJobs(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Jobs"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonJobsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/jobs/jobs.html',context)

@allif_base_view_wrapper
def commonNewJobs(request,*allifargs,**allifkwargs):
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
    newJobRef=CommonJobsModel.objects.create(number=jobNo,description="Job Description",company=allif_data.get("main_sbscrbr_entity"),owner=allif_data.get("usernmeslg") or None,
                division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
    newJobRef.save()
    return redirect('allifmaalcommonapp:commonJobs',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

@allif_base_view_wrapper
def commonWantToDeleteJob(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonJobsModel,"Delete this item",'allifmaalcommonapp/jobs/delete_job_confirm.html')

@allif_base_view_wrapper
def commonDeleteJob(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonJobsModel',pk=pk,success_redirect_url_name='commonJobs')

@allif_base_view_wrapper
def commonJobSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonJobsModel',search_fields_key='CommonJobsModel',
    template_path='allifmaalcommonapp/jobs/jobs.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonJobAdvanceSearch(request,*allifargs,**allifkwargs):
    # This view now simply calls the centralized advanced search handler
    return allif_advance_search_handler(request,model_name='CommonJobsModel',advanced_search_config_key='CommonJobsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/jobs/jobs.html', # Template for HTML results
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html', # <-- CRITICAL: Pass the PDF template path
        #accounts/coa-search-pdf.html
    )
 
@allif_base_view_wrapper
def commonAddJobDetails(request, pk, *allifargs, **allifkwargs):
    #allifquery= get_object_or_404(CommonInvoicesModel, id=pk) 
    allifquery=CommonJobsModel.all_objects.filter(id=pk).first()
    return allif_common_form_edit_and_save(request,pk,CommonAddJobDetailsForm,"Add Job Details",
    'commonAddJobDetails','allifmaalcommonapp/jobs/add-job-details.html',
    redirect_with_pk=True,redirect_pk_value=pk,)
    
@allif_base_view_wrapper
def commonAddJobItems(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery= get_object_or_404(CommonInvoicesModel, id=pk) 
    allifquery=CommonJobsModel.all_objects.filter(id=pk).first()
    allifqueryset=CommonJobItemsModel.objects.filter(jobitemconnector=allifquery)
   
    def transaction_item_pre_save(obj, request, allif_data):
        obj.jobitemconnector=allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset}
    return allif_common_form_submission_and_save(request,form_class=CommonAddJobItemsForm,
        title_text="Add Invoice Items",
        success_redirect_url_name='commonAddJobItems', # This URL expects a PK
        template_path='allifmaalcommonapp/jobs/add-job-items.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)

@allif_base_view_wrapper
def commonDeleteJobItem(request,pk,*allifargs,**allifkwargs):
    #query=get_object_or_404(CommonInvoiceItemsModel, id=pk)
    query=CommonJobItemsModel.all_objects.filter(id=pk).first()
    allifquery=query.jobitemconnector.id
    return allif_delete_hanlder(request,model_name='CommonJobItemsModel',
    pk=pk,success_redirect_url_name='commonAddJobItems',redirect_with_pk=True,redirect_pk_value=allifquery)


@allif_base_view_wrapper
def commonInvoiceJob(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery= get_object_or_404(CommonInvoicesModel, id=pk) 
    allifquery=CommonJobsModel.all_objects.filter(id=pk).first()
    allifqueryset=CommonJobItemsModel.objects.filter(jobitemconnector=allifquery)
   
    def transaction_item_pre_save(obj, request, allif_data):
        obj.jobitemconnector=allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset}
    return allif_common_form_submission_and_save(request,form_class=CommonAddJobItemsForm,
        title_text="Add Invoice Items",
        success_redirect_url_name='commonInvoiceJob', # This URL expects a PK
        template_path='allifmaalcommonapp/jobs/invoice-job.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)


@allif_base_view_wrapper
def commonJobInvoicePdf(request, pk, *allifargs, **allifkwargs):
    return allif_document_pdf_handler(request,pk=pk,document_config_key='CommonJobsModel',)

@allif_base_view_wrapper
def commonJobTransactionReportpdf(request, pk, *allifargs, **allifkwargs):
    return allif_document_pdf_handler(request,pk=pk,document_config_key='CommonJobsModel',)

#####################################3 shipments ##########################
@allif_base_view_wrapper
def commonTransits(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Transportations"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonTransitModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/transport/transits.html',context)

@allif_base_view_wrapper
def commonWantToDeleteTransit(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonTransitModel,"Delete this item",'allifmaalcommonapp/transport/delete-transit-confirm.html')

@allif_base_view_wrapper
def commonDeleteTransit(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonTransitModel',pk=pk,success_redirect_url_name='commonTransits')

@allif_base_view_wrapper
def commonTransitSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonTransitModel',search_fields_key='CommonTransitModel',
    template_path='allifmaalcommonapp/transport/transits.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonTransitAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='CommonTransitModel',advanced_search_config_key='CommonTransitModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/transport/transits.html',
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html',)
 
@allif_base_view_wrapper
def commonAddTransitDetails(request, pk, *allifargs, **allifkwargs):
    allifquery=CommonTransitModel.all_objects.filter(id=pk).first()
    return allif_common_form_edit_and_save(request,pk,CommonAddTransitDetailsForm,"Add Shipment",
    'commonAddTransitDetails','allifmaalcommonapp/transport/add_transit_details.html',
    redirect_with_pk=True,redirect_pk_value=pk,)
    
@allif_base_view_wrapper
def commonAddShipmentItems(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery= get_object_or_404(CommonInvoicesModel, id=pk) 
    allifquery=CommonTransitModel.all_objects.filter(id=pk).first()
    allifqueryset=CommonTransitItemsModel.objects.filter(shipment=allifquery)
   
    def transaction_item_pre_save(obj, request, allif_data):
        obj.shipment=allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset}
    return allif_common_form_submission_and_save(request,form_class=CommonAddTransitItemsForm,
        title_text="Add Transit Items",
        success_redirect_url_name='commonAddShipmentItems', # This URL expects a PK
        template_path='allifmaalcommonapp/transport/shipments/add_shipment_items.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)

@allif_base_view_wrapper
def commonDeleteShipmentItem(request,pk,*allifargs,**allifkwargs):
    #query=get_object_or_404(CommonInvoiceItemsModel, id=pk)
    query=CommonTransitItemsModel.all_objects.filter(id=pk).first()
    allifquery=query.shipment.id
    return allif_delete_hanlder(request,model_name='CommonTransitItemsModel',
    pk=pk,success_redirect_url_name='commonAddShipmentItems',redirect_with_pk=True,redirect_pk_value=allifquery)


@allif_base_view_wrapper
def commonNewTransit(request,*allifargs,**allifkwargs):
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

    newQuoteNumber=CommonTransitModel.objects.create(number=sqnmbr,company=allif_data.get("main_sbscrbr_entity"),owner=allif_data.get("usernmeslg"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
    newQuoteNumber.save()
    return redirect('allifmaalcommonapp:commonTransits',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

@allif_base_view_wrapper
def commonEditShipmentItem(request,pk,*allifargs,**allifkwargs):
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
    
@allif_base_view_wrapper
def commonShipmentItemDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=CommonTransitItemsModel,pk=pk,
        template_name='allifmaalcommonapp/transport/shipments/shipment_item_details.html', # Create this template
        title_map={'default': 'Item Shipment Details'},)
    
@allif_base_view_wrapper
def commonTransitToPdf(request, pk, *allifargs, **allifkwargs):
    return allif_document_pdf_handler(request,pk=pk,document_config_key='CommonTransitModel',)


###################### profit and loss section ###################3
@allif_base_view_wrapper
def commonProfitAndLoss(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Profit & Loss"
    
    latest=CommonInvoicesModel.all_objects.order_by('-date').filter(posting_inv_status='posted')[:7]
    totalsales=CommonInvoicesModel.all_objects.filter(posting_inv_status='posted').order_by('-invoice_total').aggregate(Sum('invoice_total'))['invoice_total__sum']
    totalrevenue=CommonChartofAccountsModel.all_objects.filter(code__lt=49999,code__gt=39999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
    totalgoodscost=CommonInvoicesModel.all_objects.filter(posting_inv_status='posted').order_by('-invoice_items_total_cost').aggregate(Sum('invoice_items_total_cost'))['invoice_items_total_cost__sum']
    grossprofitorloss=(totalsales or 0)-(totalgoodscost or 0)
    #totalexpenses=totalgoodscost=AllifmaalExpensesModel.objects.all().order_by('-amount').aggregate(Sum('amount'))['amount__sum']
    totexpenses=CommonChartofAccountsModel.all_objects.filter(code__lt=59999,code__gt=49999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
    netprofitorloss=grossprofitorloss-(totexpenses or 0)
    totalrevenue=CommonChartofAccountsModel.all_objects.filter(code__lt=49999,code__gt=39999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
    #order_by('-amount').aggregate(Sum('amount'))['amount__sum']
    exps=CommonChartofAccountsModel.all_objects.filter(code__lt=59999,code__gt=49999)
    
    context={"title":title,}
    return render(request,'allifmaalcommonapp/statements/financial/p&l-statement.html',context)

######################################### REPORTS SECTION ############33
@allif_base_view_wrapper
def commonMainReports(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Main Reports"
  
    context={"title":title,}
    return render(request,'allifmaalcommonapp/reports/reports.html',context)
@allif_base_view_wrapper
def commonDebtorsReport(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]
    allifqueryset=CommonCustomersModel.objects.filter(balance__gte=1,company=allif_data.get("main_sbscrbr_entity")).order_by('date')
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

@allif_base_view_wrapper
def commonCreditorsReportpdf(request,*allifargs,**allifkwargs):
   
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

@allif_base_view_wrapper
def commonAvailableStockpdf(request,*allifargs,**allifkwargs):
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
   
################################## TASKS ###########################################

@allif_base_view_wrapper
def commonTasks(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    allifqueryset=CommonTasksModel.objects.filter(task_status="incomplete",company=allif_data.get("main_sbscrbr_entity")).order_by('date')
   
    my_extra_context={"allifqueryset": allifqueryset}
    return allif_common_form_submission_and_save(request,form_class=CommonAddTasksForm,title_text="To do list",
        success_redirect_url_name='commonTasks',template_path='allifmaalcommonapp/tasks/tasks.html',
        extra_context=my_extra_context,)

@allif_base_view_wrapper
def commonMarkTaskComplete(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    mark_complete=CommonTasksModel.objects.filter(id=pk).first()
    if mark_complete.status=="incomplete":
        mark_complete.status="complete"
        mark_complete.save()
    
    else:
        mark_complete.status="incomplete"
        mark_complete.save()
    return redirect('allifmaalcommonapp:commonTasks',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

@allif_base_view_wrapper
def commonCompletedTasks(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Completed Tasks"
    formats=CommonDocsFormatModel.objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,CommonTasksModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalcommonapp/tasks/finished-tasks.html',context)


@allif_base_view_wrapper
def commonEditTask(request,pk,*allifargs,**allifkwargs):
    return allif_common_form_edit_and_save(request,pk,CommonAddTasksForm,"Edit Task","commonTasks",
    'allifmaalcommonapp/tasks/tasks.html')

@allif_base_view_wrapper
def commonDeleteTask(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='CommonTasksModel',pk=pk,success_redirect_url_name='commonTasks')


########################## progress reporting/recording#################################3
@allif_base_view_wrapper
def commonProgress(request, pk, *allifargs, **allifkwargs):
    allif_data=common_shared_data(request)
    formats=CommonDocsFormatModel.objects.all()
    allifquery=CommonTransactionsModel.all_objects.filter(id=pk).first()
    allifqueryset=CommonProgressModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),trans_number=allifquery)
    return allif_common_detail_view(request,model_class=CommonTransactionsModel,pk=pk,
        template_name='allifmaalcommonapp/records/progress/progress.html',
        title_map={'default': 'Progress Details'},
        related_data_configs=[
            {
            'context_key': 'allifqueryset',
            'related_model': 'CommonProgressModel',
            'filter_field': 'trans_number',
            'order_by': ['number'],
            },
        ]
    )


@allif_base_view_wrapper
def commonWantToDeleteProgress(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,CommonProgressModel,"Delete this item",'allifmaalcommonapp/records/progress/delete_progress_confirm.html')

@allif_base_view_wrapper
def commonProgressSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='CommonProgressModel',search_fields_key='CommonProgressModel',
    template_path='allifmaalcommonapp/records/progress/progress.html',search_input_name='allifsearchcommonfieldname',)


@allif_base_view_wrapper
def commonProgressAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='CommonProgressModel',advanced_search_config_key='CommonProgressModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalcommonapp/records/progress/progress.html',
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html',)
 
@allif_base_view_wrapper
def commonAddProgress(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    #allifquery= get_object_or_404(CommonInvoicesModel, id=pk) 
    allifquery=CommonTransactionsModel.all_objects.filter(id=pk).first()
   
    def transaction_item_pre_save(obj, request, allif_data):
        obj.trans_number=allifquery
    my_extra_context={"allifquery":allifquery}
    return allif_common_form_submission_and_save(request,form_class=CommonAddProgressForm,
        title_text="New Progress",
        success_redirect_url_name='commonAddProgress', # This URL expects a PK
        template_path='allifmaalcommonapp/records/progress/add_progress.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)


@allif_base_view_wrapper
def commonEditProgress(request, pk, *allifargs, **allifkwargs):
    query=CommonProgressModel.all_objects.filter(id=pk).first()
    allifquery=query.trans_number.id
    return allif_common_form_edit_and_save(request,pk,CommonAddProgressForm,"Add Progress",
    'commonProgress','allifmaalcommonapp/records/progress/add_progress.html',
    redirect_with_pk=True,redirect_pk_value=allifquery,)
 
@allif_base_view_wrapper
def commonProgressDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=CommonProgressModel,pk=pk,
        template_name='allifmaalcommonapp/records/progress/progress_details.html', # Create this template
        title_map={'default': 'Progress Details'},)
 
@allif_base_view_wrapper
def commonDeleteProgress(request,pk,*allifargs,**allifkwargs):
    query=CommonProgressModel.all_objects.filter(id=pk).first()
    allifquery=query.trans_number.id
    return allif_delete_hanlder(request,model_name='CommonProgressModel',
    pk=pk,success_redirect_url_name='commonProgress',redirect_with_pk=True,redirect_pk_value=allifquery)


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
