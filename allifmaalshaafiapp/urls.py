from django.urls import path
from . import views
app_name='allifmaalshaafiapp'
urlpatterns = [
    
path('Healthcare/Home/<str:allifusr>/<str:allifslug>/', views.shaafiHome, name="shaafiHome"),
path('Healthcare/Dashboard/<str:allifusr>/<str:allifslug>/', views.shaafiDashboard, name="shaafiDashboard"),

################################3 triage data ###########################3
path('Triage/Data/Recorded/Patient/Informations/<str:allifusr>/<str:allifslug>/', views.triageData, name="triageData"),
path('Add/New/Triage/Data/Details/information/Records/<str:pk>/<str:allifusr>/<str:allifslug>/', views.AddTriageData, name="AddTriageData"),
path('Edit/Update/Triage/Data/information/s/detail/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.editTriageData, name="editTriageData"),
path('Search/For/Triage/s/Data/Record/s/info/s/Details/<str:allifusr>/<str:allifslug>/', views.triageDataSearch, name="triageDataSearch"),
path('Triage/s/Details/Information/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.triageDataDetails, name="triageDataDetails"),
path('Do/You/u/Really/Want/to/Delete/This/Triage/s/data/record/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteTriageData, name="wantToDeleteTriageData"),
path('Delete/This/Triage/s/Data/Record/s/info/s/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deleteTriageData, name="deleteTriageData"),
path('Triage/data/info/s/Advance/d/Search/ing/s/<str:allifusr>/<str:allifslug>/', views.triageDataAdvancedSearch, name="triageDataAdvancedSearch"),

###################### doctor assessments ##############3
path('Doctor/Assessment/s/Observation/s/<str:allifusr>/<str:allifslug>/', views.doctorAssessments, name="doctorAssessments"),
path('Add/New/Doctor/Assessment/s/Observations/Records/<str:pk>/<str:allifusr>/<str:allifslug>/', views.addDoctorAssessment, name="addDoctorAssessment"),
path('Edit/Update/Doctor/assessment/s/observations/s/detail/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.editDoctorAssessment, name="editDoctorAssessment"),
path('Search/For/Doctor/Assessment/s/observation/s/Data/Record/s/info/s/Details/<str:allifusr>/<str:allifslug>/', views.doctorAssessmentSearch, name="doctorAssessmentSearch"),

path('Do/You/u/Really/Want/to/Delete/This/Doctor/assessment/s/observation/s/data/record/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteDoctorAssessment, name="wantToDeleteDoctorAssessment"),
path('Delete/This/Doctor/assessment/s/observations/s/Data/Record/s/info/s/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deleteDoctorAssessment, name="deleteDoctorAssessment"),
path('Doctor/assessment/observations/s/data/info/s/Advance/d/Search/ing/s/<str:allifusr>/<str:allifslug>/', views.doctorAssessmentAdvancedSearch, name="doctorAssessmentAdvancedSearch"),

################# prescriptions #####################
path('Prescriptions/<str:allifusr>/<str:allifslug>/', views.prescriptions, name="prescriptions"),
path('Add/New/Prescriptions/<str:pk>/<str:allifusr>/<str:allifslug>/', views.AddPrescription, name="AddPrescription"),
path('Edit/Update/Prescription/s/details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.EditPrescription, name="EditPrescription"),
path('Search/For/Prescriptions/Details/<str:allifusr>/<str:allifslug>/', views.prescriptionSearch, name="prescriptionSearch"),
path('Prescription/s/Details/Information/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.prescriptionDetails, name="prescriptionDetails"),
path('Do/You/u/Really/Want/to/Delete/This/Prescription/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeletePrescription, name="wantToDeletePrescription"),
path('Delete/This/Prescription/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deletePrescription, name="deletePrescription"),

path('Prescription/s/Advance/d/Search/s/<str:allifusr>/<str:allifslug>/', views.prescriptionAdvancedSearch, name="prescriptionAdvancedSearch"),

######################3 treatments and medical adminstrations ##########3
path('medical/adminstrations/treatments/s/of/clients/s/<str:allifusr>/<str:allifslug>/', views.treatments, name="treatments"),
path('Add/New/Treatment/s/medication/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.addTreatment, name="addTreatment"),
path('Edit/Update/treatment/medication/s/details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.EditTreatment, name="EditTreatment"),
path('Search/For/treatment/medication/s/Details/<str:allifusr>/<str:allifslug>/', views.treatmentSearch, name="treatmentSearch"),
path('treatment/medication/s/Details/Information/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.treatmentDetails, name="treatmentDetails"),
path('Do/You/u/Really/Want/to/Delete/This/treatment/s/medication/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteTreatment, name="wantToDeleteTreatment"),
path('Delete/This/Treatments/now/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deleteTreatment, name="deleteTreatment"),

path('advanced/treatment/s/search/e/s/<str:allifusr>/<str:allifslug>/', views.treatmentAdvancedSearch, name="treatmentAdvancedSearch"),


#####################3 admissions ##############
path('Admission/patient/s/<str:allifusr>/<str:allifslug>/', views.admissions, name="admissions"),
path('Add/New/admission/s/medication/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.addAdmission, name="addAdmission"),
path('Edit/Update/admission/s/medication/s/details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.EditAdmission, name="EditAdmission"),
path('Search/For/admission/medication/s/Details/<str:allifusr>/<str:allifslug>/', views.admissionSearch, name="admissionSearch"),
path('admission/s/medication/s/Details/Information/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.admissionDetails, name="admissionDetails"),
path('Do/You/u/Really/Want/to/Delete/This/admission/s/s/medication/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteAdmission, name="wantToDeleteAdmission"),
path('Delete/This/admission/s/now/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deleteAdmission, name="deleteAdmission"),
path('Admission/s/Advanced/Search/es/<str:allifusr>/<str:allifslug>/', views.addmissionAdvancedSearch, name="addmissionAdvancedSearch"),


################## discharges ##########################
path('Discharge/s/s/s/of/patients/clients/s/<str:allifusr>/<str:allifslug>/', views.discharges, name="discharges"),
path('Add/New/Discharge/s/s/hospitalization/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.addDischarge, name="addDischarge"),
path('Edit/Update/discharge/medication/hospitalization/s/details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.EditDischarge, name="EditDischarge"),
path('Search/For/discharge/s/medication/s/Details/<str:allifusr>/<str:allifslug>/', views.dischargeSearch, name="dischargeSearch"),
path('discharge/s/hospitalization/s/Details/Information/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.dischargeDetails, name="dischargeDetails"),
path('Do/You/u/Really/Want/to/Delete/The/selected/discharge/s/hospitalization/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteDischarge, name="wantToDeleteDischarge"),
path('Delete/This/Discharge/s/now/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deleteDischarge, name="deleteDischarge"),
path('advanced/discharge/s/searches/<str:allifusr>/<str:allifslug>/', views.dischargeAdvancedSearch, name="dischargeAdvancedSearch"),


#####################3 referals ##############
path('Referals/s/of/clients/s/<str:allifusr>/<str:allifslug>/', views.referrals, name="referrals"),
path('Add/New/referral/s/medication/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.addReferral, name="addReferral"),
path('Edit/Update/referral/s/medication/s/details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.EditReferral, name="EditReferral"),
path('Search/For/referral/s/medication/s/Details/<str:allifusr>/<str:allifslug>/', views.referralSearch, name="referralSearch"),
path('Referral/s/medication/s/Details/Information/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.referralDetails, name="referralDetails"),
path('Do/You/u/Really/Want/to/Delete/This/Referral/s/now/s/medication/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteReferral, name="wantToDeleteReferral"),
path('Delete/This/Referral/s/now/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deleteReferral, name="deleteReferral"),
path('Referal/s/advanced/search/s/<str:allifusr>/<str:allifslug>/', views.referalAdvancedSearch, name="referalAdvancedSearch"),

]  