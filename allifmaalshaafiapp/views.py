from django.shortcuts import render,redirect,get_object_or_404
from allifmaalcommonapp.allifutils import common_shared_data
from allifmaalcommonapp.decorators import subscriber_company_status,logged_in_user_must_have_profile
from allifmaalcommonapp.decorators import *
from allifmaalcommonapp.models import CommonCompanyScopeModel,CommonDataSortsModel
# Create your views here...20200 lines...
from .models import *
from django.template.loader import get_template
from django.db.models import Q
from xhtml2pdf import pisa
from django.utils import timezone
from django.shortcuts import render
from .forms import *
from django.db.models import Q
from allifmaalcommonapp.utils import allif_filtered_and_sorted_queryset # Import the new helper function
from allifmaalcommonapp.models import CommonDocsFormatModel
from allifmaalcommonapp.utils import  (allif_filtered_and_sorted_queryset,allif_common_detail_view,allif_main_models_registry,allif_delete_hanlder,allif_common_form_submission_and_save,
allif_common_form_edit_and_save,allif_redirect_based_on_sector,allif_delete_confirm,allif_excel_upload_handler,allif_search_handler, allif_advance_search_handler,allif_document_pdf_handler)
# ... (existing imports) ...
# Create your views here.
#@logged_in_user_must_have_profile
#@subscriber_company_status
def shaafiHome(request,*allifargs,**allifkwargs):
    company=request.user.company
    sector=company.sector
    title=f"Home : {sector} " +''+ str(company)
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
        title="Dashboard : Healthcare"
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

##################3 Triage ####################
@allif_base_view_wrapper
def triageData(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Triage Records"
    formats=CommonDocsFormatModel.all_objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,TriagesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalshaafiapp/triage/triage_data.html',context)

@allif_base_view_wrapper
def AddTriageData(request,pk,*allifargs,**allifkwargs):
    allifquery= get_object_or_404(CommonTransactionsModel, id=pk) 
    allifquery_id=allifquery.id
    def transaction_item_pre_save(obj, request, allif_data):
        obj.medical_file=allifquery
    my_extra_context={"allifquery":allifquery,}
    return allif_common_form_submission_and_save(request,form_class=AddTriageDetailsForm,title_text="New Triage",
        success_redirect_url_name='AddTriageData',template_path='allifmaalshaafiapp/triage/add_triage_data.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=allifquery_id,
        extra_context=my_extra_context,app_namespace='allifmaalshaafiapp',)
 
@allif_base_view_wrapper
def editTriageData(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,AddTriageDetailsForm,"Edit",
    'editTriageData','allifmaalshaafiapp/triage/add_triage_data.html',
    redirect_with_pk=True,redirect_pk_value=pk,app_namespace='allifmaalshaafiapp',)

@allif_base_view_wrapper
def triageDataDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=TriagesModel,pk=pk,
        template_name='allifmaalshaafiapp/triage/triage_data_details.html', # Create this template
        title_map={'default': 'Triage Details'},)

@allif_base_view_wrapper
def triageDataSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='TriagesModel',search_fields_key='TriagesModel',
    template_path='allifmaalshaafiapp/triage/triage_data.html',search_input_name='allifsearchcommonfieldname',)

@allif_base_view_wrapper
def triageDataAdvancedSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='TriagesModel',advanced_search_config_key='TriagesModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalshaafiapp/triage/triage_data.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def wantToDeleteTriageData(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,TriagesModel,"Delete this item",
    'allifmaalshaafiapp/triage/delete_triage_data_confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def deleteTriageData(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='TriagesModel',
    pk=pk,success_redirect_url_name='triageData',app_namespace='allifmaalshaafiapp',)

######################### doctor assessments/observations #######################
@allif_base_view_wrapper
def doctorAssessments(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Assessments"
    formats=CommonDocsFormatModel.all_objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,AssessmentsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalshaafiapp/assessments/doctor_assessments.html',context)

@allif_base_view_wrapper
def addDoctorAssessment(request,pk,*allifargs,**allifkwargs):
    allifquery= get_object_or_404(CommonTransactionsModel, id=pk) 
    allifquery_id=allifquery.id
    def transaction_item_pre_save(obj, request, allif_data):
        obj.medical_file=allifquery
    my_extra_context={"allifquery":allifquery,}
    return allif_common_form_submission_and_save(request,form_class=AddAssessmentDetailsForm,
    title_text="New Assessment",
        success_redirect_url_name='addDoctorAssessment',
        template_path='allifmaalshaafiapp/assessments/add-assessment.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=allifquery_id,
        extra_context=my_extra_context,app_namespace='allifmaalshaafiapp',)
 
@allif_base_view_wrapper
def editDoctorAssessment(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,AddAssessmentDetailsForm,"Edit",
    'editDoctorAssessment','allifmaalshaafiapp/assessments/add-assessment.html',
    redirect_with_pk=True,redirect_pk_value=pk,app_namespace='allifmaalshaafiapp',)

@allif_base_view_wrapper
def doctorAssessmentSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='AssessmentsModel',search_fields_key='AssessmentsModel',
    template_path='allifmaalshaafiapp/assessments/doctor_assessments.html',search_input_name='allifsearchcommonfieldname',)

@allif_base_view_wrapper
def doctorAssessmentAdvancedSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='AssessmentsModel',advanced_search_config_key='AssessmentsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalshaafiapp/assessments/doctor_assessments.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def wantToDeleteDoctorAssessment(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,AssessmentsModel,"Delete this item",
    'allifmaalshaafiapp/assessments/delete_assessment_confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def deleteDoctorAssessment(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='AssessmentsModel',
    pk=pk,success_redirect_url_name='doctorAssessments',app_namespace='allifmaalshaafiapp',)

####################3 lab test requests ###################
@allif_base_view_wrapper
def labTestRequests(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Lab Test Requests"
    formats=CommonDocsFormatModel.all_objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,LabTestRequestsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalshaafiapp/assessments/labtests/requests/lab_test_requests.html',context)

@allif_base_view_wrapper
def addLabTestRequest(request,pk,*allifargs,**allifkwargs):
    allifquery= get_object_or_404(CommonTransactionsModel, id=pk) 
    allifquery_id=allifquery.id
    def transaction_item_pre_save(obj, request, allif_data):
        obj.medical_file=allifquery
    my_extra_context={"allifquery":allifquery,}
    return allif_common_form_submission_and_save(request,form_class=AddLabTestRequestForm,
    title_text="New Test",
        success_redirect_url_name='addLabTestRequest',
        template_path='allifmaalshaafiapp/assessments/labtests/requests/add_lab_test_request.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=allifquery_id,
        extra_context=my_extra_context,app_namespace='allifmaalshaafiapp',)
 
@allif_base_view_wrapper
def editLabTestRequest(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,AddLabTestRequestForm,"Edit Test",
    'editLabTestRequest','allifmaalshaafiapp/assessments/labtests/requests/add_lab_test_request.html',
    redirect_with_pk=True,redirect_pk_value=pk,app_namespace='allifmaalshaafiapp',)

@allif_base_view_wrapper
def labTestRequestDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=LabTestRequestsModel,pk=pk,
        template_name='allifmaalshaafiapp/assessments/labtests/requests/lab_test_request_details.html', # Create this template
        title_map={'default': 'Test Details'},)

@allif_base_view_wrapper
def labTestRequestSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='LabTestRequestsModel',search_fields_key='LabTestRequestsModel',
    template_path='allifmaalshaafiapp/assessments/labtests/requests/lab_test_requests.html',search_input_name='allifsearchcommonfieldname',)

@allif_base_view_wrapper
def labTestRequestAdvancedSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='LabTestRequestsModel',advanced_search_config_key='LabTestRequestsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalshaafiapp/assessments/labtests/requests/lab_test_requests.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def wantToDeleteLabTestRequest(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,LabTestRequestsModel,"Delete this item",
    'allifmaalshaafiapp/assessments/labtests/requests/delete_lab_test_request_confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def deleteLabTestRequest(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='LabTestRequestsModel',
    pk=pk,success_redirect_url_name='labTestRequests',app_namespace='allifmaalshaafiapp',)

#########################3 lab test request results sections ..####################3
@allif_base_view_wrapper
def labTestResults(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
 
    title="Test Results"
    formats=CommonDocsFormatModel.all_objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,LabTestResultsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalshaafiapp/assessments/labtests/results/lab_test_results.html',context)

    
@allif_base_view_wrapper
def addLabTestResult(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    allifquery=get_object_or_404(LabTestRequestsModel, id=pk)
    allifqueryset=LabTestResultsModel.all_objects.filter(test_request=allifquery)
   
    def transaction_item_pre_save(obj, request, allif_data):
        obj.test_request=allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset}
    return allif_common_form_submission_and_save(request,form_class=AddLabTestResultForm,
        title_text="Lab Test Results",
        success_redirect_url_name='addLabTestResult', # This URL expects a PK
        template_path='allifmaalshaafiapp/assessments/labtests/results/add_lab_test_result.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context)
    
 
@allif_base_view_wrapper
def editLabTestResult(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,AddLabTestResultForm,"Edit Result",
    'editLabTestResult','allifmaalshaafiapp/assessments/labtests/results/add_lab_test_result.html',
    redirect_with_pk=True,redirect_pk_value=pk,app_namespace='allifmaalshaafiapp',)

@allif_base_view_wrapper
def labTestResultDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=LabTestResultsModel,pk=pk,
        template_name='allifmaalshaafiapp/assessments/labtests/results/lab_test_result_details.html', # Create this template
        title_map={'default': 'Result Details'},)

@allif_base_view_wrapper
def labTestResultSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='LabTestResultsModel',search_fields_key='LabTestResultsModel',
    template_path='allifmaalshaafiapp/assessments/labtests/results/lab_test_results.html',search_input_name='allifsearchcommonfieldname',)

@allif_base_view_wrapper
def labTestResultAdvancedSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='LabTestResultsModel',advanced_search_config_key='LabTestResultsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalshaafiapp/assessments/labtests/results/lab_test_results.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def wantToDeleteLabTestResult(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,LabTestResultsModel,"Delete this item",
    'allifmaalshaafiapp/assessments/labtests/results/delete_lab_test_result_confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def deleteLabTestResult(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='LabTestResultsModel',
    pk=pk,success_redirect_url_name='labTestResults',app_namespace='allifmaalshaafiapp',)

############### prescriptions and medications #############
@allif_base_view_wrapper
def prescriptions(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Prescriptions"
    formats=CommonDocsFormatModel.all_objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,MedicationsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalshaafiapp/medication/prescriptions/prescriptions.html',context)


@allif_base_view_wrapper
def AddPrescription(request,pk,*allifargs,**allifkwargs):
    allifquery=get_object_or_404(CommonTransactionsModel, id=pk)
    allifqueryset=MedicationsModel.all_objects.filter(medical_file=allifquery)
   
    def transaction_item_pre_save(obj, request, allif_data):
        obj.medical_file=allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset}
    return allif_common_form_submission_and_save(request,form_class=AddPrescriptionForm,
        title_text="New Prescription",
        success_redirect_url_name='addLabTestResult', # This URL expects a PK
        template_path='allifmaalshaafiapp/medication/prescriptions/add_prescription.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context)
    
@allif_base_view_wrapper
def EditPrescription(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,AddPrescriptionForm,"Edit Prescription",
    'EditPrescription','allifmaalshaafiapp/medication/prescriptions/add_prescription.html',
    redirect_with_pk=True,redirect_pk_value=pk,app_namespace='allifmaalshaafiapp',)

@allif_base_view_wrapper
def prescriptionDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=MedicationsModel,pk=pk,
        template_name='allifmaalshaafiapp/medication/prescriptions/prescription_details.html', # Create this template
        title_map={'default': 'Prescription Details'},)

@allif_base_view_wrapper
def prescriptionSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='MedicationsModel',search_fields_key='MedicationsModel',
    template_path='allifmaalshaafiapp/medication/prescriptions/prescriptions.html',search_input_name='allifsearchcommonfieldname',)

@allif_base_view_wrapper
def prescriptionAdvancedSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='MedicationsModel',advanced_search_config_key='MedicationsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalshaafiapp/medication/prescriptions/prescriptions.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def wantToDeletePrescription(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,MedicationsModel,"Delete this item",
    'allifmaalshaafiapp/medication/prescriptions/delete_prescription_confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def deletePrescription(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='MedicationsModel',
    pk=pk,success_redirect_url_name='prescriptions',app_namespace='allifmaalshaafiapp',)

####################### admissions ##################
@allif_base_view_wrapper
def admissions(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Admissions"
    formats=CommonDocsFormatModel.all_objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,AdmissionsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalshaafiapp/medication/admissions/admissions.html',context)

@allif_base_view_wrapper
def addAdmission(request,pk,*allifargs,**allifkwargs):
    allifquery=get_object_or_404(CommonTransactionsModel, id=pk) 
    allifquery_id=allifquery.id
    def transaction_item_pre_save(obj, request, allif_data):
        obj.medical_file=allifquery
    my_extra_context={"allifquery":allifquery,}
    return allif_common_form_submission_and_save(request,form_class=AddAdmissionForm,
    title_text="New Admission",
        success_redirect_url_name='addAdmission',
        template_path='allifmaalshaafiapp/medication/admissions/add_admission.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=allifquery_id,
        extra_context=my_extra_context,app_namespace='allifmaalshaafiapp',)
 
@allif_base_view_wrapper
def EditAdmission(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,AddAdmissionForm,"Edit Admission",
    'EditAdmission','allifmaalshaafiapp/medication/admissions/add_admission.html',
    redirect_with_pk=True,redirect_pk_value=pk,app_namespace='allifmaalshaafiapp',)

@allif_base_view_wrapper
def admissionDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=AdmissionsModel,pk=pk,
        template_name='allifmaalshaafiapp/medication/admissions/admission_details.html', # Create this template
        title_map={'default': 'Admission Details'},)

@allif_base_view_wrapper
def admissionSearch(request,*allifargs,**allifkwargs): 
    return allif_search_handler(request,model_name='AdmissionsModel',search_fields_key='AdmissionsModel',
    template_path='allifmaalshaafiapp/medication/admissions/admissions.html',search_input_name='allifsearchcommonfieldname',)

@allif_base_view_wrapper
def addmissionAdvancedSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='AdmissionsModel',advanced_search_config_key='AdmissionsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalshaafiapp/medication/admissions/admissions.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def wantToDeleteAdmission(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,AdmissionsModel,"Delete this item",
    'allifmaalshaafiapp/medication/admissions/delete_admission_confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def deleteAdmission(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='AdmissionsModel',
    pk=pk,success_redirect_url_name='admissions',app_namespace='allifmaalshaafiapp',)


##################3 medical adminstrations ############
@allif_base_view_wrapper
def treatments(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Treatments"
    formats=CommonDocsFormatModel.all_objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,MedicalAdministrationsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalshaafiapp/medication/prescriptions/treatments/treatments.html',context)

@allif_base_view_wrapper
def addTreatment(request,pk,*allifargs,**allifkwargs):
    allifquery=get_object_or_404(MedicationsModel, id=pk) 
    allifquery_id=allifquery.id
    def transaction_item_pre_save(obj, request, allif_data):
        obj.prescription=allifquery
    my_extra_context={"allifquery":allifquery,}
    return allif_common_form_submission_and_save(request,form_class=AddMedicalAdminstrationForm,
    title_text="New Treatment",
        success_redirect_url_name='addTreatment',
        template_path='allifmaalshaafiapp/medication/prescriptions/treatments/add_treatment.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=allifquery_id,
        extra_context=my_extra_context,app_namespace='allifmaalshaafiapp',)
 
@allif_base_view_wrapper
def EditTreatment(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,AddMedicalAdminstrationForm,"Edit",
    'EditTreatment','allifmaalshaafiapp/medication/prescriptions/treatments/add_treatment.html',
    redirect_with_pk=True,redirect_pk_value=pk,app_namespace='allifmaalshaafiapp',)

@allif_base_view_wrapper
def treatmentDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=MedicalAdministrationsModel,pk=pk,
        template_name='allifmaalshaafiapp/medication/prescriptions/treatments/treatment_details.html', # Create this template
        title_map={'default': 'Treatment Details'},)

@allif_base_view_wrapper
def treatmentSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='MedicalAdministrationsModel',search_fields_key='MedicalAdministrationsModel',
    template_path='allifmaalshaafiapp/medication/prescriptions/treatments/treatments.html',search_input_name='allifsearchcommonfieldname',)

@allif_base_view_wrapper
def treatmentAdvancedSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='MedicalAdministrationsModel',advanced_search_config_key='MedicalAdministrationsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalshaafiapp/medication/prescriptions/treatments/treatments.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def wantToDeleteTreatment(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,MedicalAdministrationsModel,"Delete this item",
    'allifmaalshaafiapp/medication/prescriptions/treatments/delete_treatment_confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def deleteTreatment(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='MedicalAdministrationsModel',
    pk=pk,success_redirect_url_name='treatments',app_namespace='allifmaalshaafiapp',)

#################3 discharges ##############
@allif_base_view_wrapper
def discharges(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Discharges"
    formats=CommonDocsFormatModel.all_objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,DischargesModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalshaafiapp/medication/admissions/discharge/discharges.html',context)

@allif_base_view_wrapper
def addDischarge(request,pk,*allifargs,**allifkwargs):
    allifquery=get_object_or_404(AdmissionsModel, id=pk) 
    allifquery_id=allifquery.id
    def transaction_item_pre_save(obj, request, allif_data):
        obj.admission=allifquery
    my_extra_context={"allifquery":allifquery,}
    return allif_common_form_submission_and_save(request,form_class=AddDischargeForm,
    title_text="New Discharge",
        success_redirect_url_name='addTreatment',
        template_path='allifmaalshaafiapp/medication/admissions/discharge/add_discharge.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=allifquery_id,
        extra_context=my_extra_context,app_namespace='allifmaalshaafiapp',)
 
@allif_base_view_wrapper
def EditDischarge(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,AddDischargeForm,"Edit",
    'EditDischarge','allifmaalshaafiapp/medication/admissions/discharge/add_discharge.html',
    redirect_with_pk=True,redirect_pk_value=pk,app_namespace='allifmaalshaafiapp',)

@allif_base_view_wrapper
def dischargeDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=DischargesModel,pk=pk,
        template_name='allifmaalshaafiapp/medication/admissions/discharge/discharge_details.html', # Create this template
        title_map={'default': 'Discharge Details'},)

@allif_base_view_wrapper
def dischargeSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='DischargesModel',search_fields_key='DischargesModel',
    template_path='allifmaalshaafiapp/medication/admissions/discharge/discharges.html',search_input_name='allifsearchcommonfieldname',)

@allif_base_view_wrapper
def dischargeAdvancedSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='DischargesModel',advanced_search_config_key='DischargesModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalshaafiapp/medication/admissions/discharge/discharges.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def wantToDeleteDischarge(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,DischargesModel,"Delete this item",
    'allifmaalshaafiapp/medication/admissions/discharge/delete_discharge_confirm.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def deleteDischarge(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='DischargesModel',
    pk=pk,success_redirect_url_name='discharges',app_namespace='allifmaalshaafiapp',)

####################### referals ##################
@allif_base_view_wrapper
def referrals(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Referrals"
    formats=CommonDocsFormatModel.all_objects.all()
    
    allifqueryset =allif_filtered_and_sorted_queryset(request,ReferralsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaalshaafiapp/medication/referrals/referrals.html',context)

@allif_base_view_wrapper
def addReferral(request,pk,*allifargs,**allifkwargs):
    allifquery=get_object_or_404(CommonTransactionsModel, id=pk) 
   
    allifquery_id=allifquery.id
    def transaction_item_pre_save(obj, request, allif_data):
        obj.medical_file=allifquery
    my_extra_context={"allifquery":allifquery,}
    return allif_common_form_submission_and_save(request,form_class=AddReferralForm,
    title_text="New Referral",
        success_redirect_url_name='addReferral',
        template_path='allifmaalshaafiapp/medication/referrals/add_referral.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=allifquery_id,
        extra_context=my_extra_context,app_namespace='allifmaalshaafiapp',)
 
@allif_base_view_wrapper
def EditReferral(request, pk, *allifargs, **allifkwargs):
    return allif_common_form_edit_and_save(request,pk,AddReferralForm,"Edit Referral",
    'EditReferral','allifmaalshaafiapp/medication/referrals/add_referral.html',
    redirect_with_pk=True,redirect_pk_value=pk,app_namespace='allifmaalshaafiapp',)

@allif_base_view_wrapper
def referralDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=ReferralsModel,pk=pk,
        template_name='allifmaalshaafiapp/medication/referrals/referral_details.html', # Create this template
        title_map={'default': 'Referral Details'},)

@allif_base_view_wrapper
def referralSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='ReferralsModel',search_fields_key='ReferralsModel',
    template_path='allifmaalshaafiapp/medication/referrals/referrals.html',search_input_name='allifsearchcommonfieldname',)

@allif_base_view_wrapper
def referalAdvancedSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='ReferralsModel',advanced_search_config_key='ReferralsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaalshaafiapp/medication/referrals/referrals.html',template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html')

@allif_base_view_wrapper
def wantToDeleteReferral(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,ReferralsModel,"Delete this item",
    'allifmaalshaafiapp/medication/referrals/delete_referral.html')

@logged_in_user_can_delete
@allif_base_view_wrapper
def deleteReferral(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='ReferralsModel',
    pk=pk,success_redirect_url_name='referrals',app_namespace='allifmaalshaafiapp',)

