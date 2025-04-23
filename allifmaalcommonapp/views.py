from django.shortcuts import render,redirect,get_object_or_404
from.models import *
from datetime import date
from django.core.mail import send_mail
#from sms import send_sms
from django.contrib.sessions.models import Session
import sms
from .sessions import Allifsessions
from twilio.rest import Client
from.forms import *
from .decorators import allifmaal_admin,allifmaal_admin_supperuser, unauthenticated_user,allowed_users,logged_in_user_is_owner_ceo,logged_in_user_can_add_view_edit_delete,logged_in_user_can_add,logged_in_user_can_view,logged_in_user_can_edit,logged_in_user_can_delete,logged_in_user_is_admin
import datetime
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.serializers import serialize
import json
from django.contrib.auth.models import Group
from decimal import Decimal
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from allifmaalusersapp.forms import CreateNewCustomUserForm
from django.http.response import HttpResponse, JsonResponse

from allifmaalusersapp.forms import UpdateCustomUserForm
from django.template.loader import get_template
from django.db.models import Q
from xhtml2pdf import pisa
from decimal import Decimal
from django.db.models import Count,Min,Max,Avg,Sum
from .resources import commonCompanyResource
from tablib import Dataset
from .resources import *
def commonWebsite(request):
    try:
        title="Allifmaal ERP"
        context={"title":title,}
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
        user_var=request.user
        usrslg=request.user.customurlslug
        user_var_comp=request.user.usercompany # this gives the slug of the company that the logged in user belongs to.
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var_comp).first()
        if main_sbscrbr_entity is None:#means that the logged user did not create a company and does not belong to any company
            return redirect('allifmaalcommonapp:commonAddnewEntity',allifusr=user_var)
        
        elif main_sbscrbr_entity!=None:
            sctr=str(main_sbscrbr_entity.sector)# this is very important...
            if sctr=="Sales":
                return redirect('allifmaalsalesapp:salesHome',allifusr=usrslg,allifslug=user_var_comp)
            elif sctr=="Healthcare":
                return redirect('allifmaalshaafiapp:shaafiHome',allifusr=usrslg,allifslug=user_var_comp)
            elif sctr=="Hospitality":
                return redirect('allifmaalhotelsapp:hotelsHome',allifusr=usrslg,allifslug=user_var_comp)
            elif sctr=="Education":
                return redirect('allifmaalilmapp:ilmHome',allifusr=usrslg,allifslug=user_var_comp)
            elif sctr=="Services":
                return redirect('allifmaalservicesapp:servicesHome',allifusr=usrslg,allifslug=user_var_comp)
            elif sctr=="Realestate":
                return redirect('allifmaalrealestateapp:realestateHome',allifusr=usrslg,allifslug=user_var_comp)
            elif sctr=="Logistics":
                return redirect('allifmaallogisticsapp:logisticsHome',allifusr=usrslg,allifslug=user_var_comp)
        else:
            return render(request,'allifmaalcommonapp/error/error.html')
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
def commonHome(request,*allifargs,**allifkwargs):
    try:
        if request.user.email.endswith("info@allifmaal.com"):#just for remembering purposes
            pass
        usrslg=request.user.customurlslug
        user_var_comp=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var_comp).first()
        if main_sbscrbr_entity!=None:
            sctr=str(main_sbscrbr_entity.sector)# this is very important...
            if sctr=="Sales":
                return redirect('allifmaalsalesapp:salesHome',allifusr=usrslg,allifslug=user_var_comp)
            elif sctr=="Healthcare":
                return redirect('allifmaalshaafiapp:shaafiHome',allifusr=usrslg,allifslug=user_var_comp)
            elif sctr=="Hospitality":
                return redirect('allifmaalhotelsapp:hotelsHome',allifusr=usrslg,allifslug=user_var_comp)
            elif sctr=="Education":
                return redirect('allifmaalilmapp:ilmHome',allifusr=usrslg,allifslug=user_var_comp)
            elif sctr=="Services":
                return redirect('allifmaalservicesapp:servicesHome',allifusr=usrslg,allifslug=user_var_comp)
            elif sctr=="Realestate":
                return redirect('allifmaalrealestateapp:realestateHome',allifusr=usrslg,allifslug=user_var_comp)
            elif sctr=="Logistics":
                return redirect('allifmaallogisticsapp:logisticsHome',allifusr=usrslg,allifslug=user_var_comp)
            else:
                return redirect('allifmaalcommonapp:CommonDecisionPoint')
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

################################### Sectors ############################### 
@login_required(login_url='allifmaalusersapp:userLoginPage')
@allifmaal_admin
@logged_in_user_can_view
def commonSectors(request,allifusr,*allifargs,**allifkwargs):
    try:
        title="Main Sectors"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        user_var=request.user
        allifqueryset=CommonSectorsModel.objects.all()
        form=CommonAddSectorForm()
        if request.method == 'POST':
            form=CommonAddSectorForm(request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner =user_var
                obj.save()
                return redirect('allifmaalcommonapp:commonSectors',allifusr=usrslg,allifslug=user_var)
            else:
                form=CommonAddSectorForm()
        else:
            form=CommonAddSectorForm()
        context = {
            "title":title,
            "form":form,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/sectors/sectors.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@allifmaal_admin
@logged_in_user_can_view
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
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
#@allowed_users(allowed_roles=['admin','staff'])

@allifmaal_admin
@logged_in_user_can_edit
def commonEditSector(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Sector Details"
        allifqueryset=CommonSectorsModel.objects.all()
        update_allifquery=CommonSectorsModel.objects.get(id=pk)
        user_var=request.user
        form =CommonAddSectorForm(instance=update_allifquery)
        if request.method == 'POST':
            form =CommonAddSectorForm(request.POST, instance=update_allifquery)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner =user_var
                obj.save()
                user_var=request.user.usercompany
                usrslg=request.user.customurlslug
                return redirect('allifmaalcommonapp:commonSectors',allifusr=usrslg,allifslug=user_var)
                
            else:
                form =CommonAddSectorForm(instance=update_allifquery)
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
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@allifmaal_admin  
def commonWantToDeleteSector(request,pk,*allifargs,**allifkwargs):
    try:
        allifqueryset=CommonSectorsModel.objects.all()
        myallifquery=CommonSectorsModel.objects.filter(id=pk).first()
        form=CommonAddSectorForm()
        title="Are sure to delete?"
        context={
        "title":title,
        "myallifquery":myallifquery,
        "allifqueryset":allifqueryset,
        "form":form,
        }
        return render(request,'allifmaalcommonapp/sectors/sectors.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
     
@login_required(login_url='allifmaalusersapp:userLoginPage')
@allifmaal_admin
@logged_in_user_can_delete  
def commonSectorDelete(request,pk):
    try:
        usrslg=request.user.customurlslug
        CommonSectorsModel.objects.filter(id=pk).first().delete()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        return redirect('allifmaalcommonapp:commonSectors',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

################################### Sectors ############################### 
@login_required(login_url='allifmaalusersapp:userLoginPage')
@allifmaal_admin
@logged_in_user_can_view
def commonLoadContentTest(request):
    try:
        title="Main Sectors"
        
        context = {
            "title":title,
          
        }
        return render(request,'allifmaalcommonapp/sectors/sectors-list.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
################################### Sectors ############################### 
@login_required(login_url='allifmaalusersapp:userLoginPage')
@allifmaal_admin
@logged_in_user_can_view
def commonDocsFormat(request,*allifargs,**allifkwargs):
    try:
        title="Formats"
        user_var=request.user
        allifqueryset=CommonDocsFormatModel.objects.all()
        form=CommonAddDocFormatForm()
        if request.method == 'POST':
            form=CommonAddDocFormatForm(request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner =user_var
                obj.save()
            else:
                form=CommonAddDocFormatForm()
        else:
            form=CommonAddDocFormatForm()
        context = {
            "title":title,
            "form":form,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/docformats/docformats.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@allifmaal_admin
@logged_in_user_can_edit
def commonEditDocsFormat(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Format"
        update=CommonDocsFormatModel.objects.get(id=pk)
        user_var=request.user
        form =CommonAddDocFormatForm(instance=update)
        if request.method == 'POST':
            form =CommonAddDocFormatForm(request.POST, instance=update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner =user_var
                obj.save()
                user_var=request.user.usercompany
                usrslg=request.user.customurlslug
                return redirect('allifmaalcommonapp:commonDocsFormat',allifusr=usrslg,allifslug=user_var)
                
            else:
                form =CommonAddSectorForm(instance=update)
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
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@allifmaal_admin 
@logged_in_user_can_delete
def commonDeleteDocsFormat(request,pk,*allifargs,**allifkwargs):
    try:
        usrslg=request.user.customurlslug
        CommonDocsFormatModel.objects.filter(id=pk).first().delete()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        return redirect('allifmaalcommonapp:commonDocsFormat',allifusr=usrslg,allifslug=user_var)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

################################### Sectors ############################### 
@login_required(login_url='allifmaalusersapp:userLoginPage')
@allifmaal_admin
@logged_in_user_can_view
def commonDataSorts(request,*allifargs,**allifkwargs):
    try:
        title="Main Filters"
        user_var=request.user
        allifqueryset=CommonDataSortsModel.objects.all()
        form=CommonAddDataSortsForm()
        if request.method == 'POST':
            form=CommonAddDataSortsForm(request.POST or None)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner =user_var
                obj.save()
            else:
                form=CommonAddDataSortsForm()
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

@login_required(login_url='allifmaalusersapp:userLoginPage')
@allifmaal_admin
@logged_in_user_can_edit
def commonEditDataSort(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Filter Details"
        update=CommonDataSortsModel.objects.get(id=pk)
        user_var=request.user
        user_compny=request.user.usercompany
        usrslg=request.user.customurlslug
        form =CommonAddDataSortsForm(instance=update)
        if request.method == 'POST':
            form =CommonAddDataSortsForm(request.POST, instance=update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner =user_var
                obj.save()
                return redirect('allifmaalcommonapp:commonDataSorts',allifusr=usrslg,allifslug=user_compny)
                
            else:
                form =CommonAddDataSortsForm(instance=update)
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
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@allifmaal_admin  
@logged_in_user_can_delete
def commonDeleteDataSort(request,pk):
    try:
        usrslg=request.user.customurlslug
        user_compny=request.user.usercompany
        CommonDataSortsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonDataSorts',allifusr=usrslg,allifslug=user_compny)
                
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
############################### .......Entities and companies details........... #########################3#
@login_required(login_url='allifmaalloginapp:allifmaalUserLogin')
@allifmaal_admin
@logged_in_user_can_view
def commonCompanies(request,*allifargs,**allifkwargs):
    try:
        title="Registered Companies"
        user_var=request.user
        allifqueryset=CommonCompanyDetailsModel.objects.all()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                allifqueryset=CommonCompanyDetailsModel.objects.all().order_by("-company")
            else:
                allifqueryset=CommonCompanyDetailsModel.objects.all()
        
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "user_var":user_var,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request,'allifmaalcommonapp/companies/companies.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
def commonAddnewEntity(request,allifusr,*allifargs,**allifkwargs):
    try:
        title="Entity Registration"
        usrslg=request.user.customurlslug
        user_var_comp=request.user.usercompany
        user_var=request.user
        user_var_customrulslg=request.user.customurlslug
        usernmeslg=User.objects.filter(customurlslug=user_var_customrulslg).first()
        phone=usernmeslg.phone
        email=usernmeslg.email
        form=CommonAddCompanyDetailsForm(request.POST, request.FILES)
        if request.method == 'POST':
            form=CommonAddCompanyDetailsForm(request.POST,request.FILES)

            if form.is_valid():
                sector=int(request.POST.get('sector'))
                name=request.POST.get('company')
                address=request.POST.get('address')
                if name and sector!="":
                    sectorselec=CommonSectorsModel.objects.filter(id=sector).first()
                    obj = form.save(commit=False)
                    obj.owner =usernmeslg
                    obj.legalName=str(f'{name}+{address}')#important...used to generate company slug

                    if sectorselec.name=="Sales":
                        obj.save()
                        #the code below is for connecting the usercompany field of the User model with
                        newcompny=CommonCompanyDetailsModel.objects.filter(company=obj).first()
                        allifusr=User.objects.filter(email=user_var.email).first()
                        allifusr.usercompany=str(newcompny.companyslug)
                        allifusr.save()

                        ################## Sending an Email to notify system owner #######################
                        ahmed='info@allifmaal.com'
                        muse='allifmaalengineering@gmail.com'
                        subject = title
                        message = f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System'
                        email_sender=usernmeslg.email #'ahmedmusadir@gmail.com'
                        recipient_list = [ahmed,muse]
                        send_mail(subject, message, email_sender, recipient_list)# uncomment to send emails.
                        email=CommonEmailsModel(subject=subject,message=message,recipient=recipient_list,sender=email_sender)
                        email.save()

                        ################3 this below is for the SMS to notify system owner ###################
                        account_sid = "ACb19b2a5701ec5f53c38e113ae9595917" # Twilio account
                        auth_token  = "143c2731b15d0a8a9a918db838ac048a"  # Twilio Token
                        client = Client(account_sid, auth_token)
                        message = client.messages.create(
                        to="+252610993964",# number registered with Twilio
                        from_="+17753731268",#virtual number from Twilio
                        body=f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System') # message to be sent.
                        return redirect('allifmaalsalesapp:salesHome',allifusr=usrslg,allifslug=user_var_comp)

                    elif sectorselec.name=="Healthcare":
                        obj.save()
                        #the code below is for connecting the usercompany field of the User model with
                        newcompny=CommonCompanyDetailsModel.objects.filter(company=obj).first()
                        allifusr=User.objects.filter(email=user_var.email).first()
                        allifusr.usercompany=str(newcompny.companyslug)
                        allifusr.save()
                        ################## Sending an Email to notify system owner #######################
                        ahmed='info@allifmaal.com'
                        muse='allifmaalengineering@gmail.com'
                        subject = title
                        message = f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System'
                        email_sender=usernmeslg.email #'ahmedmusadir@gmail.com'
                        recipient_list = [ahmed,muse]
                        send_mail(subject, message, email_sender, recipient_list)# uncomment to send emails.
                        email=CommonEmailsModel(subject=subject,message=message,recipient=recipient_list,sender=email_sender)
                        email.save()

                        ################3 this below is for the SMS to notify system owner ###################
                        account_sid = "ACb19b2a5701ec5f53c38e113ae9595917" # Twilio account
                        auth_token  = "143c2731b15d0a8a9a918db838ac048a"  # Twilio Token
                        client = Client(account_sid, auth_token)
                        message = client.messages.create(
                        to="+252610993964",# number registered with Twilio
                        from_="+17753731268",#virtual number from Twilio
                        body=f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System') # message to be sent.
                        return redirect('allifmaalshaafiapp:shaafiHome',allifusr=usrslg,allifslug=user_var_comp)
                    elif sectorselec.name=="Hospitality":
                        obj.save()
                        #the code below is for connecting the usercompany field of the User model with
                        newcompny=CommonCompanyDetailsModel.objects.filter(company=obj).first()
                        allifusr=User.objects.filter(email=user_var.email).first()
                        allifusr.usercompany=str(newcompny.companyslug)
                        allifusr.save()
                        ################## Sending an Email to notify system owner #######################
                        ahmed='info@allifmaal.com'
                        muse='allifmaalengineering@gmail.com'
                        subject = title
                        message = f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System'
                        email_sender=usernmeslg.email #'ahmedmusadir@gmail.com'
                        recipient_list = [ahmed,muse]
                        send_mail(subject, message, email_sender, recipient_list)# uncomment to send emails.
                        email=CommonEmailsModel(subject=subject,message=message,recipient=recipient_list,sender=email_sender)
                        email.save()

                        ################3 this below is for the SMS to notify system owner ###################
                        account_sid = "ACb19b2a5701ec5f53c38e113ae9595917" # Twilio account
                        auth_token  = "143c2731b15d0a8a9a918db838ac048a"  # Twilio Token
                        client = Client(account_sid, auth_token)
                        message = client.messages.create(
                        to="+252610993964",# number registered with Twilio
                        from_="+17753731268",#virtual number from Twilio
                        body=f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System') # message to be sent.
                        return redirect('allifmaalhotelsapp:hotelsHome',allifusr=usrslg,allifslug=user_var_comp)
                    elif sectorselec.name=="Education":
                        obj.save()
                        #the code below is for connecting the usercompany field of the User model with
                        newcompny=CommonCompanyDetailsModel.objects.filter(company=obj).first()
                        allifusr=User.objects.filter(email=user_var.email).first()
                        allifusr.usercompany=str(newcompny.companyslug)
                        allifusr.save()
                        ################## Sending an Email to notify system owner #######################
                        ahmed='info@allifmaal.com'
                        muse='allifmaalengineering@gmail.com'
                        subject = title
                        message = f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System'
                        email_sender=usernmeslg.email #'ahmedmusadir@gmail.com'
                        recipient_list = [ahmed,muse]
                        send_mail(subject, message, email_sender, recipient_list)# uncomment to send emails.
                        email=CommonEmailsModel(subject=subject,message=message,recipient=recipient_list,sender=email_sender)
                        email.save()

                        ################3 this below is for the SMS to notify system owner ###################
                        account_sid = "ACb19b2a5701ec5f53c38e113ae9595917" # Twilio account
                        auth_token  = "143c2731b15d0a8a9a918db838ac048a"  # Twilio Token
                        client = Client(account_sid, auth_token)
                        message = client.messages.create(
                        to="+252610993964",# number registered with Twilio
                        from_="+17753731268",#virtual number from Twilio
                        body=f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System') # message to be sent.
                        return redirect('allifmaalilmapp:ilmHome',allifusr=usrslg,allifslug=user_var_comp)
                    
                    elif sectorselec.name=="Logistics":
                        obj.save()
                        #the code below is for connecting the usercompany field of the User model with
                        newcompny=CommonCompanyDetailsModel.objects.filter(company=obj).first()
                        allifusr=User.objects.filter(email=user_var.email).first()
                        allifusr.usercompany=str(newcompny.companyslug)
                        allifusr.save()
                        ################## Sending an Email to notify system owner #######################
                        ahmed='info@allifmaal.com'
                        muse='allifmaalengineering@gmail.com'
                        subject = title
                        message = f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System'
                        email_sender=usernmeslg.email #'ahmedmusadir@gmail.com'
                        recipient_list = [ahmed,muse]
                        send_mail(subject, message, email_sender, recipient_list)# uncomment to send emails.
                        email=CommonEmailsModel(subject=subject,message=message,recipient=recipient_list,sender=email_sender)
                        email.save()

                        ################3 this below is for the SMS to notify system owner ###################
                        account_sid = "ACb19b2a5701ec5f53c38e113ae9595917" # Twilio account
                        auth_token  = "143c2731b15d0a8a9a918db838ac048a"  # Twilio Token
                        client = Client(account_sid, auth_token)
                        message = client.messages.create(
                        to="+252610993964",# number registered with Twilio
                        from_="+17753731268",#virtual number from Twilio
                        body=f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System') # message to be sent.
                        return redirect('allifmaallogisticsapp:logisticsHome',allifusr=usrslg,allifslug=user_var_comp)
                    elif sectorselec.name=="Realestate":
                        obj.save()
                        #the code below is for connecting the usercompany field of the User model with
                        newcompny=CommonCompanyDetailsModel.objects.filter(company=obj).first()
                        allifusr=User.objects.filter(email=user_var.email).first()
                        allifusr.usercompany=str(newcompny.companyslug)
                        allifusr.save()
                        ################## Sending an Email to notify system owner #######################
                        ahmed='info@allifmaal.com'
                        muse='allifmaalengineering@gmail.com'
                        subject = title
                        message = f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System'
                        email_sender=usernmeslg.email #'ahmedmusadir@gmail.com'
                        recipient_list = [ahmed,muse]
                        send_mail(subject, message, email_sender, recipient_list)# uncomment to send emails.
                        email=CommonEmailsModel(subject=subject,message=message,recipient=recipient_list,sender=email_sender)
                        email.save()

                        ################3 this below is for the SMS to notify system owner ###################
                        account_sid = "ACb19b2a5701ec5f53c38e113ae9595917" # Twilio account
                        auth_token  = "143c2731b15d0a8a9a918db838ac048a"  # Twilio Token
                        client = Client(account_sid, auth_token)
                        message = client.messages.create(
                        to="+252610993964",# number registered with Twilio
                        from_="+17753731268",#virtual number from Twilio
                        body=f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System') # message to be sent.
                        return redirect('allifmaalrealestateapp:realestateHome',allifusr=usrslg,allifslug=user_var_comp)
                    elif sectorselec.name=="Services":
                        obj.save()
                        #the code below is for connecting the usercompany field of the User model with
                        newcompny=CommonCompanyDetailsModel.objects.filter(company=obj).first()
                        allifusr=User.objects.filter(email=user_var.email).first()
                        allifusr.usercompany=str(newcompny.companyslug)
                        allifusr.save()
                        ################## Sending an Email to notify system owner #######################
                        ahmed='info@allifmaal.com'
                        muse='allifmaalengineering@gmail.com'
                        subject = title
                        message = f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System'
                        email_sender=usernmeslg.email #'ahmedmusadir@gmail.com'
                        recipient_list = [ahmed,muse]
                        send_mail(subject, message, email_sender, recipient_list)# uncomment to send emails.
                        email=CommonEmailsModel(subject=subject,message=message,recipient=recipient_list,sender=email_sender)
                        email.save()

                        ################3 this below is for the SMS to notify system owner ###################
                        account_sid = "ACb19b2a5701ec5f53c38e113ae9595917" # Twilio account
                        auth_token  = "143c2731b15d0a8a9a918db838ac048a"  # Twilio Token
                        client = Client(account_sid, auth_token)
                        message = client.messages.create(
                        to="+252610993964",# number registered with Twilio
                        from_="+17753731268",#virtual number from Twilio
                        body=f'Kindly note that Name: {usernmeslg}, Email: {email}, Phone: {phone}, has created an entity in the AllifApp System') # message to be sent.
                        return redirect('allifmaalservicesapp:servicesHome',allifusr=usrslg,allifslug=user_var_comp)
                    
                    else:
                        form=CommonAddCompanyDetailsForm(request.POST, request.FILES)
        
                else:
                    form=CommonAddCompanyDetailsForm(request.POST, request.FILES)
            else:
                form=CommonAddCompanyDetailsForm(request.POST, request.FILES)
        else:
            form=CommonAddCompanyDetailsForm(request.POST, request.FILES)

        context={"form":form,
                 "title":title,}
        return render(request,'allifmaalcommonapp/companies/newentity.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonCompanyDetailsForClients(request,*allifargs,**allifkwargs):
    try:
        title="Company Details and Settings"
        user_var=request.user
        compslg=request.user.usercompany
        allifquery=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        scopes=CommonCompanyScopeModel.objects.filter(company=allifquery)
        context={
            "title":title,
            "user_var":user_var,
            "allifquery":allifquery,
            "scopes":scopes,
        }
        return render(request,'allifmaalcommonapp/companies/company-details-clients.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@allifmaal_admin 
@logged_in_user_can_view
def commonEditEntityByAllifAdmin(request,allifpk,*allifargs,**allifkwargs):
    try:
        title="Update Entity Details"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        user_var_update=CommonCompanyDetailsModel.objects.filter(companyslug=allifpk).first()
        form=CommonEditCompanyDetailsFormByAllifAdmin(instance=user_var_update)
        if request.method=='POST':
            form=CommonEditCompanyDetailsFormByAllifAdmin(request.POST or None,request.FILES, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                obj.save()
                return redirect('allifmaalcommonapp:commonCompanies',allifusr=usrslg,allifslug=user_var)
                
            else:
                form=CommonEditCompanyDetailsFormByAllifAdmin(request.POST or None, instance=user_var_update)
        else:
            form=CommonEditCompanyDetailsFormByAllifAdmin(request.POST or None, instance=user_var_update)
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/companies/edit-entity.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit
@logged_in_user_is_admin
def commonEditEntityByClients(request,allifpk,*allifargs,**allifkwargs):
    try:
        title="Update Entity Details"
        user_var=request.user.usercompany
        user=request.user
        usrslg=request.user.customurlslug
        user_var_update=CommonCompanyDetailsModel.objects.filter(companyslug=allifpk).first()
       
        form=CommonAddByClientCompanyDetailsForm(instance=user_var_update)
        if request.method=='POST':
            form=CommonAddByClientCompanyDetailsForm(request.POST or None,request.FILES, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user
                obj.userbranch=user_var_update.branch
                upduser=User.objects.filter(first_name=user).first()
                upduser.userbranch=user_var_update.branch
                upduser.save()
                obj.save()
                return redirect('allifmaalcommonapp:commonCompanyDetailsForClients',allifusr=usrslg,allifslug=user_var)
                
            else:
                form=CommonAddByClientCompanyDetailsForm(request.POST or None, instance=user_var_update)
        else:
            form=CommonAddByClientCompanyDetailsForm(request.POST or None, instance=user_var_update)
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/companies/edit-entity-client.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
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
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
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

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete
@logged_in_user_is_admin 
def commonWantToDeleteCompany(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonCompanyDetailsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        
        return render(request,'allifmaalcommonapp/companies/comp-delete-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete
@logged_in_user_is_admin
def commonDeleteEntity(request,allifslug,*allifargs,**allifkwargs):
    try:
        title="Are you sure to delete?"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        allifquery=CommonCompanyDetailsModel.objects.filter(companyslug=allifslug).first()
        if allifquery.can_delete=="undeletable":
            context={"allifquery":allifquery,"title":title,}
            return render(request,'allifmaalcommonapp/error/cant_delete.html',context)
        else:
            allifquery.delete()
            return redirect('allifmaalcommonapp:commonTasks',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonCompanySearch(request,*allifargs,**allifkwargs):
    try:
        title="Search"
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonCompanyDetailsModel.objects.filter(Q(company__contains=allifsearch) | Q(address__contains=allifsearch))
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
        }
        return render(request,'allifmaalcommonapp/companies/companies.html',context)
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@allifmaal_admin
def commonCompanyAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        allifqueryset=CommonCompanyDetailsModel.objects.all()
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('strtdate')
            end_date=request.POST.get('enddate')
            if start_date!="" and end_date!="":
                searched_data=CommonCompanyDetailsModel.objects.filter(Q(created_date__gte=start_date)& Q(created_date__lte=end_date))
                # if pdf is selected
                print(searched_data)
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/companies/search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
                    "scopes":scopes
                    }
                    response = HttpResponse(content_type='application/doc')
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
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
                elif selected_option=="excel":
                    compnyresource= commonCompanyResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    "formats":formats,
                    "title":title,
                     "scopes":scopes
                    }
                    return render(request,'allifmaalcommonapp/companies/companies.html',context)

            else:
                allifqueryset=CommonCompanyDetailsModel.objects.all()
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
             "scopes":scopes
            }
            return render(request,'allifmaalcommonapp/companies/companies.html',context)
        
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
             "scopes":scopes
            }
            return render(request,'allifmaalcommonapp/companies/companies.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
############################### .......Entities and companies details........... #########################3#
#@login_required(login_url='allifmaalloginapp:allifmaalUserLogin')
#@login_required(login_url='allifmaalusersapp:userLoginPage')
#@logged_in_user_can_view
@allifmaal_admin_supperuser
def commonDivisions(request,*allifargs,**allifkwargs):
    try:
        title="Divisions"
        num_visits = request.session.get('num_visits', 0)
        num_visits += 1
        request.session['num_visits'] = num_visits
        user_var=request.user
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonEmployeesModel.objects.filter(username=user_var,company=main_sbscrbr_entity).first()
        if user_var.can_access_all==True:
            allifqueryset=CommonDivisionsModel.objects.filter(company=main_sbscrbr_entity)
        else:
            if allifquery!=None:
                emplye_division=allifquery.division
                allifqueryset=CommonDivisionsModel.objects.filter(company=main_sbscrbr_entity,division=emplye_division)
            else:
                allifqueryset=[]

        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "user_var":user_var,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            "num_visits":num_visits,
        }
        return render(request,'allifmaalcommonapp/divisions/divisions.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#@login_required(login_url='allifmaalusersapp:userLoginPage')
#@logged_in_user_can_add
def commonAddDivision(request,*allifargs,**allifkwargs):
    try:
        title="New Division"
        usrslg=request.user.customurlslug
        user_var_comp=request.user.usercompany
        usernmeslg=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var_comp).first()
        #form=CommonAddDivisionForm(main_sbscrbr_entity)
        form=CommonAddDivisionForm()
        if request.method == 'POST':
            #form=CommonAddDivisionForm(main_sbscrbr_entity,request.POST,request.FILES)
            form=CommonAddDivisionForm(request.POST,request.FILES)
            if form.is_valid():
                division=request.POST.get('division')
                address=request.POST.get('address')
                if division!="":
                    obj = form.save(commit=False)
                    obj.owner=usernmeslg
                    obj.company=main_sbscrbr_entity
                    obj.legalname=str(f'{division}+{address}')#important...used to generate company slug
                    obj.save()
                    return redirect('allifmaalcommonapp:commonDivisions',allifusr=usrslg,allifslug=user_var_comp)
                  
                else:
                    #form=CommonAddDivisionForm(main_sbscrbr_entity,request.POST, request.FILES)
                    form=CommonAddDivisionForm(request.POST, request.FILES)
            else:
                form=CommonAddDivisionForm(request.POST, request.FILES)
        else:
            form=CommonAddDivisionForm(request.POST, request.FILES)

        context={"form":form,
                 "title":title,}
        return render(request,'allifmaalcommonapp/divisions/add-division.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit
@logged_in_user_is_admin
def commonEditDivision(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Division Details"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        user_var_update=CommonDivisionsModel.objects.filter(id=pk).first()
        form=CommonAddDivisionForm(instance=user_var_update)
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            form=CommonAddDivisionForm(request.POST or None,request.FILES, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                obj.company=main_sbscrbr_entity
                obj.save()
                return redirect('allifmaalcommonapp:commonDivisions',allifusr=usrslg,allifslug=compslg)

            else:
                form=CommonAddDivisionForm(request.POST or None, instance=user_var_update)
        else:
            form=CommonAddDivisionForm(request.POST or None, instance=user_var_update)
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/divisions/add-division.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonDivisionDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Division Details"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonDivisionsModel.objects.filter(id=pk).first()
        relatedqueryset=CommonBranchesModel.objects.filter(company=main_sbscrbr_entity,division=allifquery)
        
        context={
        "allifquery":allifquery,
        "relatedqueryset": relatedqueryset,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/divisions/division-details.html',context)
        #else:
            #return render(request,'allifmaalcommonapp/error/error.html')
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_is_admin
@logged_in_user_can_delete  
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete
@logged_in_user_is_admin
def commonDeleteDivision(request,pk,*allifargs,**allifkwargs):
    try:
        CommonDivisionsModel.objects.filter(pk=pk).first().delete()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        return redirect('allifmaalcommonapp:commonDivisions',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    


############################### .......Entities and companies details........... #########################3#
@login_required(login_url='allifmaalloginapp:allifmaalUserLogin')
@logged_in_user_can_view
def commonBranches(request,*allifargs,**allifkwargs):
    try:
        title="Branches"
        user_var=request.user
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonBranchesModel.objects.all()
        allifquery=CommonEmployeesModel.objects.filter(username=user_var,company=main_sbscrbr_entity).first()
        if user_var.can_access_all==True:
            allifqueryset=CommonBranchesModel.objects.filter(company=main_sbscrbr_entity)
        else:
            if allifquery!=None:
                emplye_division=allifquery.division
                allifqueryset=CommonBranchesModel.objects.filter(company=main_sbscrbr_entity,division=emplye_division)
            else:
                allifqueryset=[]

        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "user_var":user_var,
            "main_sbscrbr_entity":main_sbscrbr_entity,
        }
        return render(request,'allifmaalcommonapp/branches/branches.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_add
def commonAddBranch(request,*allifargs,**allifkwargs):
    try:
        title="New Branch"
        usrslg=request.user.customurlslug
        user_var_comp=request.user.usercompany
        usernmeslg=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var_comp).first()

        form=CommonAddBranchForm(main_sbscrbr_entity)
        if request.method == 'POST':
            form=CommonAddBranchForm(main_sbscrbr_entity,request.POST,request.FILES)
            if form.is_valid():
                branch=request.POST.get('branch')
                address=request.POST.get('address')
                if branch!="":
                    obj = form.save(commit=False)
                    obj.owner =usernmeslg
                    obj.company =main_sbscrbr_entity
                    obj.legalname=str(f'{branch}+{address}')#important...used to generate company slug
                    obj.save()

                    return redirect('allifmaalcommonapp:commonBranches',allifusr=usrslg,allifslug=user_var_comp)
                  
                else:
                    form=CommonAddBranchForm(main_sbscrbr_entity,request.POST, request.FILES)
            else:
                form=CommonAddBranchForm(main_sbscrbr_entity,request.POST, request.FILES)
        else:
            form=CommonAddBranchForm(main_sbscrbr_entity,request.POST, request.FILES)

        context={"form":form,
                 "title":title,}
        return render(request,'allifmaalcommonapp/branches/add-branch.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit 
def commonEditBranch(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Branch Details"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        user_var_update=CommonBranchesModel.objects.filter(id=pk).first()
        usernmeslg=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        form=CommonAddBranchForm(main_sbscrbr_entity,instance=user_var_update)

        if request.method=='POST':
            form=CommonAddBranchForm(main_sbscrbr_entity,request.POST or None,request.FILES, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=usernmeslg
                obj.company=main_sbscrbr_entity
                obj.save()
                return redirect('allifmaalcommonapp:commonBranches',allifusr=usrslg,allifslug=user_var)
                
            else:
                form=CommonAddBranchForm(main_sbscrbr_entity,request.POST or None, instance=user_var_update)
        else:
            form=CommonAddBranchForm(main_sbscrbr_entity,request.POST or None, instance=user_var_update)
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/branches/add-branch.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
def commonBranchDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Branch Details"
        user_var=request.user.usercompany
        usr=request.user
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        allifquery=CommonBranchesModel.objects.filter(id=pk).first()
        allifqry=CommonEmployeesModel.objects.filter(username=usr,company=main_sbscrbr_entity).first()
        if usr.can_access_all==True:
            if allifqry!=None:
                emplye_brnch=allifqry.branch
                emply_divison=allifqry.division
                emply_department=allifqry.department
                relatedqueryset=CommonDepartmentsModel.objects.filter(company=main_sbscrbr_entity,division=emply_divison,branch=emplye_brnch)
            else:
                relatedqueryset=[]
        else:
            if allifqry!=None:
                emplye_brnch=allifqry.branch
                emply_divison=allifqry.division
                emply_department=allifqry.department
                relatedqueryset=CommonDepartmentsModel.objects.filter(company=main_sbscrbr_entity,division=emply_divison,branch=emplye_brnch,description=emply_department)
            else:
                relatedqueryset=[]

        context={
            "allifquery":allifquery,
           "relatedqueryset":relatedqueryset,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/branches/branch-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_is_admin
@logged_in_user_can_delete 
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete
@logged_in_user_is_admin
def commonDeleteBranch(request,pk,*allifargs,**allifkwargs):
    try:
        CommonBranchesModel.objects.filter(pk=pk).first().delete()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        return redirect('allifmaalcommonapp:commonBranches',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonBranchSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search"
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonBranchesModel.objects.filter(Q(branch__contains=allifsearch) | Q(address__contains=allifsearch))
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
        }
        return render(request,'allifmaalcommonapp/branches/branches.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

 ################################### below are departments #######################
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonDepartments(request,*allifargs,**allifkwargs):
    try:
        title="Departments"
        user_var=request.user
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonDepartmentsModel.objects.all()
        allifquery=CommonEmployeesModel.objects.filter(username=user_var,company=main_sbscrbr_entity).first()
        if user_var.can_access_all==True:
            if allifquery!=None:
                emplye_division=allifquery.division
                allifqueryset=CommonDepartmentsModel.objects.filter(company=main_sbscrbr_entity)
            else:
                allifqueryset=[]
        else:
            if allifquery!=None:
                emplye_division=allifquery.division
                emplye_branch=allifquery.branch
                emplye_deptmnt=allifquery.department
                allifqueryset=CommonDepartmentsModel.objects.filter(company=main_sbscrbr_entity,division=emplye_division,branch=emplye_branch,description=emplye_deptmnt)
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonDepartmentSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonDepartmentsModel.objects.filter((Q(department__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/departments/departments.html',context)
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_add
def commonAddDepartment(request,*allifargs,**allifkwargs):
    try:
        title="Add New Department"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        usr=request.user
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        form=CommonAddDepartmentForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                descrp=request.POST.get('department')
                account=CommonDepartmentsModel.objects.filter(department=descrp,company=main_sbscrbr_entity).first()
                form=CommonAddDepartmentForm(main_sbscrbr_entity,request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =usr
                    if account is None:
                        obj.save()

                        return redirect('allifmaalcommonapp:commonDepartments',allifusr=usrslg,allifslug=user_var)
                    else:
                        error_message="Sorry, a similar department description exists!!!"
                        allifcontext={"error_message":error_message,}
                        return render(request,'allifmaalcommonapp/error/error.html',allifcontext)

                else:
                    context = {
                        "title": title,
                        "form": form, # form with errors.
                    }
                    return render(request, 'allifmaalcommonapp/departments/add-department.html', context)
                    
                    form=CommonAddDepartmentForm(main_sbscrbr_entity)
                    print("invalid form")
            else:
                form=CommonAddDepartmentForm(main_sbscrbr_entity)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint') 
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/departments/add-department.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit 
def commonEditDepartment(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Department Details"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        user_var_update=CommonDepartmentsModel.objects.filter(id=pk).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        form=CommonAddDepartmentForm(main_sbscrbr_entity,instance=user_var_update)
        if request.method=='POST':
            form=CommonAddDepartmentForm(main_sbscrbr_entity,request.POST or None, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                obj.save()
                return redirect('allifmaalcommonapp:commonDepartments',allifusr=usrslg,allifslug=user_var)
        else:
            form=CommonAddDepartmentForm(main_sbscrbr_entity,instance=user_var_update)

        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/departments/add-department.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonDepartmentDetails(request,allifslug,*allifargs,**allifkwargs):
    try:
        title="Department Details"
        user_var=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        allifquery=CommonDepartmentsModel.objects.filter(pk=allifslug).first()
        relatedqueryset=CommonBanksModel.objects.filter(department=allifquery)
        context={
            "allifquery":allifquery,
            "title":title,
            "relatedqueryset":relatedqueryset,
        }
        return render(request,'allifmaalcommonapp/departments/department-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_is_admin
@logged_in_user_is_admin 
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete  
@logged_in_user_is_admin
def commonDeleteDepartment(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonDepartmentsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonDepartments',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

##########################3 company scope ######################################
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_add 
def commonAddCompanyScope(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        title="Scopes"
        form=CommonAddCompanyScopeForm()
        allifqueryset=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
       
        add_item= None
        if request.method == 'POST':
            form=CommonAddCompanyScopeForm(request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.company=main_sbscrbr_entity
                add_item.owner=user_var
                add_item.save()
        context={
    
                "form":form,
                "title":title,
                "allifqueryset":allifqueryset,
              
        }
        return render(request,'allifmaalcommonapp/scopes/scopes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit 
def commonEditCompanyScope(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Scope"
        user_var=request.user.usercompany
        user=request.user
        usrslg=request.user.customurlslug
        user_var_update=CommonCompanyScopeModel.objects.filter(pk=pk).first()
       
        form=CommonAddCompanyScopeForm(instance=user_var_update)
        if request.method=='POST':
            form=CommonAddCompanyScopeForm(request.POST or None,request.FILES, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user
                obj.save()
                return redirect('allifmaalcommonapp:commonAddCompanyScope',allifusr=usrslg,allifslug=user_var)
                
            else:
                form=CommonAddCompanyScopeForm(request.POST or None, instance=user_var_update)
        else:
            form=CommonAddCompanyScopeForm(request.POST or None, instance=user_var_update)
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/scopes/scopes.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete
def commonDeleteCompanyScope(request,pk,*allifargs,**allifkwargs):
    try:
        CommonCompanyScopeModel.objects.filter(pk=pk).first().delete()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        return redirect('allifmaalcommonapp:commonAddCompanyScope',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')  
@logged_in_user_is_admin
@logged_in_user_can_delete
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
#################################...HRM....... System users ..........#####################################
@login_required(login_url='allifmaalusersapp:userLoginPage')
  
def commonhrm(request,*allifargs,**allifkwargs):
    try:
        title="Human Resources Management"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        if  main_sbscrbr_entity!=None:
            allifqueryset=User.objects.filter(usercompany=main_sbscrbr_entity.companyslug)
            if request.method=='POST':
                selected_option=request.POST.get('requiredformat')
                if selected_option=="ascending":
                    allifqueryset=User.objects.filter(usercompany=main_sbscrbr_entity.companyslug).order_by('-first_name')
                else:
                    allifqueryset=User.objects.filter(usercompany=main_sbscrbr_entity.companyslug)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
      
        context={
            "title":title,
             "allifqueryset":allifqueryset,
             "formats":formats,
             "datasorts":datasorts,
           
            "main_sbscrbr_entity":main_sbscrbr_entity,
            } 
        return render(request,'allifmaalcommonapp/hrm/staff/staff.html',context)
                    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_add
@logged_in_user_is_admin
def commonAddUser(request,allifusr,allifslug,*allifargs,**allifkwargs):#this is where a new user is added by the subscriber admin.
    try:
        title="New Staff User Registeration"
        user_var=request.user
        compslg=user_var.usercompany # this gives the slug of the company that the logged in user belongs to.
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        
        form=CreateNewCustomUserForm()
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                fname=request.POST.get('first_name')
                lname=request.POST.get('last_name')
                email=request.POST.get('email')
                form=CreateNewCustomUserForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.usercompany=main_sbscrbr_entity.companyslug
                    obj.fullNames=str(f'{fname}+{lname}')#important...used to generate user slug
                    obj.save()
                    newUser=User.objects.filter(email=email).first()
                    if newUser!=None:
                        secret_key=newUser.customurlslug
                        context={"title":title,"form":form,"secret_key":secret_key,}
                        return render(request,"allifmaalcommonapp/hrm/users/userkey.html",context)
                    
                    else:
                        messages.info(request,f'User does not exist')
                        return redirect('allifmaalusersapp:newUserRegistration')
                else:
                    messages.info(request,f'Sorry {email} is likely taken, or passwords not match')

        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
           
        
        context={"title":title,"form":form,}
        return render(request,"allifmaalcommonapp/hrm/users/adduser.html",context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
def commonUserDetails(request,pk,*allifargs,**allifkwargs):
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
        return render(request,'allifmaalcommonapp/hrm/users/user-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
def commonLoggedInUserDetails(request,*allifargs,**allifkwargs):
    try:
        title="User Details"
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
def commonShowClickedRowUserDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="User Details"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if  main_sbscrbr_entity!=None:# if true, it means that company exists and logged user is owner 
            allifqueryset=User.objects.filter(usercompany=main_sbscrbr_entity.companyslug)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
        
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        clicked_row_data=User.objects.filter(id=pk).first()
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
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit

def commonEditUser(request,pk,*allifargs,**allifkwargs):
    try:
        user_var_update=User.objects.filter(id=pk).first()
        title="Update User Details"
        form=UpdateCustomUserForm(instance=user_var_update)
        usrcmpny=user_var_update.usercompany
        print(user_var_update)
        if request.method=='POST':
            form=UpdateCustomUserForm(request.POST or None, instance=user_var_update)
            email=request.POST.get('email')
            if form.is_valid():
                obj = form.save(commit=False)
                obj.usercompany=usrcmpny
                obj.save()
                newUser=User.objects.filter(email=email).first()
                if newUser!=None:
                    secret_key=newUser.customurlslug
                    context={"title":title,"form":form,"secret_key":secret_key,}
                    return render(request,"allifmaalcommonapp/hrm/users/userkey.html",context)
                else:
                    messages.info(request,f'User does not exist')
                    return redirect('allifmaalusersapp:newUserRegistration')
            else:
                messages.info(request,f'Sorry {email} is likely taken, or passwords not match')
        else:
            form=UpdateCustomUserForm(instance=user_var_update)

        context={"title":title,"form":form,}
        return render(request,"allifmaalcommonapp/hrm/users/adduser.html",context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete
@logged_in_user_is_admin   
def commonDeleteUser(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        User.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonhrm',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonUserSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=User.objects.filter((Q(first_name__icontains=allifsearch)|Q(last_name__icontains=allifsearch)) & Q(usercompany=compslg))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/hrm/staff/staff.html',context)
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@login_required(login_url='allifmaalusersapp:userLoginPage')
def commonUserCanAddEditViewDelete(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=User.objects.filter(id=pk).first()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
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
       
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)
       
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
@login_required(login_url='allifmaalusersapp:userLoginPage') 
def commonUserCanAdd(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=User.objects.filter(id=pk).first()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        if allifquery.can_add==True:
            allifquery.can_add=False
        else:
            allifquery.can_add=True
        allifquery.can_do_all=False
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
def commonUserCanView(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=User.objects.filter(id=pk).first()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        if allifquery.can_view==True:
            allifquery.can_view=False
        else:
            allifquery.can_view=True
        allifquery.can_do_all=False
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
def commonUserCanEdit(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=User.objects.filter(id=pk).first()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        if allifquery.can_edit==True:
            allifquery.can_edit=False
        else:
            allifquery.can_edit=True
        allifquery.can_do_all=False
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)
   
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
def commonUserCanDelete(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=User.objects.filter(id=pk).first()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        if allifquery.can_delete==True:
            allifquery.can_delete=False
        else:
            allifquery.can_delete=True
        allifquery.can_do_all=False 
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#####################3  access control for entities and sub entities
@login_required(login_url='allifmaalusersapp:userLoginPage') 
def commonUserCanAccessAll(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=User.objects.filter(id=pk).first()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        if allifquery.can_access_all==True:
            allifquery.can_access_all=False
        else:
            allifquery.can_access_all=True
        allifquery.save()
        
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
def commonUserCanAccessRelated(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=User.objects.filter(id=pk).first()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        if allifquery.can_access_related==True:
            allifquery.can_access_related=False
        else:
            allifquery.can_access_related=True
        allifquery.save()
        return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
def commonUserAllifaamlAdmin(request,pk):
    try:
        allifquery=User.objects.filter(id=pk).first()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        user=request.user.is_superuser
        
        if user==True:
            if allifquery.allifmaal_admin==True:
                allifquery.allifmaal_admin=False
            else:
                allifquery.allifmaal_admin=True
            allifquery.save()
            return redirect('allifmaalcommonapp:commonUserDetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)
        else:
            return render(request,'allifmaalcommonapp/error/error.html',error_context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


###################### staff profiles #####################################
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view   
def commonStaffProfiles(request,*allifargs,**allifkwargs):
    try:
        title="Staff Profiles"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if  main_sbscrbr_entity!=None:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonEmployeesModel.objects.filter(company=main_sbscrbr_entity)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
           
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            } 
        return render(request,'allifmaalcommonapp/hrm/profiles/profiles.html',context)
                    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_add
def commonAddStaffProfile(request,allifusr,allifslug,*allifargs,**allifkwargs): # when someone logs in, they are directed to this page to create company details.
    try:
        title="Create Staff Profile"
        user_var=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
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
            form=CommonAddStaffProfileForm(instance=main_sbscrbr_entity)
            
            if request.method=='POST':
                form=CommonAddStaffProfileForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.save()
                    user_var=request.user.usercompany
                    usrslg=request.user.customurlslug
                    return redirect('allifmaalcommonapp:commonStaffProfiles',allifusr=usrslg,allifslug=user_var)
                   
                else:
                    error_message=form.errors
                    allifcontext={"error_message":error_message,"title":title,}
                    return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
                    
            else:
                form=CommonAddStaffProfileForm(instance=main_sbscrbr_entity)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
            
           
        context={
            "title":title,
            "form":form,
            }
        return render(request,'allifmaalcommonapp/hrm/profiles/add-staff-profile.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit
def commonEditStaffProfile(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Staff Profile Details"
        user_var=request.user.usercompany
        updateItem= CommonEmployeesModel.objects.filter(id=pk).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        #form =CommonAddStaffProfileForm(instance=updateItem)#insert the content of the table stored in the selected id in the update form
        #we could have used the add customer form but the validation will refuse us to update since fields may exist
    
        if  main_sbscrbr_entity!=None:
            class CommonAddStaffProfileForm(forms.ModelForm):
                class Meta:
                    model = CommonEmployeesModel
                    fields = ['staffNo','firstName','division','branch','lastName','middleName','gender','department','title','education',
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
            form=CommonAddStaffProfileForm(instance=updateItem)
            
            if request.method=='POST':
                form=CommonAddStaffProfileForm(request.POST,instance=updateItem)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.save()
                    user_var=request.user.usercompany
                    usrslg=request.user.customurlslug
                    return redirect('allifmaalcommonapp:commonStaffProfiles',allifusr=usrslg,allifslug=user_var)
                    
                else:
                    form=CommonAddStaffProfileForm(instance=main_sbscrbr_entity)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
           
        context={
            "title":title,
            "form":form,
            }
        return render(request,'allifmaalcommonapp/hrm/profiles/add-staff-profile.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
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
@login_required(login_url='allifmaalusersapp:userLoginPage')  
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete  
def commonDeleteProfile(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonEmployeesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonStaffProfiles',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
def commonProfileSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
       
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonEmployeesModel.objects.filter((Q(firstName__icontains=allifsearch)|Q(lastName__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
            print(searched_data)
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/hrm/profiles/profiles.html',context)
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

###################333 tax parameters settings ###############
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_add
def commonTaxParameters(request,*allifargs,**allifkwargs):
    try:
        title="Applicable Tax Details"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonTaxParametersModel.objects.filter(company=main_sbscrbr_entity)
        latest=CommonTaxParametersModel.objects.filter(company=main_sbscrbr_entity).order_by('-date')[:3]
        form=CommonAddTaxParameterForm(request.POST)
        if request.method == 'POST':
            form=CommonAddTaxParameterForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.company=main_sbscrbr_entity
                obj.owner=user_var
                obj.save()
                return redirect('allifmaalcommonapp:commonTaxParameters',allifusr=user_var,allifslug=compslg)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonAddTaxParameterForm()
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


@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_add
def CommonUpdateTaxDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Tax Details"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonTaxParametersModel.objects.filter(company=main_sbscrbr_entity)
        update=CommonTaxParametersModel.objects.get(id=pk)
        form =CommonAddTaxParameterForm(instance=update)
        if request.method == 'POST':
            form = CommonAddTaxParameterForm(request.POST,instance=update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.company =main_sbscrbr_entity
                obj.owner=user_var
                obj.save()
                return redirect('allifmaalcommonapp:commonTaxParameters',allifusr=user_var,allifslug=compslg)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form =CommonAddTaxParameterForm(instance=update)
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
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_delete 
def commonWantToDeleteTaxParameter(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonTaxParametersModel.objects.filter(company=main_sbscrbr_entity)
        form=CommonAddTaxParameterForm(request.POST)
       
        allifquerydelete=CommonTaxParametersModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquerydelete":allifquerydelete,
        "title":title,
        "allifqueryset":allifqueryset,
        "form":form,
        }
        return render(request,'allifmaalcommonapp/taxes/taxes.html',context)
        return render(request,'allifmaalcommonapp/hrm/profiles/profile-delete-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete
def CommonDeleteTaxParameter(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user
        compslg=user_var.usercompany
        CommonTaxParametersModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonTaxParameters',allifusr=user_var,allifslug=compslg)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
################################# ACCOUNTS  #############################
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_is_admin
def commonGeneralLedgers(request,allifusr,allifslug,*allifargs,**allifkwargs):
    try:
        title="General Ledger Accounts"
        #mysession=Session.objects.get(pk='mxrrjr4vniy08mhpnesjjo5y79kds5ts')
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html')
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonGeneralLedgersModel.objects.filter(company=main_sbscrbr_entity)
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonGeneralLedgersModel.objects.filter(company=main_sbscrbr_entity,division=logged_user_division,branch=logged_user_branch,department=logged_user_department)
       
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/accounts/genledgers.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_add
@logged_in_user_is_admin
def commonAddGeneralLedger(request,allifusr,allifslug,*allifargs,**allifkwargs):
    try:
        title="New General Ledger Account"
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        
        form=CommonAddGeneralLedgerForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                descrp=request.POST.get('description')
                deprtmnt=request.POST.get('department')
                #account=CommonGeneralLedgersModel.objects.filter(description=descrp,company=main_sbscrbr_entity,division=logged_user_division,branch=logged_user_branch,department=logged_user_department).first()
                CommonDepartmentsModel.objects.filter(id=deprtmnt,company=main_sbscrbr_entity).first()
                account=CommonGeneralLedgersModel.objects.filter(description=descrp,department=deprtmnt,company=main_sbscrbr_entity).first()
                
                form=CommonAddGeneralLedgerForm(main_sbscrbr_entity,request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company=main_sbscrbr_entity
                    obj.owner=logged_user
                    if account is None:
                        obj.save()
                        return redirect('allifmaalcommonapp:commonGeneralLedgers',allifusr=usrslg,allifslug=user_cmpny_slug)
                    else:
                        error_message="Sorry, a similar account description exists!!!"
                        allifcontext={"error_message":error_message,
                                    "form":form,
                                    "title":title,}
                        return render(request,'allifmaalcommonapp/accounts/add-gl.html',allifcontext)
                        
                else:
                    form=CommonAddGeneralLedgerForm(main_sbscrbr_entity)
            else:
                form=CommonAddGeneralLedgerForm(main_sbscrbr_entity)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint') 
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/accounts/add-gl.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit
@logged_in_user_is_admin
def commonEditGeneralLedger(request,allifusr,pk,*allifargs,**allifkwargs):
    try:
        title="Update General Ledger Account Details"
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
       
        user_var_update=CommonGeneralLedgersModel.objects.filter(id=pk).first()
        form=CommonAddGeneralLedgerForm(main_sbscrbr_entity,instance=user_var_update)
        if request.method=='POST':
            descrp=request.POST.get('description')
            deprtmnt=request.POST.get('department')
            #account=CommonGeneralLedgersModel.objects.filter(description=descrp,company=main_sbscrbr_entity,division=logged_user_division,branch=logged_user_branch,department=logged_user_department).first()
            CommonDepartmentsModel.objects.filter(id=deprtmnt,company=main_sbscrbr_entity).first()
            account=CommonGeneralLedgersModel.objects.filter(description=descrp,department=deprtmnt,company=main_sbscrbr_entity).first()
                
            form=CommonAddGeneralLedgerForm(main_sbscrbr_entity,request.POST or None, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                if account is None:
                    obj.save()
                    return redirect('allifmaalcommonapp:commonGeneralLedgers',allifusr=usrslg,allifslug=usrslg)
                else:
                    error_message="Sorry, a similar account description exists!!!"
                    allifcontext={"error_message":error_message,
                        "form":form,
                        "title":title,}
                    return render(request,'allifmaalcommonapp/accounts/add-gl.html',allifcontext)
        else:
            form=CommonAddGeneralLedgerForm(main_sbscrbr_entity,instance=user_var_update)

        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/accounts/add-gl.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
@logged_in_user_is_admin
def commonGeneralLedgerDetails(request,allifslug,*allifargs,**allifkwargs):
    try:
        title="Account Details"
        user_cmpny_slug=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        allifquery=CommonGeneralLedgersModel.objects.filter(pk=allifslug).first()
        allifqueryset=CommonChartofAccountsModel.objects.filter(category=allifquery,company=main_sbscrbr_entity)
        context={
            "allifquery":allifquery,
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/accounts/gl-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
@logged_in_user_is_admin
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete 
@logged_in_user_is_admin 
def commonDeleteGeneralLedger(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonGeneralLedgersModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonGeneralLedgers',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_is_admin
def commonSynchGLAccount(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        if  main_sbscrbr_entity!=None:
            allifquery=CommonGeneralLedgersModel.objects.filter(id=pk,company=main_sbscrbr_entity).first()
            related_coa_accs=CommonChartofAccountsModel.objects.filter(category=allifquery,company=main_sbscrbr_entity)
            acc_balance=0
            for items in related_coa_accs:
                acc_balance+=items.balance
            acc_total=acc_balance
            allifquery.balance=acc_total
            allifquery.save()
            return redirect('allifmaalcommonapp:commonGeneralLedgers',allifusr=usrslg,allifslug=user_var)
           
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint') 
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

####################### chart of accounts ########################
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_is_admin
@logged_in_user_can_view
def commonChartofAccounts(request,*allifargs,**allifkwargs):
    try:
        
        title="Chart of Accounts"
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
        
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        form=CommonFilterCOAForm(main_sbscrbr_entity)
        allifqueryset=CommonChartofAccountsModel.objects.filter(company=main_sbscrbr_entity).order_by("code")

        assets_tot_val=CommonChartofAccountsModel.objects.filter(code__lte=19999 or 0,company=main_sbscrbr_entity).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        liablts_tot_val=CommonChartofAccountsModel.objects.filter(code__gt=19999 or 0,code__lte=29999 or 0,company=main_sbscrbr_entity).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        creditors_total_balance=CommonSuppliersModel.objects.filter(balance__gt=2,company=main_sbscrbr_entity).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        equity_tot_val=CommonChartofAccountsModel.objects.filter(code__gt=29999 or 0,code__lte=39999 or 0,company=main_sbscrbr_entity).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        sum_liablts_and_equity=Decimal(liablts_tot_val or 0)+Decimal(equity_tot_val or 0)+Decimal(creditors_total_balance or 0)

        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonChartofAccountsModel.objects.filter(company=main_sbscrbr_entity).order_by("code")
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonChartofAccountsModel.objects.filter(company=main_sbscrbr_entity,division=logged_user_division,branch=logged_user_branch,department=logged_user_department)
       
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                allifqueryset=CommonChartofAccountsModel.objects.filter(company=main_sbscrbr_entity).order_by('-balance')
            else:
                allifqueryset=CommonChartofAccountsModel.objects.filter(company=main_sbscrbr_entity)
        
        
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

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_is_admin
@logged_in_user_can_add
def commonAddChartofAccount(request,*allifargs,**allifkwargs):
    try:
        title="Add New Account"
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        form=CommonAddChartofAccountForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                code=request.POST.get('code')
                descrp=request.POST.get('description')
                deprtmnt=request.POST.get('department')
                account=CommonChartofAccountsModel.objects.filter(code=code,description=descrp,company=main_sbscrbr_entity,department=deprtmnt).first()
                form=CommonAddChartofAccountForm(main_sbscrbr_entity, request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =logged_user
                    if account is None:
                        obj.save()
                        return redirect('allifmaalcommonapp:commonChartofAccounts',allifusr=usrslg,allifslug=user_cmpny_slug)
                    else:
                        error_message="Sorry, a similar account description exists!!!"
                        allifcontext={"error_message":error_message,
                                    "form":form,
                                    "title":title,}
                        return render(request,'allifmaalcommonapp/accounts/add-coa.html',allifcontext)
                
                        
                       
                else:
                    form=CommonAddChartofAccountForm(main_sbscrbr_entity, request.POST)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/accounts/add-coa.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_is_admin
def commonChartofAccountSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonChartofAccountsModel.objects.filter((Q(description__icontains=allifsearch)|Q(code__icontains=allifsearch)|Q(category__description__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/accounts/chart-of-accs.html',context)
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_is_admin
@logged_in_user_can_edit 
def commonEditChartofAccount(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Account Details"
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
       
        user_var_update=CommonChartofAccountsModel.objects.filter(id=pk).first()
        
        querydept=user_var_update.department
        
        form=CommonAddChartofAccountForm(main_sbscrbr_entity,instance=user_var_update)
        if request.method=='POST':
            descrp=request.POST.get('description')
            code=request.POST.get('code')
            deprtmnt=request.POST.get('department')
            account=CommonChartofAccountsModel.objects.filter(code=code,description=descrp,department=deprtmnt,company=main_sbscrbr_entity).first()
            dept=CommonDepartmentsModel.objects.filter(id=deprtmnt).first()
            
            form=CommonAddChartofAccountForm(main_sbscrbr_entity,request.POST or None, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                if account is None:
                   
                    obj.save()
                    return redirect('allifmaalcommonapp:commonChartofAccounts',allifusr=usrslg,allifslug=usrslg)
                    
                else:
                    if deprtmnt==querydept.id:
                       
                        error_message="Sorry, a similar account description exists!!!"
                        allifcontext={"error_message":error_message,
                            "form":form,
                            "title":title,}
                        return render(request,'allifmaalcommonapp/accounts/add-coa.html',allifcontext)
                    else:
                        if int(deprtmnt)==int(querydept.id):
                            obj.save()
                            return redirect('allifmaalcommonapp:commonChartofAccounts',allifusr=usrslg,allifslug=usrslg)
                        else:
                            print(f"not equal {deprtmnt} {querydept.id}")
                            error_message="Sorry, a similar account description exists!!!"
                            allifcontext={"error_message":error_message,
                                "form":form,
                                "title":title,}
                            return render(request,'allifmaalcommonapp/accounts/add-coa.html',allifcontext)
                
           
                
            else:
                form=CommonAddChartofAccountForm(main_sbscrbr_entity,instance=user_var_update)
        else:
            form=CommonAddChartofAccountForm(main_sbscrbr_entity,instance=user_var_update)
        
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/accounts/add-coa.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_is_admin
@logged_in_user_can_view
def commonChartofAccountDetails(request,allifslug,*allifargs,**allifkwargs):
    try:
        title="Account Details"
        allifquery=CommonChartofAccountsModel.objects.filter(pk=allifslug).first()
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/accounts/coa-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_is_admin
@logged_in_user_can_delete  
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_is_admin
@logged_in_user_can_delete  
def commonDeleteChartofAccount(request,pk,*allifargs,**allifkwargs):
    try:
        usrslg=request.user.customurlslug
        user_var=request.user.usercompany
        CommonChartofAccountsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonChartofAccounts',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonSelectedRelatedAccs(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        if  main_sbscrbr_entity!=None:
            if request.method=="GET":
                selectedoption=request.GET.get('allifidforselecteditem')
                selectedcategoryid=CommonGeneralLedgersModel.objects.filter(pk=selectedoption,company=main_sbscrbr_entity).first()
                catid=selectedcategoryid.id
                #catdescrip=selectedcategoryid.description
                allifquery=CommonChartofAccountsModel.objects.filter(category=catid,company=main_sbscrbr_entity)#this is a queryset that will be sent to the backend.
                allifqueryrelatedlist=list(CommonChartofAccountsModel.objects.filter(category=catid,company=main_sbscrbr_entity))#this is a list
                serialized_data = serialize("json", allifqueryrelatedlist)
                myjsondata= json.loads(serialized_data)
                allifqueryset=list(CommonChartofAccountsModel.objects.filter(category=catid,company=main_sbscrbr_entity).values("category","description","id","code","balance"))
                allifrelatedserlized= json.loads(serialize('json', allifquery))#this is a list
                mystringjsondata=json.dumps(allifrelatedserlized)#this is string
                return JsonResponse(allifqueryset,safe=False)
            else:
                pass
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonClearAcc(request,pk,*allifargs,**allifkwargs):
    try:
        usrslg=request.user.customurlslug
        user_var=request.user.usercompany
        acc=CommonChartofAccountsModel.objects.filter(id=pk).first()
        acc.balance=0
        acc.save()
        return redirect('allifmaalcommonapp:commonChartofAccounts',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonChartofAccAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        allifqueryset=CommonCompanyDetailsModel.objects.all()
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
        allifqueryset=CommonChartofAccountsModel.objects.filter(company=main_sbscrbr_entity).order_by("code")
        
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_value=request.POST.get('startvalue')
            end_value=request.POST.get('endvalue')
            if start_value!="" and end_value!="":
                searched_data=CommonChartofAccountsModel.objects.filter(Q(balance__gte=start_value)& Q(balance__lte=end_value)& Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/accounts/coa-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
                    "scopes":scopes
                    }
                    response = HttpResponse(content_type='application/doc')
                    response = HttpResponse(content_type='application/pdf') # this opens on the same page
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
                elif selected_option=="excel":
                    compnyresource= commonCompanyResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    "formats":formats,
                    "title":title,
                     "scopes":scopes
                    }
                    return render(request,'allifmaalcommonapp/accounts/chart-of-accs.html',context)
                    
            else:
                allifqueryset=CommonCompanyDetailsModel.objects.all()
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
             "scopes":scopes
            }
            return render(request,'allifmaalcommonapp/companies/companies.html',context)
        
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
             "scopes":scopes
            }
            return render(request,'allifmaalcommonapp/companies/companies.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

############################### EMAILS AND SMS ####################

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonEmailsAndSMS(request,*allifargs,**allifkwargs):
    try:
        title="Emails and SMSs"
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=CommonEmailsModel.objects.filter(company=main_sbscrbr_entity)
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonEmailsModel.objects.filter(company=main_sbscrbr_entity)
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonEmailsModel.objects.filter(company=main_sbscrbr_entity,division=logged_user_division,branch=logged_user_branch,department=logged_user_department)
        ################## Sending an Email ###########################################
        ahmed='info@allifmaal.com'
        muse='allifmaalengineering@gmail.com'
        subject = title
        message = f'Thank you for creating an account!'
        email_sender=logged_user.email #'ahmedmusadir@gmail.com'
        recipient_list = [ahmed,muse]
        send_mail(subject, message, email_sender, recipient_list)# uncomment to send emails.
        email=CommonEmailsModel(subject=subject,message=message,recipient=recipient_list,sender=email_sender,company=main_sbscrbr_entity,division=logged_user_division,branch=logged_user_branch,department=logged_user_department)
        #email.save()

        ################3 this below is for the SMS... this worked ###################
        account_sid = "ACb19b2a5701ec5f53c38e113ae9595917" # Twilio account
        auth_token  = "143c2731b15d0a8a9a918db838ac048a"  # Twilio Token
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        to="+252610993964",# number registered with Twilio
        from_="+17753731268",#virtual number from Twilio
        body="Testing Message Here") # message to be sent.

    
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
            
        }
        return render(request,'allifmaalcommonapp/comms/emailsms.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_is_admin
@logged_in_user_can_delete  
def commonDeleteEmail(request,pk,*allifargs,**allifkwargs):
    try:
        usrslg=request.user.customurlslug
        user_var=request.user.usercompany
        CommonEmailsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonEmailsAndSMS',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
#################################### BANKS SECTION #############################
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonBanks(request,*allifargs,**allifkwargs):
    try:
        title="Banks"
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=CommonBanksModel.objects.filter(company=main_sbscrbr_entity)
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonBanksModel.objects.filter(company=main_sbscrbr_entity)
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonBanksModel.objects.filter(company=main_sbscrbr_entity,division=logged_user_division,branch=logged_user_branch,department=logged_user_department)
        
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/banks/banks.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_add
def commonAddBank(request,allifusr,allifslug,*allifargs,**allifkwargs):
    try:
        title="Add New Bank "
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        usr=request.user
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        form=CommonAddBankForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                descrp=request.POST.get('name')
                deptmnt=request.POST.get('department')
                account=CommonBanksModel.objects.filter(name=descrp,company=main_sbscrbr_entity,department=deptmnt).first()
                form=CommonAddBankForm(main_sbscrbr_entity,request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =usr
                    if account is None:
                        obj.save()

                        return redirect('allifmaalcommonapp:commonBanks',allifusr=usrslg,allifslug=user_var)
                    else:
                        error_message="Sorry, a similar description exists!!!"
                        allifcontext={"error_message":error_message,"form":form,}
                        return render(request,'allifmaalcommonapp/banks/add-bank.html',allifcontext)
                        

                else:
                    form=CommonAddBankForm(main_sbscrbr_entity)
            else:
                form=CommonAddBankForm(main_sbscrbr_entity)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint') 
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/banks/add-bank.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_edit
def commonEditBank(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Bank Details"
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        allifquery_update=CommonBanksModel.objects.filter(id=pk).first()
        form=CommonAddBankForm(main_sbscrbr_entity,instance=allifquery_update)
        
        if request.method=='POST':
            descrp=request.POST.get('name')
            deprtmnt=request.POST.get('department')
            account=CommonBanksModel.objects.filter(name=descrp,department=deprtmnt,company=main_sbscrbr_entity).first()
            form=CommonAddBankForm(main_sbscrbr_entity,request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=logged_user
                if account is None:
                    obj.save()
                    return redirect('allifmaalcommonapp:commonBanks',allifusr=usrslg,allifslug=usrslg)
                    
                else:
                    if int(account.id)!=int(allifquery_update.id):
                       
                        error_message="Sorry, a similar description exists!!!"
                        allifcontext={"error_message":error_message,
                            "form":form,
                            "title":title,}
                        return render(request,'allifmaalcommonapp/banks/add-bank.html',allifcontext)
                    else:
                        obj.save()
                        return redirect('allifmaalcommonapp:commonBanks',allifusr=usrslg,allifslug=usrslg)
        else:
            form=CommonAddBankForm(main_sbscrbr_entity,instance=allifquery_update)

        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/banks/add-bank.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonBankDetails(request,allifslug,*allifargs,**allifkwargs):
    try:
        title="Bank Details"
        user_var=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        allifquery=CommonBanksModel.objects.filter(pk=allifslug).first()
        allifqueryset=CommonBankWithdrawalsModel.objects.filter(bank=allifquery,company=main_sbscrbr_entity)
        queryset=CommonBankWithdrawalsModel.objects.filter(bank=allifquery,company=main_sbscrbr_entity)
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete  
def commonDeleteBank(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonBanksModel.objects.filter(pk=pk).first().delete()
        return redirect('allifmaalcommonapp:commonBanks',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonBankSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonBanksModel.objects.filter((Q(name__icontains=allifsearch)|Q(account__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/banks/banks.html',context)
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
############################################### BANK DEPOSITS ################################
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_is_admin
def commonBankShareholderDeposits(request,*allifargs,**allifkwargs):
    try:
        title="Bank Deposits"
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=CommonBanksModel.objects.filter(company=main_sbscrbr_entity)
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity)
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity,division=logged_user_division,branch=logged_user_branch,department=logged_user_department)
        
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity).order_by('-amount')
            else:
                allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity)
      
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request,'allifmaalcommonapp/banks/deposits/shareholders/deposits-sh.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonAddBankShareholderDeposit(request,*allifargs,**allifkwargs):
    try:
        title="Add New Bank Deposit"
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=CommonBanksModel.objects.filter(company=main_sbscrbr_entity)
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        form=CommonBankDepositAddForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                bank=request.POST.get('bank')
                amount=request.POST.get('amount')
                chartaccasset=request.POST.get('asset')
                chartacceqty=request.POST.get('equity')
                form=CommonBankDepositAddForm(main_sbscrbr_entity, request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =logged_user
                    obj.save()
                    myquery=CommonBanksModel.objects.filter(id=bank).first()
                    initial_bank_balnce=myquery.balance
                    myquery.balance=initial_bank_balnce+Decimal(amount)
                    myquery.deposit=Decimal(amount)
                    myquery.withdrawal=0
                    myquery.save()

                    ########### increase the asset account
                    query=CommonChartofAccountsModel.objects.filter(id=chartaccasset).first()
                    initial_bank_balnce=query.balance
                    query.balance=initial_bank_balnce+Decimal(amount)
                    query.save()

                    ############ increase equity account ##############
                    eqtyquery=CommonChartofAccountsModel.objects.filter(id=chartacceqty).first()
                    initial_bank_balnce=eqtyquery.balance
                    eqtyquery.balance=initial_bank_balnce+Decimal(amount)
                    eqtyquery.save()

                    return redirect('allifmaalcommonapp:commonBankShareholderDeposits',allifusr=usrslg,allifslug=user_cmpny_slug)
                        
                else:
                    form=CommonBankDepositAddForm(main_sbscrbr_entity)

        context={
            "form":form,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/banks/deposits/shareholders/add-deposit-sh.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
def commonEditBankShareholderDeposit(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        sector=str(main_sbscrbr_entity.sector)
        user_var_update=CommonShareholderBankDepositsModel.objects.filter(id=pk).first()
       
        form=CommonBankDepositAddForm(main_sbscrbr_entity, instance=user_var_update)
       
        title=user_var_update

        if request.method=='POST':
            form=CommonBankDepositAddForm(main_sbscrbr_entity, request.POST, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                #obj.uid=allifuid
                obj.save()
                return redirect('allifmaalcommonapp:commonBankShareholderDeposits',allifusr=usrslg,allifslug=user_var)
               
        context={"title":title,"form":form,"sector":sector,}
        return render(request,'allifmaalcommonapp/banks/deposits/shareholders/add-deposit-sh.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
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
@login_required(login_url='allifmaalusersapp:userLoginPage')  
@logged_in_user_can_view
@logged_in_user_can_delete
@logged_in_user_is_admin
def commonDeleteBankShareholderDeposit(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonShareholderBankDepositsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonBankShareholderDeposits',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonDepositSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonShareholderBankDepositsModel.objects.filter((Q(description__icontains=allifsearch)|Q(amount__icontains=allifsearch)|Q(bank__name__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/banks/deposits/shareholders/deposits-sh.html',context)
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonDepositAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        allifqueryset=CommonCompanyDetailsModel.objects.all()
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
        allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity)
       
        firstDate=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity).order_by('-amount').first().amount
       
        biggestAmount=CommonShareholderBankDepositsModel.objects.aggregate(Max('amount')).values()

        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/banks/deposits/shareholders/deposit-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
                    "scopes":scopes
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
                elif selected_option=="excel":
                    compnyresource=commonBankDepositsResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    "formats":formats,
                    "title":title,
                     "scopes":scopes
                    }
                    return render(request,'allifmaalcommonapp/banks/deposits/shareholders/deposits-sh.html',context)
                   
            else:
                allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity)
                
                
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
             "scopes":scopes
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonClearShareholderDepositSearch(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        return redirect('allifmaalcommonapp:commonBankShareholderDeposits',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
############################################### BANK WITHDRAWALS ################################
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonBankWithdrawals(request,*allifargs,**allifkwargs):
    try:
        title="Bank Withdrawals"
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=CommonBanksModel.objects.filter(company=main_sbscrbr_entity)
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            context={
                "logged_user":logged_user
            }
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonBankWithdrawalsModel.objects.filter(company=main_sbscrbr_entity)
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonBankWithdrawalsModel.objects.filter(company=main_sbscrbr_entity,division=logged_user_division,branch=logged_user_branch,department=logged_user_department)
        
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                allifqueryset=CommonBankWithdrawalsModel.objects.filter(company=main_sbscrbr_entity).order_by('-amount')
            else:
                allifqueryset=CommonBankWithdrawalsModel.objects.filter(company=main_sbscrbr_entity)
        else:
            pass
        
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request,'allifmaalcommonapp/banks/withdrawals/withdrawals.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_add
def commonAddBankWithdrawal(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usr=request.user
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        title="New Withdrawal"
        form=CommonBankWithdrawalsAddForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                bank=request.POST.get('bank')
                amount=request.POST.get('amount')
                chart_account=request.POST.get('asset')
                bankcoa=request.POST.get('bankcoa')
                
                form=CommonBankWithdrawalsAddForm(main_sbscrbr_entity, request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =usr
                    #obj.uid=allifuid
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
                   
                    return redirect('allifmaalcommonapp:commonBankWithdrawals',allifusr=usrslg,allifslug=user_var)

                else:
                    form=CommonBankWithdrawalsAddForm(main_sbscrbr_entity)

        context={
            "form":form,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/banks/withdrawals/add-withdrawal.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonEditBankWithdrawal(request,pk,*allifargs,**allifkwargs):
    try:
        
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        sector=str(main_sbscrbr_entity.sector)
        user_var_update=CommonBankWithdrawalsModel.objects.filter(id=pk).first()
       
        form=CommonBankWithdrawalsAddForm(main_sbscrbr_entity, instance=user_var_update)
       
        title=user_var_update

        if request.method=='POST':
            form=CommonBankWithdrawalsAddForm(main_sbscrbr_entity, request.POST, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                #obj.uid=allifuid
                obj.save()
                return redirect('allifmaalcommonapp:commonBankWithdrawals',allifusr=usrslg,allifslug=user_var)
               
        context={"title":title,"form":form,"sector":sector,}
        return render(request,'allifmaalcommonapp/banks/withdrawals/add-withdrawal.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
@logged_in_user_is_admin
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
@logged_in_user_is_admin
@logged_in_user_can_delete  
def commonDeleteBankWithdrawal(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonBankWithdrawalsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonBankWithdrawals',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonWithdrawalSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonBankWithdrawalsModel.objects.filter((Q(description__icontains=allifsearch)|Q(amount__icontains=allifsearch)|Q(bank__name__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/banks/withdrawals/withdrawals.html',context)
        
            
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonWithdrawalAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        allifqueryset=CommonCompanyDetailsModel.objects.all()
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
        allifqueryset=CommonBankWithdrawalsModel.objects.filter(company=main_sbscrbr_entity)
       
        firstDate=CommonBankWithdrawalsModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonBankWithdrawalsModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonBankWithdrawalsModel.objects.filter(company=main_sbscrbr_entity).order_by('-amount').first().amount
       
        biggestAmount=CommonBankWithdrawalsModel.objects.aggregate(Max('amount')).values()

        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonBankWithdrawalsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/banks/withdrawals/withdrawal-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
                    "scopes":scopes
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
                elif selected_option=="excel":
                    compnyresource=commonBankWithdrawalResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    "formats":formats,
                    "title":title,
                     "scopes":scopes
                    }
                    return render(request,'allifmaalcommonapp/banks/withdrawals/withdrawals.html',context)
                    
            else:
                allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity)
                
                
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

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonClearShareholderWithdrwlSearch(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        return redirect('allifmaalcommonapp:commonBankWithdrawals',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)

##############################33 suppliers section ###############3
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonSuppliers(request,*allifargs,**allifkwargs):
    try:
        title="Suppliers And Vendors"
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()

        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=[]
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonSuppliersModel.objects.filter(company=main_sbscrbr_entity)
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonSuppliersModel.objects.filter(company=main_sbscrbr_entity,division=logged_user_division,branch=logged_user_branch,department=logged_user_department)
        
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                allifqueryset=CommonSuppliersModel.objects.filter(company=main_sbscrbr_entity).order_by('-name')
            else:
                allifqueryset=CommonSuppliersModel.objects.filter(company=main_sbscrbr_entity)
        else:
            pass

       
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonSupplierSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonSuppliersModel.objects.filter((Q(name__icontains=allifsearch)|Q(balance__icontains=allifsearch)|Q(address__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/suppliers/suppliers.html',context)
       
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonClearSupplierSearch(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        return redirect('allifmaalcommonapp:commonSuppliers',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonAddSupplier(request,allifusr,allifslug,*allifargs,**allifkwargs):
    try:
        title="Add New Supplier"
        user_var=request.user.usercompany
        usr=request.user
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()

        form=CommonAddSupplierForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                form=CommonAddSupplierForm(main_sbscrbr_entity,request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =usr
                    obj.save()
                    return redirect('allifmaalcommonapp:commonSuppliers',allifusr=usrslg,allifslug=user_var)
                else:
                    form=CommonAddSupplierForm(main_sbscrbr_entity)
            else:
                form=CommonAddSupplierForm(main_sbscrbr_entity)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/suppliers/add-supplier.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_edit 
def commonEditSupplier(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        title="Update Supplier Details"
        user_var_update=CommonSuppliersModel.objects.filter(id=pk).first()
       
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        form=CommonAddSupplierForm(main_sbscrbr_entity,instance=user_var_update)
        if request.method=='POST':
            form=CommonAddSupplierForm(main_sbscrbr_entity,request.POST or None, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                obj.save()
                return redirect('allifmaalcommonapp:commonSuppliers',allifusr=usrslg,allifslug=user_var)
            else:
                form=CommonAddSupplierForm(main_sbscrbr_entity,instance=user_var_update)
        else:
            form=CommonAddSupplierForm(main_sbscrbr_entity,instance=user_var_update)
           
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/suppliers/add-supplier.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
@logged_in_user_is_admin 
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
@logged_in_user_is_admin 
def commonDeleteSupplier(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonSuppliersModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonSuppliers',allifusr=usrslg,allifslug=user_var)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonSupplierAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonSuppliersModel.objects.filter(company=main_sbscrbr_entity)
        firstDate=CommonSuppliersModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonSuppliersModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonSuppliersModel.objects.filter(company=main_sbscrbr_entity).order_by('-balance').first().balance
    
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonSuppliersModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(balance__gte=start_value or 0) & Q(balance__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/suppliers/supsearchpdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
                    
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
                elif selected_option=="excel":
                    compnyresource=commonBankWithdrawalResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="suppliers.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                     
                    }
                    return render(request,'allifmaalcommonapp/suppliers/suppliers.html',context)
                    
            else:
                allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity)
                
                
            context={
            "allifqueryset":allifqueryset,
            
            "title":title,
             
            }
            return render(request,'allifmaalcommonapp/suppliers/suppliers.html',context)
           
        else:
            context={
            "allifqueryset":allifqueryset,
           
            "title":title,
            
            }
            return render(request,'allifmaalcommonapp/suppliers/suppliers.html',context)
          
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
##################################### EDUCATIONS... ###################
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonForms(request,*allifargs,**allifkwargs):
    try:
        title="Forms And Faculties"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=[]
        if logged_user_profile!=None:
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonFormsModel.objects.filter(company=main_sbscrbr_entity)
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonFormsModel.objects.filter(company=main_sbscrbr_entity,department=logged_user_department)
        

        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/education/forms/forms.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonAddForm(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usr=request.user
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        title="Forms, Faculties Registration"
        form=CommonFormsAddForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                form=CommonFormsAddForm(main_sbscrbr_entity,request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =usr
                    obj.save()
                    return redirect('allifmaalcommonapp:commonForms',allifusr=usrslg,allifslug=user_var)

                else:
                    form=CommonFormsAddForm(main_sbscrbr_entity)
            else:
                    form=CommonFormsAddForm(main_sbscrbr_entity)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
        context={
            "form":form,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/education/forms/add-form.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
   
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit 
def commonEditForm(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        title="Update Forms And Faculties Details"
        user_var_update=CommonFormsModel.objects.filter(id=pk).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        form=CommonFormsAddForm(main_sbscrbr_entity,instance=user_var_update)
        if request.method=='POST':
            form=CommonFormsAddForm(main_sbscrbr_entity,request.POST or None, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                obj.save()
                return redirect('allifmaalcommonapp:commonForms',allifusr=usrslg,allifslug=user_var)
            else:
                form=CommonFormsAddForm(main_sbscrbr_entity,instance=user_var_update)

        else:
            form=CommonFormsAddForm(main_sbscrbr_entity,instance=user_var_update)
            
        
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/education/forms/add-form.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
@logged_in_user_is_admin 
def commonWantToDeleteForm(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonFormsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/education/forms/form-delete-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)       
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
@logged_in_user_is_admin 
@logged_in_user_can_delete 
def commonDeleteForm(request,pk,*allifargs,**allifkwargs):
    try:
        CommonFormsModel.objects.filter(id=pk).first().delete()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        return redirect('allifmaalcommonapp:commonForms',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonFormDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Form/Faculty Details"
        allifquery=CommonFormsModel.objects.filter(id=pk).first()
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/education/forms/forms-details.html',context)
        
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonFormSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonFormsModel.objects.filter((Q(name__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/education/forms/forms.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#######################################3 classes ###############################3
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonClasses(request,*allifargs,**allifkwargs):
    try:
        title="Classes"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=[]
        if logged_user_profile!=None:
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonClassesModel.objects.filter(company=main_sbscrbr_entity)
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonClassesModel.objects.filter(company=main_sbscrbr_entity,department=logged_user_department)
        

        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/education/classes/classes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_add
def commonAddClass(request,*allifargs,**allifkwargs):
    try:
        title="Add New Class"
        user_var=request.user.usercompany
        usr=request.user
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()

        form=CommonClassesAddForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                form=CommonClassesAddForm(main_sbscrbr_entity, request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =usr
                    obj.save()
                    return redirect('allifmaalcommonapp:commonClasses',allifusr=usrslg,allifslug=user_var)

                else:
                    form=CommonClassesAddForm(main_sbscrbr_entity)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')

        context={
            "form":form,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/education/classes/add-class.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
   
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_edit
@logged_in_user_can_view
def commonEditClass(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Class Details"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        user_var_update=CommonClassesModel.objects.filter(id=pk).first()
        form=CommonClassesAddForm(main_sbscrbr_entity, instance=user_var_update)
        if request.method=='POST':
            form=CommonClassesAddForm(main_sbscrbr_entity, request.POST, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=request.user
                obj.company =main_sbscrbr_entity
                obj.save()
                return redirect('allifmaalcommonapp:commonClasses',allifusr=usrslg,allifslug=user_var)
            else:
                form=CommonClassesAddForm(main_sbscrbr_entity, instance=user_var_update)

        else:
            form=CommonClassesAddForm(main_sbscrbr_entity, instance=user_var_update)

        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/education/classes/add-class.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_delete
@logged_in_user_can_view 
def commonDeleteClass(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonClassesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonClasses',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonClassDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Class Details"
        allifquery=CommonClassesModel.objects.filter(id=pk).first()
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/education/classes/class-details.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonClassSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonClassesModel.objects.filter((Q(name__icontains=allifsearch)|Q(comments__icontains=allifsearch)|Q(form__name__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/education/classes/classes.html',context)
        
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
@logged_in_user_is_admin 
def commonWantToDeleteClass(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonClassesModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/education/classes/class-delete-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)       


############################################ CUSTOMERS ######################
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonCustomers(request,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=[]
        if logged_user_profile!=None:
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonCustomersModel.objects.filter(company=main_sbscrbr_entity)
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonCustomersModel.objects.filter(company=main_sbscrbr_entity,department=logged_user_department)
        
        sector=str(main_sbscrbr_entity.sector)
        if sector == "Healthcare":
            title="Registered Patients"
        elif sector=="Education":
            title="Registered Students"
        else:
            title="Registered Customers"

      
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request,'allifmaalcommonapp/customers/customers.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonAddCustomer(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usr=request.user
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        sector=str(main_sbscrbr_entity.sector)

        ###### start... UID generation ##################
        allifquery=CommonCustomersModel.objects.filter(company=main_sbscrbr_entity)
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        currntyear= datetime.date.today().year
        allifuid=str(nmbr)+"/"+str(currntyear)+"/"+str(unque)
        ###### End... UID generation ##################
        
        if sector == "Healthcare":
            title="Patient Registeration"
        elif sector=="Education":
            title="Student Registeration"
        else:
            title="Customer Registeration"
            
        form=CommonCustomerAddForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                form=CommonCustomerAddForm(main_sbscrbr_entity, request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =usr
                    obj.uid=allifuid
                    obj.save()
                    return redirect('allifmaalcommonapp:commonCustomers',allifusr=usrslg,allifslug=user_var)

                else:
                    error_message=form.errors
                    allifcontext={"error_message":error_message,"title":title,}
                    return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
            else:
                    form=CommonCustomerAddForm(main_sbscrbr_entity)
        else:
                return redirect('allifmaalcommonapp:CommonDecisionPoint')
        context={
            "form":form,
            "sector":sector,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/customers/add-customer.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
def commonEditCustomer(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        sector=str(main_sbscrbr_entity.sector)
        user_var_update=CommonCustomersModel.objects.filter(id=pk).first()
        allifuid=user_var_update.uid
        form=CommonCustomerAddForm(main_sbscrbr_entity, instance=user_var_update)
        if sector == "Healthcare":
            title="Update Patient Details"
        elif sector=="Education":
            title="Update Student Details"
        else:
            title="Update Customer Details"

        if request.method=='POST':
            form=CommonCustomerAddForm(main_sbscrbr_entity, request.POST, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                obj.uid=allifuid
                obj.save()
                return redirect('allifmaalcommonapp:commonCustomers',allifusr=usrslg,allifslug=user_var)
            else:
                form=CommonCustomerAddForm(main_sbscrbr_entity, instance=user_var_update)
        else:
                form=CommonCustomerAddForm(main_sbscrbr_entity, instance=user_var_update)

        context={"title":title,"form":form,"sector":sector,}
        return render(request,'allifmaalcommonapp/customers/add-customer.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonCustomerDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonCustomersModel.objects.filter(pk=pk).first()
        user_var=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        sector=str(main_sbscrbr_entity.sector)

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
       
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
@logged_in_user_is_admin 
def commonDeleteCustomer(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonCustomersModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonCustomers',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonCustomerSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonCustomersModel.objects.filter((Q(name__icontains=allifsearch)|Q(balance__icontains=allifsearch)|Q(address__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/customers/customers.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonCustomerAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonSuppliersModel.objects.filter(company=main_sbscrbr_entity)
        firstDate=CommonSuppliersModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonSuppliersModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonCustomersModel.objects.filter(company=main_sbscrbr_entity).order_by('-balance').first().balance
    
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonCustomersModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(balance__gte=start_value or 0) & Q(balance__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/suppliers/supsearchpdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
                    
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
                elif selected_option=="excel":
                    compnyresource=commonBankWithdrawalResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="suppliers.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                     
                    }
                    return render(request,'allifmaalcommonapp/customers/customers.html',context)
                    
            else:
                allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity)
                
                
            context={
            "allifqueryset":allifqueryset,
            
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
@logged_in_user_is_admin 
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonAssetCategories(request,*allifargs,**allifkwargs):
    try:
        title="Asset Categories"
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if  main_sbscrbr_entity!=None:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonAssetCategoriesModel.objects.filter(company=main_sbscrbr_entity)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
           
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/assets/categories.html',context)
        
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonAssetCategorySearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonAssetCategoriesModel.objects.filter((Q(description__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/assets/categories.html',context)
        
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_add
def commonAddAssetCategory(request,*allifargs,**allifkwargs):
    try:
        title="Add New Asset Category"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        usr=request.user
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        form=CommonAddAssetCategoryForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                form=CommonAddAssetCategoryForm(main_sbscrbr_entity,request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =usr
                   
                    obj.save()

                    return redirect('allifmaalcommonapp:commonAssetCategories',allifusr=usrslg,allifslug=user_var)
                else:
                    error_message="Sorry, a similar bank description exists!!!"
                    allifcontext={"error_message":error_message,}
                    return render(request,'allifmaalcommonapp/error/error.html',allifcontext)

            else:
                form=CommonAddAssetCategoryForm(main_sbscrbr_entity)
           
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint') 
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/assets/add-cat.html',context)
        
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonEditAssetCategory(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Asset Category Details"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        user_var_update=CommonAssetCategoriesModel.objects.filter(id=pk).first()
        form=CommonAddAssetCategoryForm(main_sbscrbr_entity,instance=user_var_update)
        if request.method=='POST':
            form=CommonAddAssetCategoryForm(main_sbscrbr_entity,request.POST or None, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                obj.save()
                return redirect('allifmaalcommonapp:commonAssetCategories',allifusr=usrslg,allifslug=user_var)
        else:
            form=CommonAddAssetCategoryForm(main_sbscrbr_entity,instance=user_var_update)

        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/assets/add-cat.html',context)
       
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonAssetCategoryDetails(request,allifslug,*allifargs,**allifkwargs):
    try:
        title="Asset Category Details"
        user_var=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        allifquery=CommonAssetCategoriesModel.objects.filter(pk=allifslug).first()
       
        context={
            "allifquery":allifquery,
            "title":title,
          
        }
        return render(request,'allifmaalcommonapp/assets/cat-details.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
@logged_in_user_is_admin 
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_is_admin
@logged_in_user_can_delete  
def commonDeleteAssetCategory(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonAssetCategoriesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonAssetCategories',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

    ############################ ASSETS ##########################3
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonAssets(request,*allifargs,**allifkwargs):
    try:
        title="Assets"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
       
        if  main_sbscrbr_entity!=None:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonAssetsModel.objects.filter(company=main_sbscrbr_entity)
        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/assets/assets.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonAssetSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonAssetsModel.objects.filter((Q(description__icontains=allifsearch)|Q(supplier__name__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/assets/assets.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonAddAsset(request,*allifargs,**allifkwargs):
    try:
        title="Asset Registration"
        user_var=request.user.usercompany
        usr=request.user
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
    
        form=CommonAssetsAddForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                form=CommonAssetsAddForm(main_sbscrbr_entity, request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =usr
                    #obj.uid=allifuid
                    obj.save()
                    
                   
                    return redirect('allifmaalcommonapp:commonAssets',allifusr=usrslg,allifslug=user_var)
                else:
                    form=CommonAssetsAddForm(main_sbscrbr_entity)
        context={
            "form":form,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/assets/add-asset.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonPostAsset(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        allifquery=CommonAssetsModel.objects.filter(id=pk).first()#very important to get id to go to particular shipment
        supplier_id=allifquery.supplier
        payment_option=allifquery.terms
        asset_value_acc_id=allifquery.asset_account
        cost_value_acc_id=allifquery.cost_account
        asset_total_value=Decimal(allifquery.asset_total_amount)
        asset_posting_status=allifquery.status
        deposit_value=allifquery.deposit
        if asset_posting_status=="waiting":
            if payment_option=="Cash": #.....this is hard-coding the db filter.....#
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
                    return redirect('allifmaalcommonapp:commonAssets',allifusr=usrslg,allifslug=user_var)
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
                    return redirect('allifmaalcommonapp:commonAssets',allifusr=usrslg,allifslug=user_var)
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
                return redirect('allifmaalcommonapp:commonAssets',allifusr=usrslg,allifslug=user_var)
           
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_edit 
def commonEditAsset(request,pk,*allifargs,**allifkwargs):
    try:
        
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        sector=str(main_sbscrbr_entity.sector)
        user_var_update=CommonAssetsModel.objects.filter(id=pk).first()
       
        form=CommonAssetsAddForm(main_sbscrbr_entity, instance=user_var_update)
       
        title=f"Edit {user_var_update} Details"

        if request.method=='POST':
            form=CommonAssetsAddForm(main_sbscrbr_entity, request.POST, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                #obj.uid=allifuid
                obj.save()
                return redirect('allifmaalcommonapp:commonAssets',allifusr=usrslg,allifslug=user_var)
               
        context={"title":title,"form":form,"sector":sector,}
        return render(request,'allifmaalcommonapp/assets/add-asset.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
@logged_in_user_is_admin 
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
@login_required(login_url='allifmaalusersapp:userLoginPage')  
@logged_in_user_is_admin
def commonDeleteAsset(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonAssetsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonAssets',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)



############################3 ASSET DEPRECIATIONS #############3



@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
@logged_in_user_is_admin
def commonDepreciateAsset(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
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
        

            return redirect('allifmaalcommonapp:commonAssetDetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)

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
            return redirect('allifmaalcommonapp:commonAssetDetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    
############################################### EXPENSES ################################
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonExpenses(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        
        title="Expenses"

        if  main_sbscrbr_entity!=None:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonExpensesModel.objects.filter(company=main_sbscrbr_entity)
        else:
            allifqueryset=[]
        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/expenses/expenses.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_add
def commonAddExpense(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usr=request.user
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        title="Expense Registeration"
        form=CommonExpensesAddForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                funding_acc=request.POST.get('funding_account')
                expnse_acc=request.POST.get('expense_account')
                equity_acc=request.POST.get('equity_account')
                amount=request.POST.get('amount')
                form=CommonExpensesAddForm(main_sbscrbr_entity, request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =usr
                    #obj.uid=allifuid
                    obj.save()
                    fndacc=CommonChartofAccountsModel.objects.filter(id=funding_acc).first()
                    init_bal=fndacc.balance
                    fndacc.balance=init_bal-Decimal(amount)
                    fndacc.save()

                    expnacc=CommonChartofAccountsModel.objects.filter(id=expnse_acc).first()
                    init_bal=expnacc.balance
                    expnacc.balance=init_bal+Decimal(amount)
                    expnacc.save()

                    eqtyacc=CommonChartofAccountsModel.objects.filter(id=equity_acc).first()
                    init_bal=eqtyacc.balance
                    eqtyacc.balance=init_bal-Decimal(amount)
                    eqtyacc.save()


                    return redirect('allifmaalcommonapp:commonExpenses',allifusr=usrslg,allifslug=user_var)

                else:
                    form=CommonExpensesAddForm(main_sbscrbr_entity)

        context={
            "form":form,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/expenses/add-expense.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_edit 
def commonEditExpense(request,pk,*allifargs,**allifkwargs):
    try:
        
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        sector=str(main_sbscrbr_entity.sector)
        allifquery=CommonExpensesModel.objects.filter(pk=pk).first()
       
        form=CommonExpensesAddForm(main_sbscrbr_entity, instance=allifquery)
       
        title=allifquery

        if request.method=='POST':
            form=CommonExpensesAddForm(main_sbscrbr_entity, request.POST, instance=allifquery)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=allifquery.owner
                #obj.uid=allifuid
                obj.save()
                return redirect('allifmaalcommonapp:commonExpenses',allifusr=usrslg,allifslug=user_var)
               
        context={"title":title,"form":form,"sector":sector,"allifquery":allifquery,}
        return render(request,'allifmaalcommonapp/expenses/add-expense.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonExpenseDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonExpensesModel.objects.filter(pk=pk).first()
        user_var=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        title="Expense Details"
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/expenses/expense-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_delete  
def commonWantToDeleteExpense(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        allifquery=CommonExpensesModel.objects.filter(id=pk).first()
        message="Are u sure to delete"
        context={
        "message":message,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/expenses/delete-exp-confirm.html',context)

        return redirect('allifmaalcommonapp:commonExpenses',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete
@logged_in_user_is_admin  
def commonDeleteExpense(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        allifquery=CommonExpensesModel.objects.filter(id=pk).first().delete()
        
        return redirect('allifmaalcommonapp:commonExpenses',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonExpenseSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonExpensesModel.objects.filter((Q(description__icontains=allifsearch)|Q(amount__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/expenses/expenses.html',context)
        
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonPostExpense(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
       
        
        #
        payment=CommonExpensesModel.objects.filter(id=pk).first()#very important to get id to go to particular shipment
        myamount=payment.amount#this gives the initial account
        supplier=payment.supplier
        credit_acc=payment.funding_account
        debit_acc=payment.expense_account
        
        if (supplier and myamount)!=None:

            #credit the suppllier account...
            mycust=CommonSuppliersModel.objects.filter(id=supplier.id).first()
            initial_cust_acc_bal=mycust.balance
            mycust.balance= Decimal(initial_cust_acc_bal)-Decimal(myamount)
            mycust.save()

            # credit the company cash account---or the pay from account where the money is paid from
            coa_acc=CommonChartofAccountsModel.objects.filter(id=credit_acc.id).first()
            initial_coa_acc_bal=coa_acc.balance
            #coa_acc.balance= Decimal(initial_coa_acc_bal)-Decimal(myamount)
            #coa_acc.save()

             # debit the expense account since an new expense is incurred... expense account increases.
            coa_acc=CommonChartofAccountsModel.objects.filter(id=debit_acc.id).first()
            initial_coa_acc_bal=coa_acc.balance
            coa_acc.balance= Decimal(initial_coa_acc_bal)+Decimal(myamount)
            coa_acc.save()
            mypayment=CommonExpensesModel.objects.filter(id=pk).first()
            mypayment.status="posted"
            mypayment.save()

            #
            chartaccs_values_list=CommonChartofAccountsModel.objects.all().values_list('description', flat=True)
            if "Equity" in chartaccs_values_list:
                myequityacc=CommonChartofAccountsModel.objects.filter(description="Equity").first()
                initial_equity_bal=myequityacc.balance
                myequityacc.balance=initial_equity_bal-Decimal(myamount)
                myequityacc.save()

            
        else:
            return render(request,'allifmaalapp/error.html')
        return redirect('allifmaalcommonapp:commonExpenses',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
        
   
########################################33 stock ####################3
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonStockCats(request,*allifargs,**allifkwargs):
    try:
        title="Stock and inventory categories"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=[]
        if logged_user_profile!=None:
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonStockCategoriesModel.objects.filter(company=main_sbscrbr_entity)
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonStockCategoriesModel.objects.filter(company=main_sbscrbr_entity,department=logged_user_department)
        
        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/stocks/stock-cats.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_add 
def commonAddStockCat(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usr=request.user
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
    
        title="Stock Category Registration"
            
        form=CommonStockCatAddForm(main_sbscrbr_entity)
        if  main_sbscrbr_entity!=None:
            if request.method=='POST':
                form=CommonStockCatAddForm(main_sbscrbr_entity,request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.company =main_sbscrbr_entity
                    obj.owner =usr
                    obj.save()
                    return redirect('allifmaalcommonapp:commonStockCats',allifusr=usrslg,allifslug=user_var)

                else:
                    form=CommonStockCatAddForm(main_sbscrbr_entity)

        context={
            "form":form,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            "title":title,
            
            }
        return render(request,'allifmaalcommonapp/stocks/add-cat.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
   
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit 
def commonEditStockCat(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Stock Category Details"
        user_var_update=CommonStockCategoriesModel.objects.filter(id=pk).first()
        user_var=request.user.usercompany
        usr=request.user
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        form=CommonStockCatAddForm(main_sbscrbr_entity,instance=user_var_update)
        if request.method=='POST':
            form=CommonStockCatAddForm(main_sbscrbr_entity,request.POST or None, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                obj.save()
                user_var=request.user.usercompany
                usrslg=request.user.customurlslug
                return redirect('allifmaalcommonapp:commonStockCats',allifusr=usrslg,allifslug=user_var)
               
        context={"title":title,"form":form,}
        return render(request,'allifmaalcommonapp/stocks/add-cat.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonStockCategorySearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonStockCategoriesModel.objects.filter((Q(description__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/stocks/stock-cats.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete  
def commonWantToDeleteStockCat(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        allifquery=CommonStockCategoriesModel.objects.filter(id=pk).first()
        message="Are u sure to delete"
        context={
        "message":message,
        "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/stocks/x-stock-cat-cnfrm.html',context)

        
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)   
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_delete
@logged_in_user_is_admin  
def commonDeleteStockCat(request,pk,*allifargs,**allifkwargs):
    try:
        CommonStockCategoriesModel.objects.filter(id=pk).first().delete()
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        return redirect('allifmaalcommonapp:commonStockCats',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view 
def commonStockCategoryDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonStockCategoriesModel.objects.filter(pk=pk).first()
       
        title=allifquery

        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/stocks/stock-cat-details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
################### inventory/stock###########3
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonStocks(request,*allifargs,**allifkwargs):
    try:
        title="Stock And Inventory"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=[]
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        if logged_user_profile!=None:
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonStocksModel.objects.filter(company=main_sbscrbr_entity)
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonStocksModel.objects.filter(company=main_sbscrbr_entity,department=logged_user_department)
        
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                allifqueryset=CommonStocksModel.objects.filter(company=main_sbscrbr_entity).order_by('-quantity')
            else:
                allifqueryset=CommonStocksModel.objects.filter(company=main_sbscrbr_entity)
        else:
            pass
        context={
            "title":title,
            "allifqueryset":allifqueryset,
            "formats":formats,
            "datasorts":datasorts,
        }
        return render(request,'allifmaalcommonapp/stocks/stocks.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaaladminapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_add
def commonAddStockItem(request,*allifargs,**allifkwargs):
    title="Add Stock Item"
   
    user_var=request.user.usercompany
    usr=request.user
    usrslg=request.user.customurlslug
    main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
    sector=str(main_sbscrbr_entity.sector)

    ###### start... UID generation ##################
    allifquery=CommonStocksModel.objects.filter(company=main_sbscrbr_entity)
    unque=str(uuid4()).split('-')[2]
    nmbr=int(allifquery.count())+int(1)
    currntyear= datetime.date.today().year
    allifuid=str(nmbr)+"/"+str(currntyear)+"/"+str(unque)
    ###### End... UID generation ##################
    
    form=CommonStockItemAddForm(main_sbscrbr_entity)
    if  main_sbscrbr_entity!=None:
        if request.method=='POST':
            form=CommonStockItemAddForm(main_sbscrbr_entity, request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.company =main_sbscrbr_entity
                obj.owner =usr
                #obj.uid=allifuid
                obj.save()
                return redirect('allifmaalcommonapp:commonStocks',allifusr=usrslg,allifslug=user_var)

            else:
                form=CommonCustomerAddForm(main_sbscrbr_entity)

    context={
        "form":form,
        "sector":sector,
        "main_sbscrbr_entity":main_sbscrbr_entity,
        "title":title,
        
        }
    return render(request,'allifmaalcommonapp/stocks/add-stock.html',context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit 
def commonEditStockItem(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        sector=str(main_sbscrbr_entity.sector)
        user_var_update=CommonStocksModel.objects.filter(id=pk).first()
        #allifuid=user_var_update.uid
        form=CommonStockItemAddForm(main_sbscrbr_entity, instance=user_var_update)
       
        title="Edit Stock Item Details"

        if request.method=='POST':
            form=CommonStockItemAddForm(main_sbscrbr_entity, request.POST, instance=user_var_update)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=user_var_update.owner
                #obj.uid=allifuid
                obj.save()
                return redirect('allifmaalcommonapp:commonStocks',allifusr=usrslg,allifslug=user_var)
               
        context={"title":title,"form":form,"sector":sector,}
        return render(request,'allifmaalcommonapp/stocks/add-stock.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonStockItemSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonStocksModel.objects.filter((Q(description__icontains=allifsearch)|Q(partNumber__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
           
        }
        return render(request,'allifmaalcommonapp/stocks/stocks.html',context)
        
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonStockItemAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        allifqueryset=CommonCompanyDetailsModel.objects.all()
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
        allifqueryset=CommonBankWithdrawalsModel.objects.filter(company=main_sbscrbr_entity)
       
        firstDate=CommonBankWithdrawalsModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonBankWithdrawalsModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonBankWithdrawalsModel.objects.filter(company=main_sbscrbr_entity).order_by('-amount').first().amount
       
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonStocksModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(quantity__gte=start_value or 0) & Q(quantity__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/stocks/stock-item-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
                    "scopes":scopes
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
                elif selected_option=="excel":
                    compnyresource=commonBankWithdrawalResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    "formats":formats,
                    "title":title,
                     "scopes":scopes
                    }
                    return render(request,'allifmaalcommonapp/stocks/stocks.html',context)
                    
            else:
                allifqueryset=CommonShareholderBankDepositsModel.objects.filter(company=main_sbscrbr_entity)
                
                
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

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonWantToDeleteStockItem(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
@logged_in_user_can_delete    
def commonDeleteStockItem(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonStocksModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonStocks',allifusr=usrslg,allifslug=user_var)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


############################# STOCK PURCHASE ORDERS #####################################
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
def commonPurchaseOrders(request,*allifargs,**allifkwargs):
    try:
        title="Purchases & Purchase Orders"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=[]
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        if logged_user_profile!=None:
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
            
        if logged_user_can_access_all==True:
            allifqueryset=CommonPurchaseOrdersModel.objects.filter(company=main_sbscrbr_entity)
      
        else:# if true, it means that company exists and logged user is owner 
            allifqueryset=CommonPurchaseOrdersModel.objects.filter(company=main_sbscrbr_entity,department=logged_user_department)
        
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                allifqueryset=CommonPurchaseOrdersModel.objects.filter(company=main_sbscrbr_entity).order_by('-date')
            else:
                allifqueryset=CommonPurchaseOrdersModel.objects.filter(company=main_sbscrbr_entity)
        else:
            pass
        latest=CommonPurchaseOrdersModel.objects.order_by('-date').filter(company=main_sbscrbr_entity,posting_po_status="posted")[:7]

       
        context={
           
            "title":title,
          "formats":formats,
          "datasorts":datasorts,
            "latest":latest,
            "allifqueryset":allifqueryset,

        }
        return render(request,'allifmaalcommonapp/purchases/purchaseorders.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
def commonNewPurchaseOrder(request,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
       
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html')
            
        ###### start... UID generation ##################
        allifquery=CommonPurchaseOrdersModel.objects.filter(company=main_sbscrbr_entity)
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        currntyear= datetime.date.today().year
        allifuid=str(nmbr)+"/"+str(currntyear)+"/"+str(unque)
        ###### End... UID generation ##################

        if allifquery:
            purchaseNumber='PO'+"/"+str(allifuid)
        else:
            purchaseNumber= 'PO/1'+"/"+str(currntyear)+"/"+str(uuid4()).split('-')[2]
        newPurchaseOrder= CommonPurchaseOrdersModel.objects.create(po_number=purchaseNumber,company=main_sbscrbr_entity,owner=logged_user,division=logged_user_division,branch=logged_user_branch,department=logged_user_department)
        newPurchaseOrder.save()
        return redirect('allifmaalcommonapp:commonPurchaseOrders',allifusr=usrslg,allifslug=compslg)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_delete
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
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_delete
@logged_in_user_can_view 
def commonDeletePO(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonPurchaseOrdersModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonPurchaseOrders',allifusr=usrslg,allifslug=user_var)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonAddPODetails(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        title="Add Purchase Order Details"
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first()
        misc_costs=CommonPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=allifquery)
        form=CommonPOAddForm(main_sbscrbr_entity,instance=allifquery)
        if request.method == 'POST':
            #add_shipment_items_form=AddShippmentItemsForm(request.POST)
            form=CommonPOAddForm(main_sbscrbr_entity,request.POST,request.FILES,instance=allifquery)
            if form.is_valid():
                form.save()
               
                return redirect('allifmaalcommonapp:commonAddPODetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
      
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

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_add
def commonAddPOItems(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add items to the purchase order"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first()
        allifqueryset=CommonPurchaseOrderItemsModel.objects.filter(po_item_con=allifquery).order_by('-date')
        queryset=CommonPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=allifquery)
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
        allifquery.amounttaxincl=po_total+po_tax_amount
        allifquery.misccosts=miscCostotal
        allifquery.grandtotal=po_total+po_tax_amount+miscCostotal
        allifquery.save()
       

        form=CommonPOItemAddForm(main_sbscrbr_entity)
        add_item= None
        if request.method == 'POST':
            form=CommonPOItemAddForm(main_sbscrbr_entity,request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.po_item_con=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddPOItems',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)#just redirection page
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
        return render(request,'allifmaalcommonapp/purchases/add-po-items.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonWantToDeletePOItem(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first()#very important to get id to go to particular shipment
        myallifquery=CommonPurchaseOrderItemsModel.objects.filter(id=pk).first()
        allifquery=myallifquery.po_item_con
        form=CommonPOItemAddForm(main_sbscrbr_entity)
        allifqueryset=CommonPurchaseOrderItemsModel.objects.filter(po_item_con=allifquery).order_by('-date')
       
        add_item= None
        if request.method == 'POST':
            form=CommonPOItemAddForm(main_sbscrbr_entity,request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.po_item_con=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddPOItems',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)#just redirection page
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)

        title="Are u sure to delete"
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
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit 
def commonEditPOItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Item Details"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        sector=str(main_sbscrbr_entity.sector)
        myquery=CommonPurchaseOrderItemsModel.objects.filter(id=pk).first()
        allifquery=myquery.po_item_con
        allifqueryset=CommonPurchaseOrderItemsModel.objects.filter(po_item_con=allifquery).order_by('-date')

        form=CommonPOItemAddForm(main_sbscrbr_entity, instance=myquery)
        if request.method=='POST':
            form=CommonPOItemAddForm(main_sbscrbr_entity, request.POST, instance=myquery)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                return redirect('allifmaalcommonapp:commonAddPOItems',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)
         
        context={"title":title,"form":form,"sector":sector,"allifquery":allifquery,
                 "allifqueryset":allifqueryset,"myquery":myquery,}
        return render(request,'allifmaalcommonapp/purchases/add-po-items.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
@logged_in_user_can_delete  
@logged_in_user_can_view 
def commonDeletePOItem(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        allifquery=CommonPurchaseOrderItemsModel.objects.filter(id=pk).first()
        allifqueryPOId=allifquery.po_item_con.id
        allifquery.delete()
        return redirect('allifmaalcommonapp:commonAddPOItems',pk=allifqueryPOId,allifusr=usrslg,allifslug=user_var)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_add
def commonPOMiscCost(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add PO Misc. Costs"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first() #very important to get id to go to particular shipment
        form=CommonPOMiscCostAddForm(main_sbscrbr_entity)
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
            form=CommonPOMiscCostAddForm(main_sbscrbr_entity,request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.po_misc_cost_con=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonPOMiscCost',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)#just redirection page
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_add
def commonCalculatePOMiscCosts(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
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

        return redirect('allifmaalcommonapp:commonAddPODetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)#just redirection page
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_add   
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

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_add   
def commonDeleteMiscCost(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        queryobj=CommonPurchaseOrderMiscCostsModel.objects.filter(id=pk).first()
        mainparent=queryobj.po_misc_cost_con.id
        queryobj.delete()
        
        return redirect('allifmaalcommonapp:commonPOMiscCost',pk=mainparent,allifusr=usrslg,allifslug=user_var)
                
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_add   
def commonEditPOMiscCostDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Misc. Cost Details"
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        queryobj=CommonPurchaseOrderMiscCostsModel.objects.filter(id=pk).first()
        allifquery=queryobj.po_misc_cost_con
       
        form=CommonPOMiscCostAddForm(main_sbscrbr_entity,instance=queryobj)
       
        if request.method == 'POST':
            #add_shipment_items_form=AddShippmentItemsForm(request.POST)
            form=CommonPOMiscCostAddForm(main_sbscrbr_entity,request.POST,request.FILES,instance=queryobj)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.po_misc_cost_con=allifquery
                add_item.save()
                
                return redirect('allifmaalcommonapp:commonPOMiscCost',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
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

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
@logged_in_user_can_add     
def commonPostPO(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first()
        po_amount=allifquery.amount
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
        comments="purchase",company=main_sbscrbr_entity,owner=request.user,ledgowner="supplier")
        else:
            return HttpResponse("Please fill the missing fields")
           
       
        ################# ...start of  misc costs...credit the service provider account....###################
        misc_costs=CommonPurchaseOrderMiscCostsModel.objects.filter(po_misc_cost_con=allifquery)
        print(misc_costs)
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
         
        return redirect('allifmaalcommonapp:commonAddPODetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_var)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonPOToPdf(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
        title="Purchase Order"
        allifquery=CommonPurchaseOrdersModel.objects.filter(id=pk).first()
        po_suplier=allifquery.supplier
        allifqueryset=CommonPurchaseOrderItemsModel.objects.filter(po_item_con=allifquery)
        template_path = 'allifmaalcommonapp/purchases/po-pdf.html'
        context = {
        "allifqueryset":allifqueryset,
        "main_sbscrbr_entity":main_sbscrbr_entity,
        "title":title,
        "po_suplier":po_suplier,
        "scopes":scopes,
        "allifquery":allifquery,
        }
        
        response = HttpResponse(content_type='application/pdf')
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
    ##################################33 our customers ###################################3
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonPOSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonPurchaseOrdersModel.objects.filter((Q(po_number__icontains=allifsearch)|Q(amount__icontains=allifsearch)|Q(supplier__name__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
        }
        return render(request,'allifmaalcommonapp/purchases/purchaseorders.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonPOAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonPurchaseOrdersModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonPurchaseOrdersModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonPurchaseOrdersModel.objects.filter(company=main_sbscrbr_entity).order_by('-amount').first().amount
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonPurchaseOrdersModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/purchases/po-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
                   "datashorts":datasorts,
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
                elif selected_option=="excel":
                    compnyresource=commonBankWithdrawalResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    "formats":formats,
                    "title":title,
                    "datashorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/purchases/purchaseorders.html',context)
                    
            else:
                allifqueryset=CommonPurchaseOrdersModel.objects.filter(company=main_sbscrbr_entity)
         
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
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
    
######################### QUOTATION #########################
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonQuotes(request,*allifargs,**allifkwargs):
    try:
        title="Quotations"
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity)
        no_of_quotes=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity).count()
        no_of_prospects=CommonQuotesModel.objects.filter(prospect="Likely",company=main_sbscrbr_entity).count()
        prospects=CommonQuotesModel.objects.filter(prospect='Likely',company=main_sbscrbr_entity).order_by('-date')[:7]
        total_value_of_prospects=CommonQuotesModel.objects.filter(prospect="Likely",company=main_sbscrbr_entity).aggregate(Sum('total'))['total__sum']
        
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
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonNewQuote(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        usr=request.user
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_var).first()
    
        ###### start... UID generation ##################
        allifquery=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity)
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        currntyear= datetime.date.today().year
        allifuid=str(nmbr)+"/"+str(currntyear)+"/"+str(unque)
        ###### End... UID generation ##################

        if allifquery:
            sqnmbr='SQ'+"/"+str(allifuid)
        else:
            sqnmbr= 'SQ/1'+"/"+str(currntyear)+"/"+str(uuid4()).split('-')[2]

        newQuoteNumber= CommonQuotesModel.objects.create(number=sqnmbr,company=main_sbscrbr_entity,owner=usr)
        newQuoteNumber.save()

        return redirect('allifmaalcommonapp:commonQuotes',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_delete
def commonWantToDeleteQuote(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonQuotesModel.objects.filter(id=pk).first()
        myallifquery=CommonQuotesModel.objects.filter(id=pk).first()
        title="Are u sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        "myallifquery":myallifquery,
        }
        return render(request,'allifmaalcommonapp/quotes/x-qt-confrm.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_delete
def commonDeleteQuote(request,pk,*allifargs,**allifkwargs):
    try:
        usrslg=request.user.customurlslug
        user_var=request.user.usercompany
        CommonQuotesModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonQuotes',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_add
def commonAddQuoteDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Quote Details"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonQuotesModel.objects.filter(id=pk).first()
        form=CommonAddQuoteDetailsForm(main_sbscrbr_entity,instance=allifquery)
        if request.method == 'POST':
            form=CommonAddQuoteDetailsForm(main_sbscrbr_entity,request.POST,request.FILES,instance=allifquery)
            if form.is_valid():
                form.save()
                return redirect('allifmaalcommonapp:commonAddQuoteDetails',pk=allifquery.id,allifusr=usrslg,allifslug=compslg)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        context={
            "form":form,
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/quotes/add-quote-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_add
def commonAddQuoteItems(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Quote Items"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonQuotesModel.objects.filter(id=pk).first()
        form=CommonAddQuoteItemsForm(main_sbscrbr_entity)
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
        if request.method == 'POST':
            form=CommonAddQuoteItemsForm(main_sbscrbr_entity,request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.allifquoteitemconnector=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddQuoteItems',pk=allifquery.id,allifusr=usrslg,allifslug=compslg)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        
        context={
        "form":form,
        "allifquery":allifquery,
        "allifquerysettotal":allifquerysettotal,
        "allifqueryset":allifqueryset,
        "title":title, 
        }
        return render(request,'allifmaalcommonapp/quotes/add-quote-items.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit 
def commonEditQuoteItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Item Details"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        myquery=CommonQuoteItemsModel.objects.filter(id=pk).first()
        allifquery=myquery.allifquoteitemconnector
        allifqueryset=CommonQuoteItemsModel.objects.filter(allifquoteitemconnector=allifquery).order_by('-date')

        form=CommonAddQuoteItemsForm(main_sbscrbr_entity, instance=myquery)
        if request.method=='POST':
            form=CommonAddQuoteItemsForm(main_sbscrbr_entity, request.POST, instance=myquery)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                return redirect('allifmaalcommonapp:commonAddQuoteItems',pk=allifquery.id,allifusr=usrslg,allifslug=compslg)
              
        context={"title":title,"form":form,"allifquery":allifquery,
                 "allifqueryset":allifqueryset,"myquery":myquery,}
        return render(request,'allifmaalcommonapp/quotes/add-quote-items.html',context)
        
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_delete
def commonWantToDeleteQuoteItem(request,pk,*allifargs,**allifkwargs): 
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        form=CommonAddQuoteItemsForm(main_sbscrbr_entity)
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_delete
def commonDeleteQuoteItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Quote Items"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        myallifquery=CommonQuoteItemsModel.objects.filter(id=pk).first()
        myquery=myallifquery.allifquoteitemconnector
        myallifquery.delete()
        return redirect('allifmaalcommonapp:commonAddQuoteItems',pk=myquery.id,allifusr=usrslg,allifslug=compslg)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view
def commonQuoteToPdf(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usr_var=request.user
        date_today=date.today()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
        allifquery=CommonQuotesModel.objects.filter(id=pk).first()
        allifqueryset=CommonQuoteItemsModel.objects.filter(allifquoteitemconnector=allifquery)
        title="Quote "+str(allifquery)
        template_path = 'allifmaalcommonapp/quotes/quote-pdf.html'
        context = {
        "allifqueryset":allifqueryset,
        "allifquery":allifquery,
        "title":title,
        "scopes":scopes,
        "main_sbscrbr_entity":main_sbscrbr_entity,
        "usr_var":usr_var,
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
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
                allifquery= CommonQuotesModel.objects.all()
                return JsonResponse(allifquery, safe=False)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonQuotesSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonQuotesModel.objects.filter((Q(number__icontains=allifsearch)|Q(total__icontains=allifsearch)|Q(customer__name__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
        }
        return render(request, 'allifmaalcommonapp/quotes/quotes.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonQuoteAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity).order_by('-total').first().total
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonQuotesModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(total__gte=start_value or 0) & Q(total__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/quotes/quote-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
                   "datashorts":datasorts,
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
                elif selected_option=="excel":
                    compnyresource=commonBankWithdrawalResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    "formats":formats,
                    "title":title,
                    "datashorts":datasorts,
                   "formats":formats,
                    }
                    return render(request, 'allifmaalcommonapp/quotes/quotes.html',context)
                    
            else:
                allifqueryset=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity)
         
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
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

def commonScrollableTable(request,*allifargs,**allifkwargs):
    allifqueryset=CommonDivisionsModel.objects.all()
   
    context={
        "allifqueryset":allifqueryset,
      
    }
    return render(request,'allifmaalcommonapp/table.html',context)

##########################3 INVOICES #######################333
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonInvoices(request,*allifargs,**allifkwargs):
    try:
        title="Invoices"
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        usrslg=request.user.customurlslug
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonInvoicesModel.objects.filter(company=main_sbscrbr_entity)
        no_invoices=CommonInvoicesModel.objects.filter(company=main_sbscrbr_entity).count()
        #last_invoices=CommonInvoicesModel.objects.order_by('invoice_number')[:6]
        #latest_paid_invoices=CommonInvoicesModel.objects.filter(invoice_status='Paid').order_by('-date')[:7]
        #posted_invoices_total_value=CommonInvoicesModel.objects.filter(posting_inv_status="posted").aggregate(Sum('invoice_total'))['invoice_total__sum']
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

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonNewInvoice(request,*allifargs,**allifkwargs):
    try:
        usrslg=request.user.customurlslug
        usr=request.user
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
    
        ###### start... UID generation ##################
        allifquery=CommonInvoicesModel.objects.filter(company=main_sbscrbr_entity)
        unque=str(uuid4()).split('-')[2]
        nmbr=int(allifquery.count())+int(1)
        currntyear= datetime.date.today().year
        allifuid=str(nmbr)+"/"+str(currntyear)+"/"+str(unque)
        ###### End... UID generation ##################

        if allifquery:
            invnmbr='Inv'+"/"+str(allifuid)
        else:
            invnmbr= 'Inv/1'+"/"+str(currntyear)+"/"+str(uuid4()).split('-')[2]

        newinv= CommonInvoicesModel.objects.create(number=invnmbr,company=main_sbscrbr_entity,owner=usr)
        newinv.save()
        return redirect('allifmaalcommonapp:commonInvoices',allifusr=usrslg,allifslug=compslg)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_delete
def commonWantToDeleteInvoice(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonInvoicesModel.objects.filter(id=pk).first()
        myallifquery=CommonInvoicesModel.objects.filter(id=pk).first()
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        "myallifquery":myallifquery,
        }
        return render(request,'allifmaalcommonapp/invoices/x-inv-confrm.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonDeleteInvoice(request,pk,*allifargs,**allifkwargs):
    try:
        user_var=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonInvoicesModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonInvoices',allifusr=usrslg,allifslug=user_var)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonAddInvoiceDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Invoice Details "
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonInvoicesModel.objects.filter(id=pk).first()
        form=CommonAddInvoiceDetailsForm(main_sbscrbr_entity,instance=allifquery)
        if request.method == 'POST':
            form=CommonAddInvoiceDetailsForm(main_sbscrbr_entity,request.POST,request.FILES,instance=allifquery)
            if form.is_valid():
                form.save()
                return redirect('allifmaalcommonapp:commonAddInvoiceDetails',pk=allifquery.id,allifusr=usrslg,allifslug=compslg)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        
        context={
            "form":form,
            "title":title,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/invoices/add-invoice-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonAddInvoiceItems(request,pk,*allifargs,**allifkwargs):
    try:
        
        title="Add Invoice Items "
      
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonInvoicesModel.objects.filter(id=pk).first()
        form=CommonAddInvoiceItemsForm(main_sbscrbr_entity)
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
        if request.method == 'POST':
            form=CommonAddInvoiceItemsForm(main_sbscrbr_entity,request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.allifinvitemconnector=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddInvoiceItems',pk=allifquery.id,allifusr=usrslg,allifslug=compslg)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)

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

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_edit 
def commonEditInvoiceItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Invoice Item Details"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        myquery=CommonInvoiceItemsModel.objects.filter(id=pk).first()
        allifquery=myquery.allifinvitemconnector
        allifqueryset=CommonInvoiceItemsModel.objects.filter(allifinvitemconnector=allifquery).order_by('-date')

        form=CommonAddInvoiceItemsForm(main_sbscrbr_entity, instance=myquery)
        if request.method=='POST':
            form=CommonAddInvoiceItemsForm(main_sbscrbr_entity, request.POST, instance=myquery)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                
                return redirect('allifmaalcommonapp:commonAddInvoiceItems',pk=allifquery.id,allifusr=usrslg,allifslug=compslg)
              
        context={"title":title,"form":form,"allifquery":allifquery,
                 "allifqueryset":allifqueryset,"myquery":myquery,}
        return render(request,'allifmaalcommonapp/invoices/add-inv-items.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)
    

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_delete
def commonWantToDeleteInvoiceItem(request,pk,*allifargs,**allifkwargs): 
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        form=CommonAddInvoiceItemsForm(main_sbscrbr_entity)
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonDeleteInvoiceItem(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Quote Items"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        myallifquery=CommonInvoiceItemsModel.objects.filter(id=pk).first()
        myquery=myallifquery.allifinvitemconnector
        myallifquery.delete()
        return redirect('allifmaalcommonapp:commonAddInvoiceItems',pk=myquery.id,allifusr=usrslg,allifslug=compslg)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonPostInvoice(request,pk,*allifargs,**allifkwargs):
    try:
        
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=CommonBanksModel.objects.filter(company=main_sbscrbr_entity)
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            context={
                "logged_user":logged_user
            }
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)


        allifquery=CommonInvoicesModel.objects.filter(id=pk).first()#very important to get id to go to particular shipment
        allifqueryset=CommonInvoiceItemsModel.objects.filter(allifinvitemconnector=allifquery)
        myinvid=allifquery.id
        customer=allifquery.customer
        amount=allifquery.total
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
                    
                    products=CommonStocksModel.objects.filter(pk=invoice_item_id,company=main_sbscrbr_entity).first()
                    initial_item_quantity=products.quantity
                    products.quantity=initial_item_quantity-invo_quantity # reduce stock by invoice quantity
                    products.save()

                    # ....... debit the inventory account ..........
                    inv_acc=CommonChartofAccountsModel.objects.filter(pk=inventory_acc_id,company=main_sbscrbr_entity).first()
                    initial_inv_bal=inv_acc.balance
                    inv_acc.balance=initial_inv_bal-per_line_cost_price
                    inv_acc.save()

                   
                    # ....... record the revenue in the income account ..........
                    income_acc=CommonChartofAccountsModel.objects.filter(pk=income_acc_id,company=main_sbscrbr_entity).first()
                    initial_income_bal=income_acc.balance
                    income_acc.balance=initial_income_bal + per_line_selling_price
                    income_acc.save()

                    # ....... record the Cost of goods sold ..........
                    cost_goods_sold_acc_exist=CommonChartofAccountsModel.objects.filter(description="COGS",company=main_sbscrbr_entity,department=logged_user_department).first()
                    if cost_goods_sold_acc_exist:

                        cost_goods_sold_acc=CommonChartofAccountsModel.objects.filter(description="COGS",company=main_sbscrbr_entity,department=logged_user_department).first()
                        initial_cost_of_goods_sold_balance=cost_goods_sold_acc.balance
                        cost_goods_sold_acc.balance=initial_cost_of_goods_sold_balance+per_line_cost_price
                        cost_goods_sold_acc.save()
                else:
                    return HttpResponse("Please ensure invoice details are filled and that all items have been linked to the Chart of Accounts")

                    

                #increase customer turnover
                mycustomer=CommonCustomersModel.objects.filter(pk=customer_id,company=main_sbscrbr_entity,department=logged_user_department).first()
                initial_customer_acc_turnover=mycustomer.turnover or 0
               
                mycustomer.turnover=initial_customer_acc_turnover+item.description.unitPrice
                initial_customer_acc_balance=mycustomer.balance or 0
                mycustomer.balance=initial_customer_acc_balance+item.description.unitPrice

                mycustomer.save()
             
                #transaction=AllifmaalCustomerStatementModel.objects.create(customer=customer,debit=inv_total,
                        #comments="Invoice",balance=initial_customer_acc_balance+inv_total)#get the ord
            

                # ......... credit the equity account .........
                equity_acc=CommonChartofAccountsModel.objects.filter(description="Equity",company=main_sbscrbr_entity,department=logged_user_department).first()
                if equity_acc:
                    initial_equity_account_balance=equity_acc.balance
                    equity_acc.balance=initial_equity_account_balance + item.description.unitPrice-item.description.unitcost
                    equity_acc.save()
                else:
                    pass

                ######## change invoice status
                allifquery.posting_inv_status="posted"
                allifquery.save()

            # ....... record the gross profit ..........
                gross_profit_acc_exist=CommonChartofAccountsModel.objects.filter(description="Gross Profit",company=main_sbscrbr_entity,department=logged_user_department).first()
                if gross_profit_acc_exist:

                    profit_and_loss_acc=CommonChartofAccountsModel.objects.filter(description="Gross Profit",company=main_sbscrbr_entity,department=logged_user_department).first()
                    initial_profit_and_loss_balance=profit_and_loss_acc.balance
                    profit_and_loss_acc.balance=initial_profit_and_loss_balance+item.description.unitPrice-item.description.unitcost
                    profit_and_loss_acc.save()
                    
                else:
                    pass
        CommonLedgerEntriesModel.objects.create(customer=customer,credit=amount,
        comments="invoice",company=main_sbscrbr_entity,owner=request.user,ledgowner="customer")
 
        return redirect('allifmaalcommonapp:commonAddInvoiceDetails',pk=allifquery.id,allifusr=usrslg,allifslug=user_cmpny_slug)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonPostedInvoices(request,*allifargs,**allifkwargs):
    try:
        posted_invoices=CommonInvoicesModel.objects.filter(posting_inv_status="posted")
        posted_invoices_count=CommonInvoicesModel.objects.filter(posting_inv_status="posted").count()
        last_invoices=CommonInvoicesModel.objects.filter(posting_inv_status="posted").order_by('-invoice_total')[:7]
        
        title="Posted Invoices"
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        usrslg=request.user.customurlslug
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonInvoicesModel.objects.filter(company=main_sbscrbr_entity)
        no_invoices=CommonInvoicesModel.objects.filter(company=main_sbscrbr_entity).count()
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonInvoiceToPdf(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usr_var=request.user
        date_today=date.today()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
        allifquery=CommonInvoicesModel.objects.filter(id=pk).first()
        allifqueryset=CommonInvoiceItemsModel.objects.filter(allifinvitemconnector=allifquery)
        title="Invoice "+str(allifquery)
        template_path = 'allifmaalcommonapp/invoices/invoice-pdf.html'
        context = {
        "allifqueryset":allifqueryset,
        "allifquery":allifquery,
        "title":title,
        "scopes":scopes,
        "main_sbscrbr_entity":main_sbscrbr_entity,
        "usr_var":usr_var,
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonSearchAjaxInvoice(request,*allifargs,**allifkwargs):
    try:
   
        if request.method=="GET":
            data_from_front_end=request.GET.get('search_result_key')
            print(data_from_front_end)
            
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


@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonInvoicesSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonInvoicesModel.objects.filter((Q(number__icontains=allifsearch)|Q(total__icontains=allifsearch)|Q(customer__name__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
        }
        return render(request,'allifmaalcommonapp/invoices/invoices.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonInvoiceAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonInvoicesModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonInvoicesModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonInvoicesModel.objects.filter(company=main_sbscrbr_entity).order_by('-total').first().total
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonInvoicesModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(total__gte=start_value or 0) & Q(total__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/invoices/invoice-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
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
                elif selected_option=="excel":
                    compnyresource=commonBankWithdrawalResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/invoices/invoices.html',context)
                 
            else:
                allifqueryset=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity)
         
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

################# general ledger entris #############
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_add
def commonLedgerEntries(request,*allifargs,**allifkwargs):
    try:
        title="Ledger Entries"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            context={
                "logged_user":logged_user
            }
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        allifqueryset= CommonLedgerEntriesModel.objects.filter(company=main_sbscrbr_entity).order_by('date') 
        context ={ 
         'allifqueryset':allifqueryset,
          "title":title, }
        
         
        return render(request,'allifmaalcommonapp/ledgerentries/ledgerentries.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonLedgerEntryDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Ledger Entry Details "
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonLedgerEntriesModel.objects.filter(id=pk).first()
        context={
            "title":title,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/ledgerentries/ledger-entry-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_delete
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view   
def commonDeleteLedgerEntry(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonLedgerEntriesModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonLedgerEntries',allifusr=usrslg,allifslug=compslg)
      
    except:
        return render(request,'allifmaalapp/error.html')

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonLedgerEntrySearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonLedgerEntriesModel.objects.filter((Q(debit__icontains=allifsearch)
            |Q(debit__icontains=allifsearch)|Q(credit__icontains=allifsearch)|Q(balance__icontains=allifsearch)|Q(customer__name__icontains=allifsearch)|Q(supplier__name__icontains=allifsearch)|Q(staff__staffNo__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
        }
        return render(request,'allifmaalcommonapp/ledgerentries/ledgerentries.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonLedgerEntryAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonLedgerEntriesModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonLedgerEntriesModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonLedgerEntriesModel.objects.filter(company=main_sbscrbr_entity).order_by('-balance').first().balance
        scopes=CommonCompanyScopeModel.objects.filter(company=main_sbscrbr_entity)
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonLedgerEntriesModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(balance__gte=start_value or 0) & Q(balance__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/ledgerentries/ledger-entries-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
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
                elif selected_option=="excel":
                    compnyresource=commonBankWithdrawalResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/ledgerentries/ledgerentries.html',context)
                 
            else:
                allifqueryset=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity)
         
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonSupplierLedgerEntries(request,pk,*allifargs,**allifkwargs):
    try: 
        title="Supplier Ledger Entries Details"
        
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonSuppliersModel.objects.filter(id=pk).first()
        allifqueryset= CommonLedgerEntriesModel.objects.filter(supplier=allifquery,company=main_sbscrbr_entity).order_by('date') 
        
        context = { 'allifquery':allifquery, 'allifqueryset':allifqueryset, 'title':title, }
        return render(request,'allifmaalcommonapp/ledgerentries/suppliers/supplier-ledger-entries.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonCustomerLedgerEntries(request,pk,*allifargs,**allifkwargs):
    try: 
        title="Customer Ledger Entries Details"
        
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonCustomersModel.objects.filter(id=pk).first()
        allifqueryset= CommonLedgerEntriesModel.objects.filter(customer=allifquery,company=main_sbscrbr_entity).order_by('date') 
        
        context = { 'allifquery':allifquery, 'allifqueryset':allifqueryset, 'title':title, }
        return render(request,'allifmaalcommonapp/ledgerentries/customers/customer-ledger-entries.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonStaffLedgerEntries(request,pk,*allifargs,**allifkwargs):
    try: 
        title="Staff Ledger Entries Details"
        
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonEmployeesModel.objects.filter(id=pk).first()
        allifqueryset= CommonLedgerEntriesModel.objects.filter(supplier=allifquery,company=main_sbscrbr_entity).order_by('date') 
        
        context = { 'allifquery':allifquery, 'allifqueryset':allifqueryset, 'title':title, }
        return render(request,'allifmaalcommonapp/ledgerentries/staff/staff-ledger-entries.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
######### supplier payments section ############
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonSupplierPayments(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonSupplierPaymentsModel.objects.filter(company=main_sbscrbr_entity)
        allifquerysetlatest=CommonSupplierPaymentsModel.objects.filter(company=main_sbscrbr_entity).order_by('-date')[:7]
        title="Supplier Payments"
        context={
        "title":title,
        "allifqueryset":allifqueryset,
        "allifquerysetlatest":allifquerysetlatest,
        "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payments.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonPaySupplier(request,pk,*allifargs,**allifkwargs):
    try:
        title="Pay Supplier"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            context={
                "logged_user":logged_user
            }
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        allifquery=CommonSuppliersModel.objects.filter(id=pk).first()
        form=CommonAddSupplierPaymentForm(main_sbscrbr_entity,logged_user_department)
        add_item= None
        if request.method == 'POST':
            form=CommonAddSupplierPaymentForm(main_sbscrbr_entity,logged_user_department,request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.supplier=allifquery
                add_item.company=main_sbscrbr_entity
                add_item.owner=request.user
                add_item.save()
                return redirect('allifmaalcommonapp:commonSupplierPayments',allifusr=usrslg,allifslug=compslg)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        context={
            "form":form,  
            "title":title,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/pay-supplier.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonSupplierPaymentSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonSupplierPaymentsModel.objects.filter((Q(amount__icontains=allifsearch)
            |Q(description__icontains=allifsearch)|Q(supplier__name__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payments.html',context)
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonSupplierPaymentAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonSupplierPaymentsModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonSupplierPaymentsModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonSupplierPaymentsModel.objects.filter(company=main_sbscrbr_entity).order_by('-amount').first().amount
        scopes=CommonSupplierPaymentsModel.objects.filter(company=main_sbscrbr_entity)
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonSupplierPaymentsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":

                    template_path = 'allifmaalcommonapp/payments/suppliers/supplier-payment-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
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
                elif selected_option=="excel":
                    compnyresource=commonBankWithdrawalResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payments.html',context)
            else:
                allifqueryset=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity)
         
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_delete
def commonWantToDeleteSupplierPayment(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonSupplierPaymentsModel.objects.filter(id=pk).first()
        myallifquery=CommonSupplierPaymentsModel.objects.filter(id=pk).first()
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        "myallifquery":myallifquery,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/x-supplier-payment-confrm.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_delete 
def commonDeleteSupplierPayment(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonSupplierPaymentsModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonSupplierPayments',allifusr=usrslg,allifslug=compslg)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonSupplierPaymentDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Supplier Payment Details "
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            context={
                "logged_user":logged_user
            }
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        allifquery=CommonSupplierPaymentsModel.objects.filter(id=pk).first()
        form =CommonAddSupplierPaymentForm(main_sbscrbr_entity,logged_user_department,instance=allifquery)
        if request.method == 'POST':
            form = CommonAddSupplierPaymentForm(main_sbscrbr_entity,logged_user_department,request.POST, instance=allifquery)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.company=main_sbscrbr_entity
                add_item.owner=request.user
                add_item.save()
                return redirect('allifmaalcommonapp:commonSupplierPaymentDetails',pk=allifquery.id,allifusr=usrslg,allifslug=compslg)
        context={
            
            "title":title,
            "allifquery":allifquery,
            "form":form,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/supplier-payment-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonEditSupplierPayment(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Supplier Payment"
        allifquery= CommonSupplierPaymentsModel.objects.filter(id=pk).first()
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
       
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            context={
                "logged_user":logged_user
            }
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        form =CommonAddSupplierPaymentForm(main_sbscrbr_entity,logged_user_department,instance=allifquery)
        if request.method == 'POST':
            form = CommonAddSupplierPaymentForm(main_sbscrbr_entity,logged_user_department,request.POST, instance=allifquery)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.company=main_sbscrbr_entity
                add_item.owner=request.user
                add_item.save()
                #CommonSupplierPaymentsModel.objects.get(id=pk).delete()
                return redirect('allifmaalcommonapp:commonSupplierPayments',allifusr=usrslg,allifslug=compslg)
              
        context = {
            'form':form,
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/pay-supplier.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonPostSupplierPayment(request,pk,*allifargs,**allifkwargs):#global
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonSupplierPaymentsModel.objects.filter(id=pk).first()
        allifsup=allifquery.supplier.id
        amount=allifquery.amount#this gives the amount of salary given to the staff
        pay_from_acc_id=allifquery.account.id
        mysupp=CommonSuppliersModel.objects.filter(id=pk).first()
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
        comments="Payment",balance= Decimal(init_balance)+Decimal(amount),company=main_sbscrbr_entity,owner=request.user,ledgowner="supplier")#get the ord
        legs=CommonLedgerEntriesModel.objects.all()

        print(legs)
        allifquery.status="posted"
        allifquery.save()
        return redirect('allifmaalcommonapp:commonSupplierPayments',allifusr=usrslg,allifslug=compslg)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonPostedSupplierPayments(request,*allifargs,**allifkwargs):
    try:
        title="Posted Supplier Payments"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
       
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            context={
                "logged_user":logged_user
            }
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        
        allifqueryset=CommonSupplierPaymentsModel.objects.filter(status="posted",company=main_sbscrbr_entity)
        latestpayments=CommonSupplierPaymentsModel.objects.filter(company=main_sbscrbr_entity).order_by('-date')[:7]
        context={
            "allifqueryset":allifqueryset,
            "title":title,
            "latestpayments":latestpayments,
        }
        return render(request,'allifmaalcommonapp/payments/suppliers/posted-payments.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonPaySupplierDirect(request,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
       
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            context={
                "logged_user":logged_user
            }
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        
        form=CommonAddSupplierPaymentForm(main_sbscrbr_entity,logged_user_department)
        title="Direct Pay Supplier"
        if request.method == 'POST':
            form=CommonAddSupplierPaymentForm(main_sbscrbr_entity,logged_user_department,request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.company=main_sbscrbr_entity
                add_item.owner=request.user
                add_item.save()
                return redirect('allifmaalcommonapp:commonSupplierPayments',allifusr=usrslg,allifslug=compslg)
       
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

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonSupplierStatementpdf(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonSuppliersModel.objects.filter(id=pk).first()
        allifqueryset= CommonLedgerEntriesModel.objects.filter(supplier=allifquery,company=main_sbscrbr_entity).order_by('date') 
        total = sum(transaction.balance for transaction in allifqueryset) 
        mydate=datetime.date.today()
        system_user=request.user
        title="Customer Statement "+" "+str(allifquery)
        template_path = 'allifmaalapp/suppliers/statements/supplier-statement-details-pdf.html'
      
        context = {
        'allifquery':allifquery,
        "system_user":system_user,
        "title":title,
        
        "mydate":mydate,
    
        }
        
        response = HttpResponse(content_type='application/pdf')
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonCustomerPayments(request,*allifargs,**allifkwargs):
    try:
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonCustomerPaymentsModel.objects.filter(company=main_sbscrbr_entity)
        allifquerysetlatest=CommonCustomerPaymentsModel.objects.filter(company=main_sbscrbr_entity).order_by('-date')[:7]
        title="Customer Payments"
        context={
            
            "title":title,
            "allifqueryset":allifqueryset,
            "allifquerysetlatest":allifquerysetlatest,
        }
        return render(request,'allifmaalcommonapp/payments/customers/customer-payments.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonTopUpCustomerAccount(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        default_cash_accs=CommonChartofAccountsModel.objects.filter(description="Cash").first()
        form=CommonAddCustomerPaymentForm(main_sbscrbr_entity,initial={'account':default_cash_accs})
        customer=CommonCustomersModel.objects.get(id=pk)
        mycustid=customer.id
        title="Receive Payment From "+ str(customer)
    
        top_up_cust_account= get_object_or_404(CommonCustomersModel, id=pk)
        topups=CommonCustomerPaymentsModel.objects.filter(customer=customer)#this line helps to
        
        add_item= None
        if request.method == 'POST':
            form=CommonAddCustomerPaymentForm(main_sbscrbr_entity,request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.customer=top_up_cust_account
                add_item.company=main_sbscrbr_entity
                add_item.save()
                form=CommonAddCustomerPaymentForm(main_sbscrbr_entity)
                
                return redirect("allifmaalcommonapp:commonCustomerPayments",allifusr=usrslg,allifslug=compslg)
                #return redirect("allifmaalapp:AllifmaaltopUpCustomerAccount",pk=mycustid)

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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonEditCustomerPayment(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        title="Update Customer Payment"
        allifquery=CommonCustomerPaymentsModel.objects.get(id=pk)
        form=CommonAddCustomerPaymentForm(main_sbscrbr_entity,instance=allifquery)
    
        if request.method == 'POST':
            form =CommonAddCustomerPaymentForm(main_sbscrbr_entity,request.POST, instance=allifquery)
            if form.is_valid():
                form.save()
                return redirect("allifmaalcommonapp:commonCustomerPayments",allifusr=usrslg,allifslug=compslg)
               
        context = {
            "form":form,
            "allifquery":allifquery,
           
            "title":title,
        }
        
        return render(request,'allifmaalcommonapp/payments/customers/add-customer-payment.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_delete
def commonWantToDeleteCustomerPayment(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonCustomerPaymentsModel.objects.filter(id=pk).first()
        myallifquery=CommonCustomerPaymentsModel.objects.filter(id=pk).first()
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        "myallifquery":myallifquery,
        }
        return render(request,'allifmaalcommonapp/payments/customers/x-cust-payment-confrm.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view   
def commonDeleteCustomerPayment(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug

        CommonCustomerPaymentsModel.objects.get(id=pk).delete()
        return redirect("allifmaalcommonapp:commonCustomerPayments",allifusr=usrslg,allifslug=compslg)
        return redirect('allifmaalapp:AllifmaalCustomerPayments')
    except:
        return render(request,'allifmaalapp/error.html')
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonCustomerPaymentDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Payment Details "
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        user_cmpny_slug=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=user_cmpny_slug).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            context={
                "logged_user":logged_user
            }
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        allifquery=CommonCustomerPaymentsModel.objects.filter(id=pk).first()
        form =CommonAddCustomerPaymentForm(main_sbscrbr_entity,instance=allifquery)
        if request.method == 'POST':
            form =CommonAddCustomerPaymentForm(main_sbscrbr_entity,request.POST, instance=allifquery)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.company=main_sbscrbr_entity
                add_item.owner=request.user
                add_item.save()
                return redirect('allifmaalcommonapp:commonCustomerPaymentDetails',pk=allifquery.id,allifusr=usrslg,allifslug=compslg)
            
        context={
            
            "title":title,
            "allifquery":allifquery,
            "form":form,
            
        }
        return render(request,'allifmaalcommonapp/payments/customers/customer-payment-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonReceiveCustomerMoney(request,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
       
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            context={
                "logged_user":logged_user
            }
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        
        form=CommonAddCustomerPaymentForm(main_sbscrbr_entity)
        title="Receive Customer Money"
        if request.method == 'POST':
            form=CommonAddCustomerPaymentForm(main_sbscrbr_entity,request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.company=main_sbscrbr_entity
                add_item.owner=request.user
                add_item.save()
                return redirect('allifmaalcommonapp:commonCustomerPayments',allifusr=usrslg,allifslug=compslg)
       
        context={
            "form":form,  
            "title":title,
        }
        return render(request,'allifmaalcommonapp/payments/customers/receive-customer-money.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonPostCustomerPayment(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        payment=CommonCustomerPaymentsModel.objects.get(id=pk)#very important to get id to go to particular shipment
        myamount=payment.amount#this gives the initial account
        customer=payment.customer
        debit_acc=payment.account
        if (customer and myamount)!=None:
            mycust=CommonCustomersModel.objects.get(id=customer.id)
            initial_cust_acc_bal=mycust.balance
            mycust.balance= Decimal(initial_cust_acc_bal)-Decimal(myamount)
            mycust.status="posted"
            mycust.save()

            # debit the asset account where the money from customer is received to
            coa_acc=CommonChartofAccountsModel.objects.get(id=debit_acc.id)
            initial_coa_acc_bal=coa_acc.balance
            coa_acc.balance= Decimal(initial_coa_acc_bal)+Decimal(myamount)
            coa_acc.save()
            CommonLedgerEntriesModel.objects.create(customer=customer,credit=myamount,
            comments="payment",company=main_sbscrbr_entity,owner=request.user,ledgowner="customer")
            return redirect('allifmaalcommonapp:commonCustomerPayments',allifusr=usrslg,allifslug=compslg)
                
        else:
            return render(request,'allifmaalcommonapp/error/error.html')
           
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonPostedCustomerPayments(request,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        title="Posted Customer Payments"
        
        allifqueryset=CommonCustomerPaymentsModel.objects.filter(status="posted",company=main_sbscrbr_entity)
        latestpayments=CommonCustomerPaymentsModel.objects.filter(status="posted",company=main_sbscrbr_entity).order_by('-date')[:7]
        context={
            "allifqueryset":allifqueryset,
            "title":title,
          
            "latestpayments":latestpayments,

        }
        return render(request,'allifmaalcommonapp/payments/customers/customer-posted-payments.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonCustomerStatementpdf(request,pk,*allifargs,**allifkwargs):
    try:
        mydate=datetime.date.today()
        system_user=request.user
        AllifQueryDetails=get_object_or_404(CommonCustomersModel,id=pk)
        title="Customer Statement "+" "+str(AllifQueryDetails)
    
        AllifObject=CommonCustomersModel.objects.get(id=pk)
        PO_suplier=AllifObject.name
        AllifQueryItems= CommonCustomerStatementsModel.objects.filter(customer=AllifObject)

        template_path = 'allifmaalapp/statements/customer-statement-details-pdf.html'
        
        #companyDetails=AllifmaalDetailsModel.objects.all()
        #scopes=AllifmaalScopeModel.objects.all()
        
        context = {
        'AllifQueryDetails':AllifQueryDetails,
        "AllifQueryItems":AllifQueryItems,
        #"companyDetails":companyDetails,
        #"scopes":scopes, 
        "system_user":system_user,
        "title":title,
        
        "PO_suplier":PO_suplier,
        "AllifObject":AllifObject,
        "mydate":mydate,
    
        }
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="Customer-Statement.pdf"'
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonCustomerPaymentSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonCustomerPaymentsModel.objects.filter((Q(amount__icontains=allifsearch)
            |Q(description__icontains=allifsearch)|Q(customer__name__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
        }
        return render(request,'allifmaalcommonapp/payments/customers/customer-payments.html',context)
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonCustomerPaymentAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonCustomerPaymentsModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonCustomerPaymentsModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonCustomerPaymentsModel.objects.filter(company=main_sbscrbr_entity).order_by('-amount').first().amount
        scopes=CommonCustomerPaymentsModel.objects.filter(company=main_sbscrbr_entity)
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonCustomerPaymentsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":

                    template_path = 'allifmaalcommonapp/payments/customers/customer-payment-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
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
                elif selected_option=="excel":
                    compnyresource=commonBankWithdrawalResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/payments/customers/customer-payments.html',context)
            else:
                allifqueryset=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity)
         
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_is_admin
def commonSalaries(request,*allifargs,**allifkwargs):
    try:
        title="Staff Salaries"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
        allifqueryset=CommonSalariesModel.objects.filter(company=main_sbscrbr_entity)
      
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }

        return render(request,'allifmaalcommonapp/hrm/salaries/salaries.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonAddSalary(request,*allifargs,**allifkwargs):
    try:
        title="Initiate Salary Payment"
        usrslg=request.user.customurlslug
        cmpslg=request.user.usercompany
        
        usr=request.user
        
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=cmpslg).first()

        form =CommonAddSalaryForm(main_sbscrbr_entity)
        if request.method == 'POST':
            form =CommonAddSalaryForm(main_sbscrbr_entity,request.POST,request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner=usr
                obj.company=main_sbscrbr_entity
                obj.save()
                
                return redirect('allifmaalcommonapp:commonSalaries',allifusr=usrslg,allifslug=cmpslg)
                
            else:
                form.non_field_errors
           
        context = {
            "title":title,
            "form":form,
     
        }

        return render(request,'allifmaalcommonapp/hrm/salaries/add-salary.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonSalarySearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonSalariesModel.objects.filter((Q(amount__icontains=allifsearch)
            |Q(description__icontains=allifsearch)|Q(staff__firstName__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
        }
        return render(request,'allifmaalcommonapp/hrm/salaries/salaries.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonSalaryAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonSalariesModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonSalariesModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonSalariesModel.objects.filter(company=main_sbscrbr_entity).order_by('-amount').first().amount
        scopes=CommonSalariesModel.objects.filter(company=main_sbscrbr_entity)
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonSalariesModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":

                    template_path = 'allifmaalcommonapp/payments/suppliers/supplier-payment-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
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
                elif selected_option=="excel":
                    compnyresource=commonBankWithdrawalResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/hrm/salaries/salaries.html',context)
                   
            else:
                allifqueryset=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity)
         
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
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
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
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonEditSalaryDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Salary Details"
        usrslg=request.user.customurlslug
        cmpslg=request.user.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=cmpslg).first()

        allifquery=CommonSalariesModel.objects.get(id=pk)
        form =CommonAddSalaryForm(main_sbscrbr_entity,instance=allifquery)#insert the content of the table stored in the selected id in the update form
        #we could have used the add customer form but the validation will refuse us to update since fields may exist
        if request.method == 'POST':
            form =CommonAddSalaryForm(main_sbscrbr_entity,request.POST, instance=allifquery)
            if form.is_valid():
               
                form.save()
                
                return redirect('allifmaalcommonapp:commonSalaries',allifusr=usrslg,allifslug=cmpslg)
                
        context = {
            'form':form,
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/hrm/salaries/add-salary.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_delete
def commonWantToDeleteSalary(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonSalariesModel.objects.filter(id=pk).first()
        myallifquery=CommonSalariesModel.objects.filter(id=pk).first()
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        "myallifquery":myallifquery,
        }
        return render(request,'allifmaalcommonapp/hrm/salaries/x-salary-confirm.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonDeleteSalary(request,pk,*allifargs,**allifkwargs):
    try:
        usrslg=request.user.customurlslug
        cmpslg=request.user.usercompany
        CommonSalariesModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonSalaries',allifusr=usrslg,allifslug=cmpslg)
        
    except:
        return render(request,'allifmaalapp/error.html')
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonPostSalary(request,pk,*allifargs,**allifkwargs):
    
    #try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()

        allifquery=CommonSalariesModel.objects.get(id=pk)
        emp_no=allifquery.staff.staffNo
        normal_salary=allifquery.amount#this gives the amount of salary given to the staff
        month_salary=allifquery.salary_payable
        pay_from_acc_id=allifquery.account.id
       
        CommonLedgerEntriesModel.objects.create(credit=month_salary,
        comments="payment",company=main_sbscrbr_entity,owner=request.user,ledgowner="staff")
        

        

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
            return redirect('allifmaalcommonapp:commonSalaries',allifusr=usrslg,allifslug=compslg)
    
        else:
            messgeone=messages.error(request, 'Please note that either Equity or Salaries or both accounts are missing in the chart of accounts.')
            messgetwo=messages.error(request, 'Add Equity and Salaries accounts in the Equity and Expenses categories respectively, if they are not already there, then post again.')
           
            return render(request,'allifmaalcommonapp/error/error.html')
            
       
    #except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonPostedSalaries(request,*allifargs,**allifkwargs):
    try:
        title="Posted Staff Salaries"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonSalariesModel.objects.filter(status="posted",company=main_sbscrbr_entity)
        context = {
            "title":title,
            "allifqueryset":allifqueryset,
        }

        return render(request,'allifmaalcommonapp/hrm/salaries/posted-salaries.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

################################ JOBS ############################
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonJobs(request,*allifargs,**allifkwargs):
    try:
        title="Jobs"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifqueryset=CommonJobsModel.objects.filter(company=main_sbscrbr_entity)
        context={
            "allifqueryset":allifqueryset,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/jobs/jobs.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

import datetime
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonNewJobs(request,*allifargs,**allifkwargs):
    compslg=request.user.usercompany
    usrslg=request.user.customurlslug
    logged_user=User.objects.filter(customurlslug=usrslg).first()
    main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
    logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
    logged_user_can_access_all=logged_user.can_access_all
    
    if logged_user_profile!=None:
        logged_user_division=logged_user_profile.division
        logged_user_branch=logged_user_profile.branch
        logged_user_department=logged_user_profile.department
    else:
        context={
            "logged_user":logged_user
        }
        return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
    
    current_datetime = datetime.datetime.now()
    job_year=current_datetime.year
    last_job= CommonJobsModel.objects.filter(company=main_sbscrbr_entity).order_by('id').last()
    last_obj=CommonJobsModel.objects.filter(company=main_sbscrbr_entity).last()
    if last_obj:
        last_obj_id=last_obj.id
        last_obj_incremented=last_obj_id+1
        jobNo= 'Job/'+str(uuid4()).split('-')[1]+'/'+str(last_obj_incremented)+'/'+str(job_year)
    else:
       jobNo= 'First/Job/'+str(uuid4()).split('-')[1]
    newJobRef=CommonJobsModel.objects.create(job_number=jobNo,description="Job Description",company=main_sbscrbr_entity,owner=logged_user,
                division=logged_user_division,branch=logged_user_branch,department=logged_user_department)
    newJobRef.save()
    return redirect('allifmaalcommonapp:commonJobs',allifusr=usrslg,allifslug=compslg)
    
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonJobSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonJobsModel.objects.filter((Q(job_number__icontains=allifsearch)
            |Q(description__icontains=allifsearch)|Q(customer__name__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
        }
        return render(request,'allifmaalcommonapp/jobs/jobs.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonJobAdvanceSearch(request,*allifargs,**allifkwargs):
    try:
        title="Advanced Search"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        allifqueryset=[]
       
        firstDate=CommonSupplierPaymentsModel.objects.filter(company=main_sbscrbr_entity).first().date
        lastDate=CommonSupplierPaymentsModel.objects.filter(company=main_sbscrbr_entity).last().date
        largestAmount=CommonSupplierPaymentsModel.objects.filter(company=main_sbscrbr_entity).order_by('-amount').first().amount
        scopes=CommonSupplierPaymentsModel.objects.filter(company=main_sbscrbr_entity)
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            start_date=request.POST.get('startdate',selected_option) or None
            end_date=request.POST.get('enddate') or None
            start_value=request.POST.get('startvalue') or None
            end_value=request.POST.get('endvalue') or None
            if start_date!="" or end_date!="" or start_value!="" or end_value!="":
                searched_data=CommonSupplierPaymentsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=main_sbscrbr_entity))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":

                    template_path = 'allifmaalcommonapp/jobs/job-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":main_sbscrbr_entity,
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
                elif selected_option=="excel":
                    compnyresource=commonBankWithdrawalResource()
                    dataset =compnyresource.export(searched_data)
                    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="zamzam-stock.xls"'
                    return response
                # if word is selected
                elif selected_option=="word":
                    pass

                # if something else is selected or none is selected
                else:
                    context = {
                    "searched_data":searched_data,
                    
                    "title":title,
                    "datasorts":datasorts,
                   "formats":formats,
                    }
                    return render(request,'allifmaalcommonapp/jobs/jobs.html',context)
                    
                   
            else:
                allifqueryset=CommonQuotesModel.objects.filter(company=main_sbscrbr_entity)
         
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/jobs/jobs.html',context)
            
        else:
            context={
            "allifqueryset":allifqueryset,
            "formats":formats,
            "title":title,
            "datashorts":datasorts,
            "formats":formats,
            }
            return render(request,'allifmaalcommonapp/jobs/jobs.html',context)
           
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonDeleteJob(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonJobsModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonJobs',allifusr=usrslg,allifslug=compslg)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
   
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonAddJobDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Job Details"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonJobsModel.objects.filter(id=pk).first()
        form=CommonAddJobDetailsForm(main_sbscrbr_entity,instance=allifquery)
        if request.method =='POST':
            form=CommonAddJobDetailsForm(main_sbscrbr_entity,request.POST,instance=allifquery)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.company=main_sbscrbr_entity
                add_item.owner=logged_user
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddJobDetails',pk=allifquery.id,allifusr=usrslg,allifslug=compslg)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
                
        context={
            "form":form,
            "title":title,
            "allifquery":allifquery,
        }
        return render(request,'allifmaalcommonapp/jobs/add-job-details.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
 
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonAddJobItems(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add Job Items"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonJobsModel.objects.filter(id=pk).first()
        form=CommonAddJobItemsForm(main_sbscrbr_entity)
        allifqueryset= CommonJobItemsModel.objects.filter(jobitemconnector=allifquery)#this line helps to
    
        add_item= None
        if request.method == 'POST':
            form=CommonAddJobItemsForm(main_sbscrbr_entity,request.POST)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.jobitemconnector=allifquery
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddJobItems',pk=allifquery.id,allifusr=usrslg,allifslug=compslg)
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)

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
    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_delete
def commonWantToDeleteJob(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonJobsModel.objects.filter(id=pk).first()
        myallifquery=CommonJobsModel.objects.filter(id=pk).first()
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        "myallifquery":myallifquery,
        }
        return render(request,'allifmaalcommonapp/jobs/add-job-details.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context) 

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
@logged_in_user_can_delete
def commonWantToDeleteJobItem(request,pk,*allifargs,**allifkwargs): 
    try:
        allifquery=CommonJobItemsModel.objects.filter(id=pk).first()
        myallifquery=CommonJobItemsModel.objects.filter(id=pk).first()
        title="Are you sure to delete"
        context={
        "title":title,
        "allifquery":allifquery,
        "myallifquery":myallifquery,
        }
        return render(request,'allifmaalcommonapp/jobs/add-job-items.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)    
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonDeleteJobItem(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        
        myallifquery=CommonJobItemsModel.objects.filter(id=pk).first()
        allifquery=myallifquery.jobitemconnector
        myallifquery.delete()
        return redirect('allifmaalcommonapp:commonAddJobItems',pk=allifquery.id,allifusr=usrslg,allifslug=compslg)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonInvoiceJob(request,pk,*allifargs,**allifkwargs):
    try:
        title="Invoice PDF"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonJobsModel.objects.filter(id=pk).first()
        form=CommonAddJobDetailsForm(main_sbscrbr_entity,instance=allifquery)
        
        allifqueryset=CommonJobItemsModel.objects.filter(jobitemconnector=allifquery)
    
        context={
        "allifquery":allifquery,
        "allifqueryset":allifqueryset,
            
        }
        
        return render(request,'allifmaalcommonapp/jobs/invoice-job.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonJobInvoicePdf(request,pk,*allifargs,**allifkwargs):
    try:
        title="Job Invoice Pdf"
        system_user=request.user
        my_job_id=CommonJobsModel.objects.get(id=pk)
        job_Items =CommonJobItemsModel.objects.filter(jobitemconnector=my_job_id)
        myuplift=0
    
        template_path = 'allifmaalcommonapp/jobs/job-inv-pdf.html'
    
        context={
            "my_job_id":my_job_id,
            "job_Items":job_Items,
            "myuplift":myuplift,
        
            "system_user":system_user,
            
            "title":title,
            
        }
        
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="Allifmaal-invoice.pdf"'
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


@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonJobTransactionReportpdf(request,pk,*allifargs,**allifkwargs):
    try:
        title="Job Transactions Report Pdf"
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
            #"alwenco":alwenco,
            "title":title,
            
        }
        
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="Job-Transactions.pdf"'
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
        
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


################################## TASKS ###########################################
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonTasks(request,*allifargs,**allifkwargs):
    try:
        title="To do list"
        formats=CommonDocsFormatModel.objects.all()
        datasorts=CommonDataSortsModel.objects.all()
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        logged_user_can_access_all=logged_user.can_access_all
        allifqueryset=CommonBanksModel.objects.filter(company=main_sbscrbr_entity)
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        
        form =CommonAddTasksForm(main_sbscrbr_entity,request.POST or None)
        allifqueryset=CommonTasksModel.objects.order_by('dueDate').filter(status="incomplete",company=main_sbscrbr_entity)
        completed_tasks=CommonTasksModel.objects.filter(status="complete")
        if form.is_valid():
            obj= form.save(commit=False)
            obj.company=main_sbscrbr_entity
            obj.owner=logged_user
            obj.save()
            form=CommonAddTasksForm(main_sbscrbr_entity)#this clears out the form after adding the product
            return redirect('allifmaalcommonapp:commonTasks',allifusr=usrslg,allifslug=compslg)
        if request.method=='POST':
            selected_option=request.POST.get('requiredformat')
            if selected_option=="ascending":
                allifqueryset=CommonTasksModel.objects.order_by('dueDate').filter(status="incomplete",company=main_sbscrbr_entity)
                
            else:
                allifqueryset=CommonTasksModel.objects.filter(status="incomplete",company=main_sbscrbr_entity)
            
        else:
            pass
           
        context = {
            "form":form,
            "allifqueryset":allifqueryset,
            "title":title,
            "completed_tasks":completed_tasks,
            "datasorts":datasorts,
            
        }

        return render(request,'allifmaalcommonapp/tasks/tasks.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonTaskBasicSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonTasksModel.objects.filter((Q(task__icontains=allifsearch)
            |Q(status__icontains=allifsearch)|Q(assignedto__firstName__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
        }
        return render(request,'allifmaalcommonapp/tasks/tasks.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@login_required(login_url='allifmaalusersapp:userLoginPage')
@logged_in_user_can_view
def commonTasksSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        user_var=request.user
        compslg=user_var.usercompany
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonTasksModel.objects.filter((Q(task__icontains=allifsearch)
            |Q(status__icontains=allifsearch)|Q(assignedto__firstName__icontains=allifsearch)) & Q(company=main_sbscrbr_entity))
           
            context={
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
            "main_sbscrbr_entity":main_sbscrbr_entity,
        }
        return render(request,'allifmaalcommonapp/tasks/tasks.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonAddSeeTaskDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Add And See Task Details"
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        allifquery=CommonTasksModel.objects.filter(id=pk).first()
        form=CommonAddTasksForm(main_sbscrbr_entity,instance=allifquery)
        if request.method =='POST':
            form=CommonAddTasksForm(main_sbscrbr_entity,request.POST,instance=allifquery)
            if form.is_valid():
                add_item= form.save(commit=False)
                add_item.company=main_sbscrbr_entity
                add_item.owner=logged_user
                add_item.save()
                return redirect('allifmaalcommonapp:commonAddSeeTaskDetails',pk=allifquery.id,allifusr=usrslg,allifslug=compslg)
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonMarkTaskComplete(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        mark_complete=CommonTasksModel.objects.filter(id=pk).first()
        if mark_complete.status=="incomplete":
            mark_complete.status="complete"
            mark_complete.save()
        
        else:
            mark_complete.status="incomplete"
            mark_complete.save()
        return redirect('allifmaalcommonapp:commonTasks',allifusr=usrslg,allifslug=compslg)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonCompletedTasks(request,*allifargs,**allifkwargs):
    try:
        title="Completed Tasks"
        tasks=CommonTasksModel.objects.filter(status="incomplete")
        allifqueryset=CommonTasksModel.objects.filter(status="complete")
        context = {
            "tasks":tasks,
            "title":title,
            "allifqueryset":allifqueryset,
        }

        return render(request,'allifmaalcommonapp/tasks/finished-tasks.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#@allowed_users(allowed_roles=['admin'])  
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonDeleteTask(request,pk,*allifargs,**allifkwargs):
    try:
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        CommonTasksModel.objects.get(id=pk).delete()
        return redirect('allifmaalcommonapp:commonTasks',allifusr=usrslg,allifslug=compslg)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonEditTask(request,pk,*allifargs,**allifkwargs):
    try:
        title="Edit Task"
        
        compslg=request.user.usercompany
        usrslg=request.user.customurlslug
        logged_user=User.objects.filter(customurlslug=usrslg).first()
        main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
        logged_user_profile=CommonEmployeesModel.objects.filter(username=logged_user,company=main_sbscrbr_entity).first()
        allifquery=CommonTasksModel.objects.filter(id=pk).first()
        allifqueryset=CommonTasksModel.objects.filter(company=main_sbscrbr_entity)
        if logged_user_profile!=None:
            logged_user_division=logged_user_profile.division
            logged_user_branch=logged_user_profile.branch
            logged_user_department=logged_user_profile.department
        else:
            return render(request,'allifmaalcommonapp/hrm/profiles/no-profile.html',context)
        
        form =CommonAddTasksForm(main_sbscrbr_entity,instance=allifquery)
        if request.method == 'POST':
            form = CommonAddTasksForm(main_sbscrbr_entity,request.POST, instance=allifquery)
            if form.is_valid():
                form.save()
                return redirect('allifmaalcommonapp:commonTasks',allifusr=usrslg,allifslug=compslg)
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonProfitAndLoss(request,*allifargs,**allifkwargs):
    try:
        title="Profit And Loss"
     
        latest=CommonInvoicesModel.objects.order_by('-date').filter(posting_inv_status='posted')[:7]
        totalsales=CommonInvoicesModel.objects.filter(posting_inv_status='posted').order_by('-invoice_total').aggregate(Sum('invoice_total'))['invoice_total__sum']
        totalrevenue=CommonChartofAccountsModel.objects.filter(code__lt=49999,code__gt=39999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        totalgoodscost=CommonInvoicesModel.objects.filter(posting_inv_status='posted').order_by('-invoice_items_total_cost').aggregate(Sum('invoice_items_total_cost'))['invoice_items_total_cost__sum']
        grossprofitorloss=totalsales-totalgoodscost
        #totalexpenses=totalgoodscost=AllifmaalExpensesModel.objects.all().order_by('-amount').aggregate(Sum('amount'))['amount__sum']
        totexpenses=CommonChartofAccountsModel.objects.filter(code__lt=59999,code__gt=49999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        netprofitorloss=grossprofitorloss-(totexpenses or 0)
        totalrevenue=CommonChartofAccountsModel.objects.filter(code__lt=49999,code__gt=39999).order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        #order_by('-amount').aggregate(Sum('amount'))['amount__sum']
        exps=CommonChartofAccountsModel.objects.filter(code__lt=59999,code__gt=49999)
    
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
        return render(request,'allifmaalusersapp/error/error.html',error_context)
  
######################################### REPORTS SECTION ############33
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonMainReports(request,*allifargs,**allifkwargs):
    try:
        title="Main Reports"
        context={
        "title":title,
        }
        return render(request,'allifmaalcommonapp/reports/reports.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonDebtorsReport(request,*allifargs,**allifkwargs):
    try:
        mydate=date.today()
        title="Debtors List"
        template_path = 'allifmaalcommonapp/reports/debtors-report.html'#this is the template to be converted to pdf
        customers=CommonCustomersModel.objects.filter(balance__gte=1)
        context = {
        "customers":customers,
        "mydate":mydate,
        "title":title,
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

@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonCreditorsReportpdf(request,*allifargs,**allifkwargs):
    try:
        title="Creditors List"
        mydate=date.today()
        system_user=request.user
        creditors=CommonSuppliersModel.objects.filter(balance__gte=1)
        template_path = 'allifmaalcommonapp/reports/creditors-report.html'
       
        context = {
        "system_user":system_user,
        "creditors":creditors,
        
        "mydate":mydate,
        "title":title,
    
        }
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="creditors-report.pdf"'
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
@login_required(login_url='allifmaalusersapp:userLoginPage') 
@logged_in_user_can_view 
def commonAvailableStockpdf(request,*allifargs,**allifkwargs):
    try:
        title="Available Stock List"
        mydate=date.today()
        system_user=request.user
        stocks=CommonStocksModel.objects.filter(quantity__gte=1)
        template_path = 'allifmaalcommonapp/reports/available-stock-report.html'
        context = {
        "system_user":system_user,
        "stocks":stocks,
        "mydate":mydate,
        "title":title,
        }
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="available-stock-report.pdf"'
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

        context={}
        return render(request,"allifmaalcommonapp/website/website.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalusersapp/error/error.html',error_context)






def ui1(request,*allifargs,**allifkwargs):
    print()
    context = {
           
        }
    return render(request,'allifmaalcommonapp/ui/ui1.html',context)
def ui2(request,*allifargs,**allifkwargs):
    print()
    context = {
           
        }
    return render(request,'allifmaalcommonapp/ui/ui2.html',context)
def ui3(request,*allifargs,**allifkwargs):
    print()
    context = {
           
        }
    return render(request,'allifmaalcommonapp/ui/ui3.html',context)
def ui4(request,*allifargs,**allifkwargs):
    print()
    context = {
           
        }
    return render(request,'allifmaalcommonapp/ui/ui4.html',context)

def ui6(request,*allifargs,**allifkwargs):
    print()
    context ={

        }
    return render(request,'allifmaalcommonapp/ui/ui6.html',context)
def ui7(request,*allifargs,**allifkwargs):
    print()
    context = {
           
        }
    return render(request,'allifmaalcommonapp/ui/ui7.html',context)
def ui8(request,*allifargs,**allifkwargs):
    print()
    context = {
           
        }
    return render(request,'allifmaalcommonapp/ui/ui8.html',context)

#################### testingl inks

from .models import TemplateLink
from .forms import TemplateLinkForm

def link_list(request):
    for item in TemplateLink.objects.all():
        #item.delete()
        pass
    links = TemplateLink.objects.all()
    return render(request, 'allifmaalcommonapp/links/link_list.html', {'links': links})

def add_link(request):
    if request.method == 'POST':
        form = TemplateLinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allifmaalcommonapp:link_list')
    else:
        form = TemplateLinkForm()
    return render(request, 'allifmaalcommonapp/links/add_link.html', {'form': form})

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
            form = CommonAddSectorForm(data)
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

    return render(request, 'allifmaalcommonapp/dynamic_form.html')