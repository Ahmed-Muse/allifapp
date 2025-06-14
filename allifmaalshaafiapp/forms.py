from django import forms
from .models import *

############################# start of datepicker customization ##############################
class DatePickerInput(forms.DateInput):#use this class whereever you have a date and it will give you the calender
    input_type='date'#
class TimePickerInput(forms.TimeInput):#use this wherever you have time input
    input_type='time'
class DateTimePickerInput(forms.DateTimeInput):#use this wherever you have datetime input
    input_type='datetime'
    ################################# end of datepicker customization ################################


class AddPrescriptionForm(forms.ModelForm):
    class Meta:
        model = MedicationsModel
        fields = ['medical_file','is_issued','quantity','via','medication','dosage_form','dosage','division','branch','department',
                  'frequency','duration','prescribed_by_doctor','instructions','issued_by_pharmacist',
                  'issued_date_time']
        widgets={
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
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'prescribed_by_doctor':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        } 
    def __init__(self,allifmaalparameter,*args,**kwargs):
        super (AddPrescriptionForm,self).__init__(*args,**kwargs) # populates the post
        self.fields['department'].queryset=CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset =CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset=CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['medical_file'].queryset=CommonTransactionsModel.objects.filter(company=allifmaalparameter)
        self.fields['medication'].queryset =CommonStocksModel.objects.filter(company=allifmaalparameter)
        self.fields['prescribed_by_doctor'].queryset=CommonEmployeesModel.objects.filter(company=allifmaalparameter)
        self.fields['issued_by_pharmacist'].queryset=CommonEmployeesModel.objects.filter(company=allifmaalparameter)
        

class AddAdmissionForm(forms.ModelForm):
    class Meta:
        model = AdmissionsModel
        fields = ['medical_file','ward','bed','admission_date_time','description','division','branch','department',
                  'status','admitting_doctor','reason_for_admission'
                  ]
        widgets={
            'reason_for_admission':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'medical_file':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'ward':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'bed':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'admitting_doctor':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'admission_date_time' : DatePickerInput(attrs={'class':'form-control'}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        } 
    def __init__(self,allifmaalparameter,*args,**kwargs):
        super (AddAdmissionForm,self).__init__(*args,**kwargs) # populates the post
        self.fields['department'].queryset=CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset =CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset=CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['medical_file'].queryset=CommonTransactionsModel.objects.filter(company=allifmaalparameter)
       
        self.fields['admitting_doctor'].queryset=CommonEmployeesModel.objects.filter(company=allifmaalparameter)
        

class AddMedicalAdminstrationForm(forms.ModelForm):
    class Meta:
        model = MedicalAdministrationsModel
        fields = ['medical_file','prescription','administered_by_nurse',
                  'dosage_value','dosage_unit','given_on','via','division','branch','department',
                  'comments',
                  ]
        widgets={
            'dosage_value':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
           
            'given_on' : DatePickerInput(attrs={'class':'form-control'}),
          
            'administered_by_nurse':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            'prescription':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
           
            'medical_file':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'via':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          
            
            'dosage_unit':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            

            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        } 
    def __init__(self,allifmaalparameter,*args,**kwargs):
        super (AddMedicalAdminstrationForm,self).__init__(*args,**kwargs) # populates the post
        self.fields['department'].queryset=CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset =CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset=CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['medical_file'].queryset=CommonTransactionsModel.objects.filter(company=allifmaalparameter)
       
     

class AddDischargeForm(forms.ModelForm):
    class Meta:
        model = DischargesModel
        fields = ['admission','discharge_diagnosis','discharge_summary',
                  'medications_at_discharge','follow_up_plan','division','branch','department','recorded_on',
                  ]
        widgets={
            
            'discharge_summary':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
            'discharge_diagnosis':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'medications_at_discharge':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'follow_up_plan':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'recorded_on' : DatePickerInput(attrs={'class':'form-control'}),
            'admission':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        } 
    def __init__(self,allifmaalparameter,*args,**kwargs):
        super (AddDischargeForm,self).__init__(*args,**kwargs) # populates the post
        self.fields['department'].queryset=CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset =CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset=CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['admission'].queryset=AdmissionsModel.objects.filter(company=allifmaalparameter)
     

class AddReferralForm(forms.ModelForm):
    class Meta:
        model = ReferralsModel
        fields = ['medical_file','referring_doctor','reason_for_referral','referred_on','referral_type','referred_to_doctor','referred_to_external_organization','division','branch','department',
                  'status',
                  ]
        widgets={
            'reason_for_referral':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
           
            'referred_on' : DatePickerInput(attrs={'class':'form-control'}),
            
            'medical_file':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'referring_doctor':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'referral_type':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'referred_to_doctor':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'referred_to_external_organization':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        } 
    def __init__(self,allifmaalparameter,*args,**kwargs):
        super (AddReferralForm,self).__init__(*args,**kwargs) # populates the post
        self.fields['department'].queryset=CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset =CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset=CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['medical_file'].queryset=CommonTransactionsModel.objects.filter(company=allifmaalparameter)
       
        self.fields['referring_doctor'].queryset=CommonEmployeesModel.objects.filter(company=allifmaalparameter)
