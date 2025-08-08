from django.db import models
from allifmaalcommonapp.constants import TRIAGE_DISPOSITION_CHOICES,MENTAL_STATUS_CHOICES, MOBILITY_CHOICES,BED_TYPES,MODE_OF_ARRIVAL_CHOICES,TRIAGE_LEVEL_CHOICES,SPECIMEN_TYPE,PRIORITY_LEVELS, PRESCRIPTION_FORMULATIONS, ADMINISTRATION_ROUTES, DOSAGE_UNITS, OCCUPANCY_STATUSES, APPOINTMENT_STATUSES, ADMISSION_STATUSES, REFERRAL_TYPES, REFERRAL_STATUSES, LAB_TEST_STATUSES, IMAGING_TEST_STATUSES, PATIENT_GENDERS, BLOOD_GROUPS, ENCOUNTER_TYPES, MEDICAL_SERVICE_TYPES

from allifmaalusersapp.models import User
from allifmaalcommonapp.models import CommonBaseModel,CommonTransactionsModel,CommonSpacesModel,CommonSpaceUnitsModel,CommonCategoriesModel, CommonSuppliersModel, CommonEmployeesModel, CommonDivisionsModel,CommonBranchesModel,CommonDepartmentsModel, CommonCustomersModel,CommonStocksModel,CommonCompanyDetailsModel

# Usage: CommonCompanyScopeModel.active_scopes.for_company(company_id)
class TriagesModel(CommonBaseModel):# very important model
    """
    these are used to record patient assessments like triage records, doctor observations...
    """
    staff=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="en_triage",help_text="The main employee attending this encounter.")
    medical_file=models.ForeignKey(CommonTransactionsModel, on_delete=models.CASCADE,blank=True,null=True, related_name="filetranige",help_text="The customer associated with this encounter.")
    
    #description=models.CharField(max_length=255,blank=True,null=True)
    complaints=models.TextField(null=True, blank=True,help_text="Patient's main symptoms or reason for visit.")
    weight=models.DecimalField(max_digits=10,blank=True,null=True,decimal_places=1)
    # Added height for BMI calculation max_digits=5, decimal_places=2, blank=True, null=True,
    height=models.DecimalField(max_digits=10,blank=True,null=True,decimal_places=2,help_text="Patient's height in centimeters.")# normally in cm
    # Blood pressure separated for better data handling
    blood_pressure_systolic=models.IntegerField(blank=True, null=True,help_text="Systolic blood pressure (mmHg).")
    blood_pressure_diastolic=models.IntegerField(blank=True, null=True,help_text="Diastolic blood pressure (mmHg).")
    # temperatures are normally assumed to be in Celsius ... or specify the unit
    temperature=models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True,help_text="Patient's temperature in Celsius.")
    pulse_rate = models.IntegerField(blank=True, null=True,help_text="Patient's pulse rate (beats per minute).")
    respiration_rate = models.IntegerField(blank=True, null=True,help_text="Patient's respiration rate (breaths per minute).")
    oxygen_saturation = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True,help_text="Patient's oxygen saturation (SpO2 %).")

    past_medical_history = models.TextField(blank=True, null=True,help_text="Relevant past medical history provided by the patient.")
    known_chronic_conditions = models.TextField(blank=True, null=True,help_text="Patient's reported chronic conditions at triage.")
    # Consider linking to a structured MedicationHistoryModel instead of free text 'drugs'
    current_medication = models.TextField(blank=True, null=True,help_text="Medications patient is currently taking, reported at triage.")

    treatment_plan=models.TextField(blank=True, null=True,help_text="Treatment plan (medications, tests, referrals, follow-up).")
   
    pain_level = models.IntegerField(blank=True, null=True,choices=[(i, str(i)) for i in range(0, 11)],help_text="Patient's reported pain level (0-10, 0=no pain, 10=worst pain).")
    allergies=models.TextField(blank=True, null=True,help_text="Patient's reported allergies (e.g., medications, food, environmental).")
   
    triage_disposition = models.CharField(max_length=50, blank=True, null=True,choices=TRIAGE_DISPOSITION_CHOICES,
    help_text="Triage decision or immediate disposition of the patient."
    )
# Add a field for free-text comments about the disposition:
    disposition_notes = models.TextField(blank=True, null=True,help_text="Detailed notes on the triage disposition.")
   
    
    triage_level = models.IntegerField(blank=True, null=True,choices=TRIAGE_LEVEL_CHOICES,help_text="Assigned triage urgency level (e.g., ESI level 1-5).")
    
    mode_of_arrival = models.CharField(max_length=50, blank=True, null=True, choices=MODE_OF_ARRIVAL_CHOICES)
    
    mobility_status = models.CharField(max_length=50, blank=True, null=True, choices=MOBILITY_CHOICES)
   
    mental_status = models.CharField(max_length=50, blank=True, null=True, choices=MENTAL_STATUS_CHOICES)

    class Meta:
       
        ordering = ['-temperature'] # Your ordering is also here
    def __str__(self):
        return str(self.medical_file)


class AssessmentsModel(CommonBaseModel):# very important model
    """
    these are used to record patient assessments like triage records, doctor observations...
    """
    staff=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="en_assessment",help_text="The main employee attending this encounter.")
    medical_file=models.ForeignKey(CommonTransactionsModel, on_delete=models.CASCADE,blank=True,null=True, related_name="fileassessemnt",help_text="The customer associated with this encounter.")
    #owner=models.ForeignKey(User, related_name="owned_encounters_triage", on_delete=models.SET_NULL, null=True, blank=True)
    #items=models.ForeignKey(CommonStocksModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="assessment_items",help_text="The main employee attending this encounter.")
    record_date=models.DateField(blank=True,null=True)
    description=models.CharField(max_length=255,blank=True,null=True)
    complaints=models.TextField(null=True, blank=True,help_text="Patient's main symptoms or reason for visit.")
    weight=models.DecimalField(max_digits=10,blank=True,null=True,decimal_places=1,default=0)
    # Added height for BMI calculation max_digits=5, decimal_places=2, blank=True, null=True,
    height=models.DecimalField(max_digits=10,blank=True,null=True,decimal_places=2,help_text="Patient's height in centimeters.")# normally in cm
    # Blood pressure separated for better data handling
    blood_pressure_systolic=models.IntegerField(blank=True, null=True,help_text="Systolic blood pressure (mmHg).")
    blood_pressure_diastolic=models.IntegerField(blank=True, null=True,help_text="Diastolic blood pressure (mmHg).")
    # temperatures are normally assumed to be in Celsius ... or specify the unit
    temperature=models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True,help_text="Patient's temperature in Celsius.")
    pulse_rate = models.IntegerField(blank=True, null=True,help_text="Patient's pulse rate (beats per minute).")
    respiration_rate = models.IntegerField(blank=True, null=True,help_text="Patient's respiration rate (breaths per minute).")
    oxygen_saturation = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True,help_text="Patient's oxygen saturation (SpO2 %).")

    past_medical_history = models.TextField(blank=True, null=True,help_text="Relevant past medical history provided by the patient.")
    known_chronic_conditions= models.TextField(blank=True, null=True,help_text="Patient's reported chronic conditions at triage.")
    # Consider linking to a structured MedicationHistoryModel instead of free text 'drugs'
    current_medication= models.TextField(blank=True, null=True,help_text="Medications patient is currently taking, reported at triage.")

    treatment_plan=models.TextField(blank=True, null=True,help_text="Treatment plan (medications, tests, referrals, follow-up).")
    
    def __str__(self):
        return str(self.medical_file)


class LabTestRequestsModel(CommonBaseModel):
    """
    Represents a request from a healthcare professional for one or more laboratory tests.
    """
  
    
    items=models.ForeignKey(CommonStocksModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="items_lab_test_requests",)
    
    medical_file=models.ForeignKey(CommonTransactionsModel, on_delete=models.CASCADE, related_name="medical_file_lab_test_requests", blank=True, null=True,)
   
    lab_name=models.ForeignKey(CommonSpacesModel, on_delete=models.SET_NULL, related_name="lab_name_lab_test_requests", blank=True, null=True,)
    specimen=models.CharField(max_length=50,choices=SPECIMEN_TYPE,default='Blood',help_text="Current status of the lab order.")

    test_status=models.CharField(max_length=50,choices=LAB_TEST_STATUSES,default='Ordered',help_text="Current status of the lab order.")

    def __str__(self):
        return str(self.medical_file)
    
class LabTestResultsModel(CommonBaseModel):
    """
    Stores the results for a specific test item from a laboratory order.
    """
  
    test_request=models.ForeignKey(LabTestRequestsModel, on_delete=models.CASCADE, related_name="test_lab_test_requests_results", blank=True, null=True,)
   
   
    def __str__(self):
        return str(self.test_request.medical_file)
      
       
class MedicationsModel(CommonBaseModel):# prescriptions...
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

    frequency=models.CharField(max_length=350,blank=True,null=True)
    duration=models.CharField(max_length=350,blank=True,null=True)
    
    
    prescribed_by_doctor=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="issued_prescriptions",help_text="The doctor who issued this prescription.")
    
    issued_by_pharmacist=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="dispensed_prescriptions",help_text="The pharmacist who dispensed the medication (if dispensed).")
   
    def __str__(self):
        return str(self.medication)


class AdmissionsModel(CommonBaseModel):
    """
    defines admisions of patients in the hospital...
    """
   
    admitting_doctor=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="admitted_patients",)
   
    ward=models.ForeignKey(CommonSpacesModel, on_delete=models.CASCADE, related_name="admissions", blank=True, null=True,help_text="The ward to which the patient is admitted.")
    bed=models.ForeignKey(CommonSpaceUnitsModel, on_delete=models.CASCADE, related_name="admissions", blank=True, null=True,help_text="The specific bed allocated to the patient.")
    
    medical_file=models.ForeignKey(CommonTransactionsModel, on_delete=models.SET_NULL, related_name="mdcladmnss", blank=True, null=True,)
   
    def __str__(self):
        return str(self.medical_file)


class MedicalAdministrationsModel(CommonBaseModel):
    prescription=models.ForeignKey(MedicationsModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="administrations",help_text="The prescription being administered (optional)." )
    
    administered_by_nurse=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="administered_medications",help_text="The nurse or staff member who administered the medication.")
    # Specific fields for dosage administered
    dosage_value=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,help_text="The actual dosage administered (e.g., '500').")
    dosage_unit = models.CharField(max_length=10, choices=DOSAGE_UNITS, blank=True, null=True,help_text="The unit of the administered dosage (e.g., 'MG', 'ML').")
    via=models.CharField(max_length=10, choices=ADMINISTRATION_ROUTES, blank=True, null=True,help_text="The route by which the medication was administered.")
  
    administration_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date', auto_now_add
    given_on = models.DateTimeField(blank=True, null=True) # Keep if 'given_on' is the actual time of administration
   
    def __str__(self):
        return str(self.prescription)

class DischargesModel(CommonBaseModel):
    #For inpatients, a summary at discharge.
    admission=models.ForeignKey(AdmissionsModel, related_name="dschrgsummryadmsn", on_delete=models.SET_NULL, null=True, blank=True)
    discharge_summary=models.CharField(null=True, blank=True,max_length=250)
    discharge_diagnosis=models.CharField(null=True, blank=True,max_length=250)
    medications_at_discharge=models.CharField(null=True, blank=True,max_length=250)
    follow_up_plan=models.CharField(null=True, blank=True,max_length=250)
   
    def __str__(self):
        return str(self.admission)


class ReferralsModel(CommonBaseModel):
    
    """
    Records a patient referral to another doctor, department, or external organization.
    """
    
    referring_doctor=models.ForeignKey(CommonEmployeesModel,help_text="The doctor issuing the referral.",related_name="referring_doctor",on_delete=models.SET_NULL,null=True,blank=True)
   
    medical_file=models.ForeignKey(CommonTransactionsModel, on_delete=models.CASCADE, related_name="referrals_medfile", blank=True, null=True,help_text="The encounter this referral belongs to.")
    
    referral_type=models.CharField(max_length=10, choices=REFERRAL_TYPES, default='INT',help_text="Type of referral (Internal or External).",blank=True,null=True)
    referred_to_doctor=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="received_referrals",help_text="The doctor to whom the patient is referred (if internal).")
    
    # If external, you might link to CommonSuppliersModel or create a specific ExternalHealthcareProviderModel
    referred_to_external_organization = models.ForeignKey(CommonSuppliersModel, on_delete=models.SET_NULL, blank=True, null=True,help_text="Name of the external organization/clinic referred to (if external referral).")
   
    def __str__(self):
        return str(self.medical_file)