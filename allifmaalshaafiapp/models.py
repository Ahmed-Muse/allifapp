from django.db import models
from allifmaalcommonapp.constants import BED_TYPES, PRESCRIPTION_FORMULATIONS, ADMINISTRATION_ROUTES, DOSAGE_UNITS, OCCUPANCY_STATUSES, APPOINTMENT_STATUSES, ADMISSION_STATUSES, REFERRAL_TYPES, REFERRAL_STATUSES, LAB_TEST_STATUSES, IMAGING_TEST_STATUSES, PATIENT_GENDERS, BLOOD_GROUPS, ENCOUNTER_TYPES, MEDICAL_SERVICE_TYPES

from allifmaalusersapp.models import User
from allifmaalcommonapp.models import CommonTransactionEventsModel,CommonCategoriesModel, CommonSuppliersModel, CommonEmployeesModel, CommonDivisionsModel,CommonBranchesModel,CommonDepartmentsModel, CommonCustomersModel,CommonStocksModel,CommonCompanyDetailsModel

class PrescriptionsModel(models.Model):
    """
    Represents a medication prescription issued by a doctor for a patient.
    """
    patient=models.ForeignKey(CommonCustomersModel, max_length=200,on_delete=models.CASCADE,related_name="prescriptionscustm",blank=True,null=True)
    medication=models.ForeignKey(CommonStocksModel, help_text="The drug/item prescribed (from common inventory).",max_length=250,on_delete=models.CASCADE,related_name="prescriptions",blank=True,null=True)
    dosage_form=models.CharField(choices=PRESCRIPTION_FORMULATIONS, help_text="Formulation of the drug (e.g., Tablet, Syrup, Injection).", default='Please select', max_length=200,blank=True,null=True)
    
    # Keep as CharField if it includes value + unit (e.g., "500mg")
    dosage=models.CharField(choices=DOSAGE_UNITS,blank=True,null=True,max_length=250, help_text="Dosage amount and unit (e.g., '500mg', '10ml').")
    route_of_administration=models.CharField(choices=ADMINISTRATION_ROUTES,blank=True,null=True,max_length=250,default='ORAL', help_text="How the medication should be administered (e.g., Oral, IV, IM).")
    quantity=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=1,default=0)
    is_issued=models.BooleanField(max_length=50,default=False,help_text="True if the prescription has been dispensed by the pharmacy.")

    owner=models.ForeignKey(User, related_name="ownrprescrptns",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpprescrptns",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsprescrptns",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchprescrptn",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptprescrptns",on_delete=models.SET_NULL,null=True,blank=True)
    frequency=models.CharField(max_length=350,blank=True,null=True)
    duration=models.CharField(max_length=350,blank=True,null=True)
    
    medical_file=models.ForeignKey(CommonTransactionEventsModel, on_delete=models.CASCADE, related_name="prescriptions", blank=True, null=True,help_text="The encounter this prescription belongs to.")
    prescribed_by_doctor=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="issued_prescriptions",help_text="The doctor who issued this prescription.")
    
    # Added: How often the medication should be taken
    frequency=models.CharField(max_length=100, blank=True, null=True,help_text="How often the medication should be taken (e.g., 'Once daily', 'Twice a day').")
     # For how long the medication should be taken
    duration=models.CharField(max_length=100, blank=True, null=True,help_text="Duration of the treatment (e.g., '7 days', 'Until finished').")
    instructions=models.TextField(blank=True, null=True,help_text="Patient-specific instructions for medication use.")
   
    issued_by_pharmacist=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="dispensed_prescriptions",help_text="The pharmacist who dispensed the medication (if dispensed).")
    issued_date_time=models.DateTimeField(blank=True, null=True,help_text="Date and time when the prescription was dispensed.")

    prescription_date_time=models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date' to specific, auto_now_add
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return str(self.drug)

class WardsModel(models.Model):
    ward_name=models.TextField(max_length=250,blank=True,null=True,default='Ward')
    date=models.DateField(blank=True,null=True,auto_now_add=True)
    owner=models.ForeignKey(User, related_name="ownrwards",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpwardsrelatnme",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvswards",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchwards",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptwards",on_delete=models.SET_NULL,null=True,blank=True)
   
    ward_type=models.CharField(max_length=50, blank=True, null=True,choices=[('GEN', 'General'), ('ICU', 'Intensive Care Unit'), ('MAT', 'Maternity'),('PED', 'Pediatrics'), ('SURG', 'Surgical')],help_text="Category of the ward (e.g., ICU, Maternity).")
    capacity=models.IntegerField(blank=True, null=True, default=0,help_text="Maximum number of beds this ward can accommodate.")
    
    # give more details on this word if necessary
    description=models.TextField(blank=True, null=True)

    nurse_in_charge=models.ForeignKey(CommonEmployeesModel,related_name="nurseinchrgwards",on_delete=models.SET_NULL,null=True,blank=True,help_text="The nurse designated as in-charge of this ward.")
    doctor_in_charge = models.ForeignKey(CommonEmployeesModel,related_name="docinchrgewards",on_delete=models.SET_NULL,null=True,blank=True,help_text="The doctor designated as in-charge of this ward.")

    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.ward_name)

class BedsModel(models.Model):
    owner=models.ForeignKey(User, related_name="ownrbds",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpbds",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsbds",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchbds",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptbds",on_delete=models.SET_NULL,null=True,blank=True)
    
    features=models.TextField(max_length=250,blank=True,null=True,default='Ward')
    bed_number=models.CharField(max_length=50, blank=True, null=True,default=1,help_text="Unique identifier for the bed (e.g., 'Room 101-A', 'Bed 5').")
    ward=models.ForeignKey(WardsModel, on_delete=models.CASCADE, related_name="bedsword", blank=True, null=True, help_text="The ward to which this bed belongs.")
    room_number=models.CharField( max_length=50, blank=True, null=True,help_text="Room number within the ward, if applicable.")
    
    bed_type=models.CharField(max_length=10, choices=BED_TYPES, default='STD', blank=True, null=True,help_text="Type of bed (e.g., Standard, Private, ICU).")
    daily_charges=models.DecimalField(max_digits=30, decimal_places=2, default=0, blank=True, null=True,help_text="Daily charge for occupying this bed.")
    current_occupancy_status=models.CharField(choices=OCCUPANCY_STATUSES, default='VACANT', blank=True, null=True, max_length=50,help_text="Current occupancy status of the bed.")
    features=models.TextField(blank=True, null=True,help_text="Special features or amenities of the bed/room.")

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return str(self.bed)

class AppointmentsModel(models.Model):
    patient=models.ForeignKey(CommonCustomersModel,max_length=200,on_delete=models.CASCADE,related_name="custappnt",db_index=True,blank=True,null=True)
    owner=models.ForeignKey(User, related_name="ownrappointment",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpappointment",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsappointment",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchappointment",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptappointment",on_delete=models.SET_NULL,null=True,blank=True)
    
    doctor=models.ForeignKey(CommonEmployeesModel,related_name="ownrappointment",on_delete=models.SET_NULL,null=True,blank=True)

    #linking to MedicalServicesModel if appointment is for a specific service (e.g., X-ray)
    scheduled_service=models.ForeignKey(CommonCategoriesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="service_appointments",help_text="The medical service for which this appointment is scheduled (optional).")

    appointment_date_time=models.DateTimeField(blank=True, null=True,help_text="Scheduled date and time of the appointment.")
    duration_minutes = models.IntegerField(blank=True, null=True, default=30,help_text="Expected duration of the appointment in minutes.")
    reason_for_visit=models.TextField(blank=True, null=True,help_text="Reason for the patient's visit.")
    status=models.CharField(max_length=10, choices=APPOINTMENT_STATUSES, default='SCH',help_text="Current status of the appointment.")
    is_checked_in = models.BooleanField(default=False) # Added: To track patient arrival
    check_in_time = models.DateTimeField(blank=True, null=True) # Added: Time of check-in

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date'
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.description)

class AdmissionsModel(models.Model):
    owner=models.ForeignKey(User, related_name="ownradmissns",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpadmissns",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsadmissns",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchaadmissns",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptadmissns",on_delete=models.SET_NULL,null=True,blank=True)
    patient=models.ForeignKey(CommonCustomersModel, on_delete=models.CASCADE, related_name="admissions", db_index=True, blank=True, null=True,help_text="The patient being admitted.")
    admitting_doctor=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="admitted_patients",)
    admission_date_time=models.DateTimeField(blank=True, null=True, auto_now_add=True,help_text="Date and time of patient admission.")
    reason_for_admission=models.TextField(max_length=250,blank=True, null=True,help_text="The primary reason for patient admission.")
    ward=models.ForeignKey(WardsModel, on_delete=models.CASCADE, related_name="admissions", blank=True, null=True,help_text="The ward to which the patient is admitted.")
    bed=models.ForeignKey(BedsModel, on_delete=models.CASCADE, related_name="admissions", blank=True, null=True,help_text="The specific bed allocated to the patient.")
    status=models.CharField(max_length=100, choices=ADMISSION_STATUSES, default='ADM',help_text="Current status of the admission (e.g., Admitted, Discharged).")
    discharge_date_time=models.DateTimeField(blank=True, null=True,help_text="Date and time of patient discharge (if applicable).")
    discharge_reason=models.TextField(blank=True, null=True,help_text="Reason for patient discharge (e.g., 'Recovered', 'Transferred').")
    medical_file=models.ForeignKey(CommonTransactionEventsModel, on_delete=models.SET_NULL, related_name="mdcladmnss", blank=True, null=True,)
    date_created=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return str(self.patient)

class VitalSignsModel(models.Model):
    """
    Records continuous or periodic vital signs for a patient during an visit or admision.
    """
    patient=models.ForeignKey(CommonCustomersModel,max_length=200,on_delete=models.CASCADE,related_name="cstvtlsgns",db_index=True,blank=True,null=True)
    
    owner=models.ForeignKey(User, related_name="ownvtlsgns",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpvtlsgns",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsvtlsgns",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchvtlsgns",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptvtlsgns",on_delete=models.SET_NULL,null=True,blank=True)
    
    recorded_by_nurse=models.ForeignKey(CommonEmployeesModel, help_text="The nurse or staff member who recorded the vital signs.",related_name="refering_nurse",on_delete=models.SET_NULL,null=True,blank=True)
   
    medical_file=models.ForeignKey(CommonTransactionEventsModel, on_delete=models.CASCADE, related_name="vital_signs", blank=True, null=True,help_text="The encounter this vital signs record belongs to.")
    
    temperature=models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True,help_text="Temperature in Celsius.")
    blood_pressure_systolic=models.IntegerField(blank=True, null=True,help_text="Systolic blood pressure (mmHg).")
    blood_pressure_diastolic=models.IntegerField(blank=True, null=True,help_text="Diastolic blood pressure (mmHg).")
    pulse_rate=models.IntegerField(blank=True, null=True,help_text="Pulse rate (beats per minute).")
    respiration_rate=models.IntegerField(blank=True, null=True,help_text="Respiration rate (breaths per minute).")
    oxygen_saturation=models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True,help_text="Oxygen saturation (SpO2 %).")
    pain_level=models.IntegerField(blank=True, null=True, choices=[(i, str(i)) for i in range(11)],help_text="Patient's pain level on a scale of 0-10 (optional).")
    additional_observations=models.TextField(blank=True, null=True,help_text="Any additional qualitative observations.")

    recording_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date', auto_now_add
    recorded_on = models.DateTimeField(blank=True, null=True) # Keep if 'recorded_on' is the actual time of measurement
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
   
    def __str__(self):
        return str(self.patient)
    
class ReferralsModel(models.Model):
    
    """
    Records a patient referral to another doctor, department, or external organization.
    """
    patient=models.ForeignKey(CommonCustomersModel,max_length=200,on_delete=models.CASCADE,related_name="custrefrals",db_index=True,blank=True,null=True)
    reason_for_referral=models.CharField(null=True, blank=True,max_length=250, help_text="The reason for the referral.")
    owner=models.ForeignKey(User, related_name="ownrrefrals",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmprefrals",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsrefrals",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brncharefrals",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptrefrals",on_delete=models.SET_NULL,null=True,blank=True)
    
    referring_doctor=models.ForeignKey(CommonEmployeesModel,help_text="The doctor issuing the referral.",related_name="referring_doctor",on_delete=models.SET_NULL,null=True,blank=True)
    referred_on=models.DateField(blank=True, null=True)
    
    medical_file=models.ForeignKey(CommonTransactionEventsModel, on_delete=models.CASCADE, related_name="referrals_medfile", blank=True, null=True,help_text="The encounter this referral belongs to.")
    
    referral_type=models.CharField(max_length=10, choices=REFERRAL_TYPES, default='INT',help_text="Type of referral (Internal or External).")
    referred_to_doctor=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="received_referrals",help_text="The doctor to whom the patient is referred (if internal).")
    referred_to_department=models.ForeignKey(CommonDepartmentsModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="department_referrals",help_text="The department to which the patient is referred (if internal).")
    # If external, you might link to CommonSuppliersModel or create a specific ExternalHealthcareProviderModel
    referred_to_external_organization = models.ForeignKey(CommonSuppliersModel, on_delete=models.SET_NULL, blank=True, null=True,help_text="Name of the external organization/clinic referred to (if external referral).")
    status=models.CharField( max_length=10, choices=REFERRAL_STATUSES, default='PEND',help_text="Current status of the referral.")

    referral_date_time=models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date', auto_now_add
    referred_on=models.DateTimeField(blank=True, null=True) # Keep 'referred_on' if it's the actual date of referral action, separate from record creation
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.patient)

class MedicalAdministrationsModel(models.Model):
    #Records the actual administration of medication to a patient.
    patient=models.ForeignKey(CommonCustomersModel,max_length=200,on_delete=models.CASCADE,related_name="custmedcladmins",db_index=True,blank=True,null=True)
   
    owner=models.ForeignKey(User, related_name="ownmedcladmins",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpmedcladmins",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsmedcladmins",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchamedcladmins",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptmedcladmins",on_delete=models.SET_NULL,null=True,blank=True)
   
    medical_file=models.ForeignKey(CommonTransactionEventsModel, on_delete=models.CASCADE, related_name="medication_administrations", blank=True, null=True,help_text="The encounter this medication administration belongs to.")
    # Link to the prescription this administration fulfills (optional, but good for tracking)
    prescription=models.ForeignKey(PrescriptionsModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="administrations",help_text="The prescription being administered (optional)." )
    drug_name=models.ForeignKey(CommonStocksModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="administered_medications",help_text="The actual drug administered (from inventory).")
    administered_by_nurse=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="administered_medications",help_text="The nurse or staff member who administered the medication.")
    # Specific fields for dosage administered
    dosage_value=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,help_text="The actual dosage administered (e.g., '500').")
    dosage_unit = models.CharField(max_length=10, choices=DOSAGE_UNITS, blank=True, null=True,help_text="The unit of the administered dosage (e.g., 'MG', 'ML').")
    route_of_administration=models.CharField(max_length=10, choices=ADMINISTRATION_ROUTES, blank=True, null=True,help_text="The route by which the medication was administered.")
    comments=models.TextField(blank=True, null=True,help_text="Any additional comments about the administration.")
    
    administration_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date', auto_now_add
    given_on = models.DateTimeField(blank=True, null=True) # Keep if 'given_on' is the actual time of administration
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
   
    def __str__(self):
        return str(self.patient)

class NursingNotesModel(models.Model):
    #Records general nursing observations and progress notes.
   
    patient=models.ForeignKey(CommonCustomersModel,max_length=200,on_delete=models.CASCADE,related_name="custnrsingntes",db_index=True,blank=True,null=True)
    
    owner=models.ForeignKey(User, related_name="ownrnrsingnte",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmpnrsingntes",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsnrsingntes",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchnrsingntes",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptnrsingntes",on_delete=models.SET_NULL,null=True,blank=True)
   
    medical_file=models.ForeignKey(CommonTransactionEventsModel, on_delete=models.CASCADE, related_name="nursing_notes", blank=True, null=True,help_text="The encounter this nursing note belongs to.")
    recorded_by_nurse=models.ForeignKey(CommonEmployeesModel, on_delete=models.SET_NULL, null=True, blank=True,related_name="authored_nursing_notes",help_text="The nurse who recorded these notes.")
    notes=models.TextField(blank=True, null=True,help_text="Detailed nursing observations and progress notes.")

    note_date_time=models.DateTimeField(auto_now_add=True, blank=True, null=True) # Renamed 'date', auto_now_add
    recorded_on=models.DateTimeField(blank=True, null=True) # Keep if 'recorded_on' is the actual time of note-taking
    last_updated=models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Nursing Note"
        verbose_name_plural = "Nursing Notes"
        ordering = ['-note_date_time']
   
    def __str__(self):
        return str(self.patient)

class DischargeSummaryModel(models.Model):
    #For inpatients, a summary at discharge.
    admission=models.ForeignKey(AdmissionsModel, related_name="dschrgsummryadmsn", on_delete=models.SET_NULL, null=True, blank=True)
    patient=models.ForeignKey(CommonCustomersModel, related_name="patinetdischrsummrs", on_delete=models.SET_NULL, null=True, blank=True)
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