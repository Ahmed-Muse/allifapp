from django.shortcuts import render,redirect
from allifmaalcommonapp.allifutils import common_shared_data
from allifmaalcommonapp.decorators import subscriber_company_status,logged_in_user_must_have_profile
from allifmaalcommonapp.decorators import *
from allifmaalcommonapp.models import CommonCompanyScopeModel
# Create your views here.
from .models import *
from django.template.loader import get_template
from django.db.models import Q
from xhtml2pdf import pisa
from django.utils import timezone
from django.shortcuts import render
from .forms import *
from django.db.models import Q
# Create your views here.
#@logged_in_user_must_have_profile
#@subscriber_company_status
def shaafiHome(request,*allifargs,**allifkwargs):
    title="Home : Healthcare"
    try:
        user_is_supper=request.user.is_superuser
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_profile") is not None:
            context={"title":title,"user_is_supper":user_is_supper,}
            return render(request,"allifmaalshaafiapp/home/home.html",context)
        else:
            return redirect('allifmaalcommonapp:commonAddStaffProfile',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
   
def shaafiDashboard(request,*allifargs,**allifkwargs):
    try:
        title="Dashboard : Hospitality"
        user_var=request.user
        user_role=user_var.allifmaal_admin
        user_is_supper=request.user.is_superuser
        context={
            "title":title,
            "user_var":user_var,
            "user_is_supper":user_is_supper,
        }
        return render(request,"allifmaalshaafiapp/dashboard/dashboard.html",context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

############### prescriptions and medications #############

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin
def prescriptions(request,*allifargs,**allifkwargs):
    title="Medication Prescriptions"
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=MedicationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=MedicationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=MedicationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=MedicationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={"title":title,"allifqueryset":allifqueryset,}
        return render(request,'allifmaalshaafiapp/medication/prescriptions/prescriptions.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
@logged_in_user_is_admin
def AddPrescription(request,*allifargs,**allifkwargs):
    title="Add New Prescription"
    try:
        allif_data=common_shared_data(request)
        form=AddPrescriptionForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=AddPrescriptionForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalshaafiapp:prescriptions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
               
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=AddPrescriptionForm(allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalshaafiapp/medication/prescriptions/add_prescription.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_is_admin
def EditPrescription(request,pk,*allifargs,**allifkwargs):
    title="Update Prescription Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=MedicationsModel.objects.filter(id=pk).first()
        form=AddPrescriptionForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=AddPrescriptionForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalshaafiapp:prescriptions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=AddPrescriptionForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalshaafiapp/medication/prescriptions/add_prescription.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def prescriptionSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=MedicationsModel.objects.filter((Q(description__icontains=allifsearch)|Q(trans_number__number__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        
        else:
            searched_data=[]

        context={
        
        "title":title,
        "searched_data":searched_data,
        
        }
        return render(request,'allifmaalshaafiapp/medication/prescriptions/prescriptions.html',context)
    
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def prescriptionAdvancedSearch(request,*allifargs,**allifkwargs):
    try:
        title="Purchase Order Advanced Search Results"
        allif_data=common_shared_data(request)
       
        allifqueryset=[]
       
        firstDate=MedicationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
        lastDate=MedicationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
        largestAmount=MedicationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-amount').first().amount

        scopes=CommonCompanyScopeModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-date')[:4]

        current_date=timezone.now().date().today()
        firstDate=current_date
        lastDate=current_date
        largestAmount=0
        searched_data=[]
        firstDepo=MedicationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first()
    
        lastDepo=MedicationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last()
        if firstDepo and lastDepo:
            firstDate=MedicationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).first().date
            lastDate=MedicationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).last().date
            largestAmount=MedicationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity")).order_by('-amount').first().amount
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
                searched_data=MedicationsModel.objects.filter(Q(date__gte=start_date or firstDate) & Q(date__lte=end_date or lastDate) & Q(amount__gte=start_value or 0) & Q(amount__lte=end_value or largestAmount) & Q(company=allif_data.get("main_sbscrbr_entity")))
                #searched_data=CommonShareholderBankDepositsModel.objects.filter(Q(date__gte=start_date or date_today) & Q(company=main_sbscrbr_entity))
                # if pdf is selected
                if selected_option=="pdf":
                    template_path = 'allifmaalcommonapp/purchases/po-search-pdf.html'
                    allifcontext = {
                    "searched_data":searched_data,
                    "title":title,
                    "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
                 
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
                    return render(request,'allifmaalshaafiapp/medication/prescriptions/prescriptions.html',context)
                   
            else:
                searched_data=[]
              
                context={
                    "searched_data":searched_data,
            
                }
                return render(request,'allifmaalshaafiapp/medication/prescriptions/prescriptions.html',context)
              
        else:
            context={
            "allifqueryset":allifqueryset,
           
            "title":title,
           
            }
            return render(request,'allifmaalshaafiapp/medication/prescriptions/prescriptions.html',context)
           
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
         
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def prescriptionDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Prescription Details"
        allifquery=MedicationsModel.objects.filter(id=pk).first()
      
        context={
            "allifquery":allifquery,
            "title":title,
          
        }
        return render(request,'allifmaalshaafiapp/medication/prescriptions/prescription_details.html',context)
    
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_departmental_delete
@logged_in_user_can_delete
def wantToDeletePrescription(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=MedicationsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalshaafiapp/medication/prescriptions/delete_prescription_confirm.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_universal_delete
@logged_in_user_can_delete
def deletePrescription(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        MedicationsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalshaafiapp:prescriptions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)



####################### admissions ##################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin
def admissions(request,*allifargs,**allifkwargs):
    title="Admissions"
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=AdmissionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=AdmissionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=AdmissionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=AdmissionsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={"title":title,"allifqueryset":allifqueryset,}
        return render(request,'allifmaalshaafiapp/medication/admissions/admissions.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
@logged_in_user_is_admin
def addAdmission(request,*allifargs,**allifkwargs):
    title="Add New Admission"
    try:
        allif_data=common_shared_data(request)
        form=AddAdmissionForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=AddAdmissionForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalshaafiapp:admissions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
               
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=AddAdmissionForm(allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalshaafiapp/medication/admissions/add_admission.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_is_admin
def EditAdmission(request,allifusr,pk,*allifargs,**allifkwargs):
    title="Update Prescription Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=AdmissionsModel.objects.filter(id=pk).first()
        form=AddAdmissionForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=AddAdmissionForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:admissions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=AddAdmissionForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalshaafiapp/medication/admissions/add_admission.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def admissionSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=AdmissionsModel.objects.filter((Q(description__icontains=allifsearch)|Q(trans_number__number__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        
        else:
            searched_data=[]

        context={
        
        "title":title,
        "searched_data":searched_data,
        
        }
        return render(request,'allifmaalshaafiapp/medication/admissions/admissions.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def admissionDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Prescription Details"
        allifquery=AdmissionsModel.objects.filter(id=pk).first()
      
        context={
            "allifquery":allifquery,
            "title":title,
          
        }
        return render(request,'allifmaalshaafiapp/medication/admissions/admission_details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_departmental_delete
@logged_in_user_can_delete
def wantToDeleteAdmission(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=AdmissionsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalshaafiapp/medication/admissions/delete_admission_confirm.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_universal_delete
@logged_in_user_can_delete
def deleteAdmission(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        AdmissionsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalshaafiapp:admissions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)


##################3 medical adminstrations ############


@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin
def treatments(request,*allifargs,**allifkwargs):
    title="Treatments"
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=MedicalAdministrationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=MedicalAdministrationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=MedicalAdministrationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=MedicalAdministrationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={"title":title,"allifqueryset":allifqueryset,}
        return render(request,'allifmaalshaafiapp/medication/prescriptions/treatments/treatments.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
@logged_in_user_is_admin
def addTreatment(request,*allifargs,**allifkwargs):
    title="Add and Give New Treatment"
    try:
        allif_data=common_shared_data(request)
        form=AddMedicalAdminstrationForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=AddMedicalAdminstrationForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalshaafiapp:treatments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
               
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=AddMedicalAdminstrationForm(allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalshaafiapp/medication/prescriptions/treatments/add_treatment.html',context)
    
        return render(request,'allifmaalshaafiapp/medication/referrals/add_referral.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_is_admin
def EditTreatment(request,allifusr,pk,*allifargs,**allifkwargs):
    title="Update Referral Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=MedicalAdministrationsModel.objects.filter(id=pk).first()
        form=AddMedicalAdminstrationForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=AddMedicalAdminstrationForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalshaafiapp:treatments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=AddReferralForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalshaafiapp/medication/prescriptions/treatments/add_treatment.html',context)
    
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def treatmentSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=MedicalAdministrationsModel.objects.filter((Q(description__icontains=allifsearch)|Q(trans_number__number__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        
        else:
            searched_data=[]

        context={
        
        "title":title,
        "searched_data":searched_data,
        
        }
        return render(request,'allifmaalshaafiapp/medication/prescriptions/treatments/treatments.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def treatmentDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Prescription Details"
        allifquery=MedicalAdministrationsModel.objects.filter(id=pk).first()
      
        context={
            "allifquery":allifquery,
            "title":title,
          
        }
        return render(request,'allifmaalshaafiapp/medication/prescriptions/treatments/treatment_details.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_departmental_delete
@logged_in_user_can_delete
def wantToDeleteTreatment(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=MedicalAdministrationsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalshaafiapp/medication/prescriptions/treatments/delete_treatment_confirm.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_universal_delete
@logged_in_user_can_delete
def deleteTreatment(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        MedicalAdministrationsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalshaafiapp:treatments',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    

#################3 discharges ##############

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin
def discharges(request,*allifargs,**allifkwargs):
    title="Referrals"
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=DischargesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=DischargesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=DischargesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=DischargesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={"title":title,"allifqueryset":allifqueryset,}
        return render(request,'allifmaalshaafiapp/medication/admissions/discharge/discharges.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
@logged_in_user_is_admin
def addDischarge(request,*allifargs,**allifkwargs):
    title="Add New Discharge"
    try:
        allif_data=common_shared_data(request)
        form=AddDischargeForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=AddDischargeForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalshaafiapp:discharges',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
               
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=AddDischargeForm(allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalshaafiapp/medication/admissions/discharge/add_discharge.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_is_admin
def EditDischarge(request,allifusr,pk,*allifargs,**allifkwargs):
    title="Update Discharge Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=DischargesModel.objects.filter(id=pk).first()
        form=AddDischargeForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=AddDischargeForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalshaafiapp:discharges',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=AddReferralForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalshaafiapp/medication/admissions/discharge/add_discharge.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def dischargeSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=DischargesModel.objects.filter((Q(description__icontains=allifsearch)|Q(trans_number__number__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        
        else:
            searched_data=[]

        context={
        
        "title":title,
        "searched_data":searched_data,
        
        }
        return render(request,'allifmaalshaafiapp/medication/admissions/discharge/discharges.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def dischargeDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Prescription Details"
        allifquery=DischargesModel.objects.filter(id=pk).first()
      
        context={
            "allifquery":allifquery,
            "title":title,
          
        }
        return render(request,'allifmaalshaafiapp/medication/admissions/discharge/discharge_details.html',context)
    
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_departmental_delete
@logged_in_user_can_delete
def wantToDeleteDischarge(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=ReferralsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalshaafiapp/medication/admissions/discharge/delete_discharge_confirm.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_universal_delete
@logged_in_user_can_delete
def deleteDischarge(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        DischargesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalshaafiapp:discharges',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)




####################### referals ##################

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
@logged_in_user_is_admin
def referrals(request,*allifargs,**allifkwargs):
    title="Referrals"
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=ReferralsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=ReferralsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=ReferralsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=ReferralsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
        context={"title":title,"allifqueryset":allifqueryset,}
        return render(request,'allifmaalshaafiapp/medication/referrals/referrals.html',context)
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
@logged_in_user_is_admin
def addReferral(request,*allifargs,**allifkwargs):
    title="Add New Referral"
    try:
        allif_data=common_shared_data(request)
        form=AddReferralForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=AddReferralForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalshaafiapp:referrals',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
               
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=AddReferralForm(allif_data.get("main_sbscrbr_entity"))
        context = {
            "title":title,
            "form":form,
        }
        return render(request,'allifmaalshaafiapp/medication/referrals/add_referral.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_is_admin
def EditReferral(request,allifusr,pk,*allifargs,**allifkwargs):
    title="Update Referral Details"
    try:
        allif_data=common_shared_data(request)
        allifquery_update=ReferralsModel.objects.filter(id=pk).first()
        form=AddReferralForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=AddReferralForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:admissions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=AddReferralForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalshaafiapp/medication/referrals/add_referral.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def referralSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=ReferralsModel.objects.filter((Q(description__icontains=allifsearch)|Q(trans_number__number__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        
        else:
            searched_data=[]

        context={
        
        "title":title,
        "searched_data":searched_data,
        
        }
        return render(request,'allifmaalshaafiapp/medication/referrals/referrals.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
def referralDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Prescription Details"
        allifquery=ReferralsModel.objects.filter(id=pk).first()
      
        context={
            "allifquery":allifquery,
            "title":title,
          
        }
        return render(request,'allifmaalshaafiapp/medication/referrals/referral_details.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_departmental_delete
@logged_in_user_can_delete
def wantToDeleteReferral(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=ReferralsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalshaafiapp/medication/referrals/delete_referral_confirm.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)    

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_is_admin
@logged_in_user_has_universal_delete
@logged_in_user_can_delete
def deleteReferral(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        ReferralsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalshaafiapp:referrals',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)