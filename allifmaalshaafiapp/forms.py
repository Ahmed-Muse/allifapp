from django import forms
from .models import *
from allifmaalcommonapp.forms import CommonBaseForm
from allifmaalcommonapp.utils import allif_initialize_form_select_querysets
############################# start of datepicker customization ##############################
class DatePickerInput(forms.DateInput):#use this class whereever you have a date and it will give you the calender
    input_type='date'#
class TimePickerInput(forms.TimeInput):#use this wherever you have time input
    input_type='time'
class DateTimePickerInput(forms.DateTimeInput):#use this wherever you have datetime input
    input_type='datetime'

class AddTriageDetailsForm(CommonBaseForm):
    company_filtered_fields = {
        'staff': CommonEmployeesModel,
       
        }
    class Meta(CommonBaseForm.Meta):
        model=TriagesModel
        fields=CommonBaseForm.Meta.fields + ['staff','description','complaints','weight','height',
                  'blood_pressure_systolic','blood_pressure_diastolic','temperature','pulse_rate',
                  'respiration_rate','oxygen_saturation','past_medical_history','known_chronic_conditions',
                  'current_medication','treatment_plan',
                  'pain_level','allergies','triage_disposition','disposition_notes','triage_level','mode_of_arrival',
                  'mobility_status','mental_status']
        widgets = {
        **CommonBaseForm.Meta.widgets,
       
            'allergies':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'disposition_notes':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'blood_pressure_diastolic':forms.TextInput(attrs={'class':'form-control','placeholder':'in mmHg'}),
            'current_medication':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'oxygen_saturation':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'temperature':forms.TextInput(attrs={'class':'form-control','placeholder':'in Degrees Celcious'}),
            'respiration_rate':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'known_chronic_conditions':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'pulse_rate':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'record_date' : DatePickerInput(attrs={'class':'form-control'}),
            'treatment_plan':forms.Textarea(attrs={'class':'form-control allif-form-control-textarea','placeholder':''}),
            'staff':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

            
            'pain_level':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'triage_disposition':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'triage_level':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'mode_of_arrival':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'mobility_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'mental_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

            'complaints':forms.Textarea(attrs={'class':'form-control allif-form-control-textarea','placeholder':''}),
            'weight':forms.TextInput(attrs={'class':'form-control','placeholder':'in KGs'}),
            'height':forms.TextInput(attrs={'class':'form-control','placeholder':'in cm'}),
            
            'blood_pressure_systolic':forms.TextInput(attrs={'class':'form-control','placeholder':'in mmHg'}),
            'past_medical_history':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        }
        """
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['staff'].queryset=CommonEmployeesModel.objects.filter(company=allifmaalparameter)
      
        else:
            self.fields['staff'].queryset=CommonEmployeesModel.objects.none()
    """
    
      
class AddAssessmentDetailsForm(CommonBaseForm):
    company_filtered_fields = {
        'medical_file': CommonTransactionsModel,
        'staff': CommonEmployeesModel,
       
        }
     
    class Meta(CommonBaseForm.Meta):
        model = AssessmentsModel
        fields = CommonBaseForm.Meta.fields + ['medical_file','record_date','staff','complaints','weight','height',
                  'blood_pressure_systolic','blood_pressure_diastolic','temperature','pulse_rate',
                  'respiration_rate','oxygen_saturation','past_medical_history','known_chronic_conditions',
                  'current_medication',
                  'treatment_plan']
        widgets={
            **CommonBaseForm.Meta.widgets,
            
            'blood_pressure_diastolic':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'current_medication':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'oxygen_saturation':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'temperature':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'respiration_rate':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'known_chronic_conditions':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'pulse_rate':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'record_date' : DatePickerInput(attrs={'class':'form-control'}),
            'treatment_plan':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
            'staff':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          
            'complaints':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
            'weight':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'height':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'medical_file':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
         
            'blood_pressure_systolic':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'past_medical_history':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
        } 
   
###########3 lab requests ############3

class AddLabTestRequestForm(CommonBaseForm):
    company_filtered_fields = {
        'medical_file': CommonTransactionsModel,
        'items': CommonStocksModel,
       
        }
    
    class Meta(CommonBaseForm.Meta):
        model = LabTestRequestsModel
        fields = CommonBaseForm.Meta.fields + ['medical_file','date_time','items',
                  'lab_name','status','priority','specimen','description',
                 ]
        widgets={
            **CommonBaseForm.Meta.widgets,
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
          
            'date_time' : DatePickerInput(attrs={'class':'form-control'}),
            
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          
            'medical_file':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            'lab_name':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'priority':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'specimen':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           

        } 
    
###############33 lab results #############

class AddLabTestResultForm(CommonBaseForm):
    company_filtered_fields = {
        'medical_file': CommonTransactionsModel,
        'test_request': LabTestRequestsModel,
       
        }
    
    class Meta(CommonBaseForm.Meta):
        model = LabTestResultsModel
        fields = CommonBaseForm.Meta.fields + ['medical_file','date_time','results',
                  'lab_name','test_request',
                 ]
        widgets={
            **CommonBaseForm.Meta.widgets,
          
            'results':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
            'date_time' : DatePickerInput(attrs={'class':'form-control'}),
            
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          
            'medical_file':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            'lab_name':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'test_request':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
       
        } 
   
class AddPrescriptionForm(CommonBaseForm):
    company_filtered_fields = {
        'medical_file': CommonTransactionsModel,
        'medication': CommonStocksModel,
        'prescribed_by_doctor': CommonEmployeesModel,
        'issued_by_pharmacist': CommonEmployeesModel,
       
        }
    
    class Meta(CommonBaseForm.Meta):
        model = MedicationsModel
        fields = CommonBaseForm.Meta.fields + ['medical_file','is_issued','quantity','via','medication','dosage_form','dosage',
                  'frequency','duration','prescribed_by_doctor','instructions','issued_by_pharmacist',
                  'issued_date_time']
        widgets={
            **CommonBaseForm.Meta.widgets,
            'frequency':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'issued_date_time' : DatePickerInput(attrs={'class':'form-control'}),
            'instructions':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
            'dosage':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'dosage_form':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'medication':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'quantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'duration':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'medical_file':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'via':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'issued_by_pharmacist':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            'prescribed_by_doctor':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
        } 
   
class AddAdmissionForm(CommonBaseForm):
    company_filtered_fields = {
        'admitting_doctor': CommonEmployeesModel,
       
        }
    
    class Meta(CommonBaseForm.Meta):
        model = AdmissionsModel
        fields = CommonBaseForm.Meta.fields + ['medical_file','ward','bed','admission_date_time',
                  'status','admitting_doctor','reason_for_admission'
                  ]
        widgets={
            **CommonBaseForm.Meta.widgets,
            'reason_for_admission':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'medical_file':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'ward':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'bed':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'admitting_doctor':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'admission_date_time' : DatePickerInput(attrs={'class':'form-control'}),
           
        } 
   
class AddMedicalAdminstrationForm(CommonBaseForm):
    company_filtered_fields = {
        'medical_file': CommonTransactionsModel,
       
        }
    class Meta(CommonBaseForm.Meta):
        model = MedicalAdministrationsModel
        fields = CommonBaseForm.Meta.fields + ['medical_file','prescription','administered_by_nurse',
                  'dosage_value','dosage_unit','given_on','via',
                 
                  ]
        widgets={
            **CommonBaseForm.Meta.widgets,
            'dosage_value':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'given_on' : DatePickerInput(attrs={'class':'form-control'}),
          
            'administered_by_nurse':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            'prescription':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
           
            'medical_file':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'via':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          
            
            'dosage_unit':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
        } 
  
class AddDischargeForm(CommonBaseForm):
    company_filtered_fields = {
        'admission': AdmissionsModel,
       
        }
    class Meta(CommonBaseForm.Meta):
        model = DischargesModel
        fields = CommonBaseForm.Meta.fields + ['admission','discharge_diagnosis','discharge_summary',
                  'medications_at_discharge','follow_up_plan','recorded_on',
                  ]
        widgets={
            **CommonBaseForm.Meta.widgets,
            
            'discharge_summary':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
            'discharge_diagnosis':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'medications_at_discharge':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'follow_up_plan':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'recorded_on' : DatePickerInput(attrs={'class':'form-control'}),
            'admission':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
        } 
   

class AddReferralForm(CommonBaseForm):
    company_filtered_fields = {
        'medical_file': CommonTransactionsModel,
        'referring_doctor':CommonEmployeesModel,
       
        }
    
    class Meta(CommonBaseForm.Meta):
        model = ReferralsModel
        fields = CommonBaseForm.Meta.fields + ['medical_file','referring_doctor','reason_for_referral','referred_on','referral_type','referred_to_doctor','referred_to_external_organization',
                  'status',
                  ]
        widgets={
            **CommonBaseForm.Meta.widgets,
            'reason_for_referral':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
           
            'referred_on' : DatePickerInput(attrs={'class':'form-control'}),
            
            'medical_file':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'referring_doctor':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'referral_type':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'referred_to_doctor':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'referred_to_external_organization':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
        } 
  