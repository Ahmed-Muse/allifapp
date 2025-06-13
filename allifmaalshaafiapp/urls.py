from django.urls import path
from . import views
app_name='allifmaalshaafiapp'
urlpatterns = [
    
path('Healthcare/Home/<str:allifusr>/<str:allifslug>/', views.shaafiHome, name="shaafiHome"),
path('Healthcare/Dashboard/<str:allifusr>/<str:allifslug>/', views.shaafiDashboard, name="shaafiDashboard"),

################# prescriptions #####################
path('Prescriptions/<str:allifusr>/<str:allifslug>/', views.prescriptions, name="prescriptions"),
path('Add/New/Prescriptions/<str:allifusr>/<str:allifslug>/', views.AddPrescription, name="AddPrescription"),
path('Edit/Update/Prescription/s/details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.EditPrescription, name="EditPrescription"),
path('Search/For/Prescriptions/Details/<str:allifusr>/<str:allifslug>/', views.prescriptionSearch, name="prescriptionSearch"),
path('Prescription/s/Details/Information/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.prescriptionDetails, name="prescriptionDetails"),
path('Do/You/u/Really/Want/to/Delete/This/Prescription/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeletePrescription, name="wantToDeletePrescription"),
path('Delete/This/Prescription/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deletePrescription, name="deletePrescription"),

path('Prescription/s/Advance/d/Search/s/<str:allifusr>/<str:allifslug>/', views.prescriptionAdvancedSearch, name="prescriptionAdvancedSearch"),


######################3 treatments and medical adminstrations ##########3
path('medical/adminstrations/treatments/s/of/clients/s/<str:allifusr>/<str:allifslug>/', views.treatments, name="treatments"),

path('Add/New/Treatment/s/medication/s/<str:allifusr>/<str:allifslug>/', views.addTreatment, name="addTreatment"),
path('Edit/Update/treatment/medication/s/details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.EditTreatment, name="EditTreatment"),
path('Search/For/treatment/medication/s/Details/<str:allifusr>/<str:allifslug>/', views.treatmentSearch, name="treatmentSearch"),
path('treatment/medication/s/Details/Information/s/<str:int>/<str:allifusr>/<str:allifslug>/', views.treatmentDetails, name="treatmentDetails"),
path('Do/You/u/Really/Want/to/Delete/This/treatment/s/medication/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteTreatment, name="wantToDeleteTreatment"),
path('Delete/This/Treatments/now/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deleteTreatment, name="deleteTreatment"),


#####################3 admissions ##############
path('Admission/patient/s/<str:allifusr>/<str:allifslug>/', views.admissions, name="admissions"),

path('Add/New/admission/s/medication/s/<str:allifusr>/<str:allifslug>/', views.addAdmission, name="addAdmission"),
path('Edit/Update/admission/s/medication/s/details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.EditAdmission, name="EditAdmission"),
path('Search/For/admission/medication/s/Details/<str:allifusr>/<str:allifslug>/', views.admissionSearch, name="admissionSearch"),
path('admission/s/medication/s/Details/Information/s/<str:int>/<str:allifusr>/<str:allifslug>/', views.admissionDetails, name="admissionDetails"),
path('Do/You/u/Really/Want/to/Delete/This/admission/s/s/medication/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteAdmission, name="wantToDeleteAdmission"),
path('Delete/This/admission/s/now/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deleteAdmission, name="deleteAdmission"),



################## discharges ##########################
path('Discharge/s/s/s/of/patients/clients/s/<str:allifusr>/<str:allifslug>/', views.discharges, name="discharges"),
path('Add/New/Discharge/s/s/hospitalization/s/<str:allifusr>/<str:allifslug>/', views.addDischarge, name="addDischarge"),
path('Edit/Update/discharge/medication/hospitalization/s/details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.EditDischarge, name="EditDischarge"),
path('Search/For/discharge/s/medication/s/Details/<str:allifusr>/<str:allifslug>/', views.dischargeSearch, name="dischargeSearch"),
path('discharge/s/hospitalization/s/Details/Information/s/<str:int>/<str:allifusr>/<str:allifslug>/', views.dischargeDetails, name="dischargeDetails"),
path('Do/You/u/Really/Want/to/Delete/The/selected/discharge/s/hospitalization/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteDischarge, name="wantToDeleteDischarge"),
path('Delete/This/Discharge/s/now/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deleteDischarge, name="deleteDischarge"),




#####################3 referals ##############
path('Referals/s/of/clients/s/<str:allifusr>/<str:allifslug>/', views.referrals, name="referrals"),
path('Add/New/referral/s/medication/s/<str:allifusr>/<str:allifslug>/', views.addReferral, name="addReferral"),
path('Edit/Update/referral/s/medication/s/details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.EditReferral, name="EditReferral"),
path('Search/For/referral/s/medication/s/Details/<str:allifusr>/<str:allifslug>/', views.referralSearch, name="referralSearch"),
path('Referral/s/medication/s/Details/Information/s/<str:int>/<str:allifusr>/<str:allifslug>/', views.referralDetails, name="referralDetails"),
path('Do/You/u/Really/Want/to/Delete/This/Referral/s/now/s/medication/s/<str:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteReferral, name="wantToDeleteReferral"),
path('Delete/This/Referral/s/now/Permanently/<str:pk>/<str:allifusr>/<str:allifslug>/', views.deleteReferral, name="deleteReferral"),




]  