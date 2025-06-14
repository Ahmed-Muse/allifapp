from django.db import models
from allifmaalcommonapp.constants import BED_TYPES, PRESCRIPTION_FORMULATIONS, ADMINISTRATION_ROUTES, DOSAGE_UNITS, OCCUPANCY_STATUSES, APPOINTMENT_STATUSES, ADMISSION_STATUSES, REFERRAL_TYPES, REFERRAL_STATUSES, LAB_TEST_STATUSES, IMAGING_TEST_STATUSES, PATIENT_GENDERS, BLOOD_GROUPS, ENCOUNTER_TYPES, MEDICAL_SERVICE_TYPES

from allifmaalusersapp.models import User
from allifmaalcommonapp.models import CommonTransactionsModel,CommonSpacesModel,CommonSpaceUnitsModel,CommonCategoriesModel, CommonSuppliersModel, CommonEmployeesModel, CommonDivisionsModel,CommonBranchesModel,CommonDepartmentsModel, CommonCustomersModel,CommonStocksModel,CommonCompanyDetailsModel

class MedicationsModel(models.Model):# prescriptions...
    """
    Represents an actual prescription of medication  and otherprescriptions issued by a doctor for a patient.
    """
    medical_file=models.ForeignKey(CommonTransactionsModel, on_delete=models.CASCADE, related_name="prescriptions", blank=True, null=True,help_text="The encounter this prescription belongs to.")
    medication=models.ForeignKey(CommonStocksModel, help_text="The drug/item prescribed (from common inventory).",max_length=250,on_delete=models.CASCADE,related_name="prescriptions",blank=True,null=True)
    dosage_form=models.CharField(choices=PRESCRIPTION_FORMULATIONS, help_text="Formulation of the drug (e.g., Tablet, Syrup, Injection).", default='Please select', max_length=200,blank=True,null=True)
    
    # Keep as CharField if it includes value + unit (e.g., "500mg")
    dosage=models.CharField(choices=DOSAGE_UNITS,blank=True,null=True,max_length=250, help_text="Dosage amount and unit (e.g., '500mg', '10ml').")
    via=models.CharField(choices=ADMINISTRATION_ROUTES,blank=True,null=True,max_length=250,default='ORAL', help_text="How the medication should be administered (e.g., Oral, IV, IM).")
    quantity=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    is_issued=models.BooleanField(max_length=50,default=False,help_text="True if the prescription has been dispensed by the pharmacy.")

    owner=models.ForeignKey(User, related_name="ownrprescrptns",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpprescrptns",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsprescrptns",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchprescrptn",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptprescrptns",on_delete=models.SET_NULL,null=True,blank=True)
    frequency=models.CharField(max_length=350,blank=True,null=True)
    duration=models.CharField(max_length=350,blank=True,null=True)
    
    
    prescribed_by_doctor=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="issued_prescriptions",help_text="The doctor who issued this prescription.")
    
  
    instructions=models.TextField(blank=True, null=True,help_text="Patient-specific instructions for medication use.")
   
    issued_by_pharmacist=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="dispensed_prescriptions",help_text="The pharmacist who dispensed the medication (if dispensed).")
    issued_date_time=models.DateTimeField(blank=True, null=True,help_text="Date and time when the prescription was dispensed.")

    prescription_date_time=models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date' to specific, auto_now_add
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return str(self.medication)


class AdmissionsModel(models.Model):
    """
    defines admisions of patients in the hospital...
    """
    owner=models.ForeignKey(User, related_name="ownradmissns",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpadmissns",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsadmissns",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchaadmissns",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptadmissns",on_delete=models.SET_NULL,null=True,blank=True)
    description=models.CharField(max_length=50, help_text="Type of referral (Internal or External).",blank=True,null=True)
    admitting_doctor=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="admitted_patients",)
    date_time=models.DateTimeField(blank=True, null=True, auto_now_add=True,help_text="Date and time of patient admission.")
    reason_for_admission=models.TextField(max_length=250,blank=True, null=True,help_text="The primary reason for patient admission.")
    ward=models.ForeignKey(CommonSpacesModel, on_delete=models.CASCADE, related_name="admissions", blank=True, null=True,help_text="The ward to which the patient is admitted.")
    bed=models.ForeignKey(CommonSpaceUnitsModel, on_delete=models.CASCADE, related_name="admissions", blank=True, null=True,help_text="The specific bed allocated to the patient.")
    status=models.CharField(max_length=100, choices=ADMISSION_STATUSES, default='ADM',help_text="Current status of the admission (e.g., Admitted, Discharged).")
    admission_date_time=models.DateTimeField(blank=True, null=True,help_text="Date and time of patient discharge (if applicable).")
    
    medical_file=models.ForeignKey(CommonTransactionsModel, on_delete=models.SET_NULL, related_name="mdcladmnss", blank=True, null=True,)
    date_created=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return str(self.medical_file)


class MedicalAdministrationsModel(models.Model):
   
    owner=models.ForeignKey(User, related_name="ownmedcladmins",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpmedcladmins",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsmedcladmins",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchamedcladmins",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptmedcladmins",on_delete=models.SET_NULL,null=True,blank=True)
   
    medical_file=models.ForeignKey(CommonTransactionsModel, on_delete=models.CASCADE, related_name="medication_administrations", blank=True, null=True,help_text="The encounter this medication administration belongs to.")
    # Link to the prescription this administration fulfills (optional, but good for tracking)
    prescription=models.ForeignKey(MedicationsModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="administrations",help_text="The prescription being administered (optional)." )
    
    administered_by_nurse=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="administered_medications",help_text="The nurse or staff member who administered the medication.")
    # Specific fields for dosage administered
    dosage_value=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,help_text="The actual dosage administered (e.g., '500').")
    dosage_unit = models.CharField(max_length=10, choices=DOSAGE_UNITS, blank=True, null=True,help_text="The unit of the administered dosage (e.g., 'MG', 'ML').")
    via=models.CharField(max_length=10, choices=ADMINISTRATION_ROUTES, blank=True, null=True,help_text="The route by which the medication was administered.")
    comments=models.TextField(blank=True, null=True,help_text="Any additional comments about the administration.")
    
    administration_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date', auto_now_add
    given_on = models.DateTimeField(blank=True, null=True) # Keep if 'given_on' is the actual time of administration
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
   
    def __str__(self):
        return str(self.medical_file)

class DischargesModel(models.Model):
    #For inpatients, a summary at discharge.
    admission=models.ForeignKey(AdmissionsModel, related_name="dschrgsummryadmsn", on_delete=models.SET_NULL, null=True, blank=True)
    discharge_summary=models.CharField(null=True, blank=True,max_length=250)
    discharge_diagnosis=models.CharField(null=True, blank=True,max_length=250)
    medications_at_discharge=models.CharField(null=True, blank=True,max_length=250)
    follow_up_plan=models.CharField(null=True, blank=True,max_length=250)
    recorded_on = models.DateTimeField(blank=True, null=True) # Keep if 'recorded_on' is the actual time of note-taking
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    owner=models.ForeignKey(User, related_name="owned_nursing_notes", on_delete=models.SET_NULL, null=True, blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel, related_name="company_nursing_notes", on_delete=models.CASCADE, null=True, blank=True)
    division=models.ForeignKey(CommonDivisionsModel, related_name="division_nursing_notes", on_delete=models.SET_NULL, null=True, blank=True)
    branch=models.ForeignKey(CommonBranchesModel, related_name="branch_nursing_notes", on_delete=models.SET_NULL, null=True, blank=True)
    department=models.ForeignKey(CommonDepartmentsModel, related_name="department_nursing_notes", on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return str(self.patient)


class ReferralsModel(models.Model):
    
    """
    Records a patient referral to another doctor, department, or external organization.
    """
    
    reason_for_referral=models.CharField(null=True, blank=True,max_length=250, help_text="The reason for the referral.")
    owner=models.ForeignKey(User, related_name="ownrrefrals",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmprefrals",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsrefrals",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brncharefrals",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptrefrals",on_delete=models.SET_NULL,null=True,blank=True)
    
    referring_doctor=models.ForeignKey(CommonEmployeesModel,help_text="The doctor issuing the referral.",related_name="referring_doctor",on_delete=models.SET_NULL,null=True,blank=True)
    referred_on=models.DateField(blank=True, null=True)
    
    medical_file=models.ForeignKey(CommonTransactionsModel, on_delete=models.CASCADE, related_name="referrals_medfile", blank=True, null=True,help_text="The encounter this referral belongs to.")
    
    referral_type=models.CharField(max_length=10, choices=REFERRAL_TYPES, default='INT',help_text="Type of referral (Internal or External).")
    referred_to_doctor=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="received_referrals",help_text="The doctor to whom the patient is referred (if internal).")
    
    # If external, you might link to CommonSuppliersModel or create a specific ExternalHealthcareProviderModel
    referred_to_external_organization = models.ForeignKey(CommonSuppliersModel, on_delete=models.SET_NULL, blank=True, null=True,help_text="Name of the external organization/clinic referred to (if external referral).")
    status=models.CharField( max_length=10, choices=REFERRAL_STATUSES, default='PEND',help_text="Current status of the referral.")

    referral_date_time=models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date', auto_now_add
    
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.medical_file)