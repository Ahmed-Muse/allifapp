from django import forms
from .models import *
from allifmaalcommonapp.utils import allif_initialize_form_select_querysets 


# forms.py

from django import forms
from django.forms.widgets import DateInput # Or your specific DatePickerInput import
# from some_app.widgets import DatePickerInput # Example if DatePickerInput is custom
class CommonLearnning(forms.ModelForm):
    """
    form filter has two arguments...
    
    """
    class Meta:
        model=CommonOperationYearsModel
        fields = ['department','branch','division','is_current','description','comments','starts','ends','year']
        widgets={
        'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        'mode':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        'account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
          # the css class that we are passing
        }
    def __init__(self, allifmaalparameter,dept, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['supplier'].queryset =CommonSuppliersModel.objects.filter(company=allifmaalparameter,department=dept)
            self.fields['account'].queryset =CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=29999,department=dept).order_by('code')
            self.fields['account'].queryset =CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=29999,department=dept).order_by('code')

        else:
            self.fields['supplier'].queryset =CommonSuppliersModel.objects.none()
            self.fields['account'].queryset =CommonChartofAccountsModel.objects.none()
# --- Custom Widget (assuming this is how your DatePickerInput works) ---
class DatePickerInput(DateInput):
    input_type = 'date' # Renders as an HTML5 date input

# --- Select2 specific attrs ---
SELECT2_ATTRS = {'class': 'form-control custom-field-class-for-seclect2', 'placeholder': 'Select value'}


############################# start of datepicker customization ##############################
class DatePickerInput(forms.DateInput):#use this class whereever you have a date and it will give you the calender
    input_type='date'#
class TimePickerInput(forms.TimeInput):#use this wherever you have time input
    input_type='time'
class DateTimePickerInput(forms.DateTimeInput):#use this wherever you have datetime input
    input_type='datetime'
    ################################# end of datepicker customization ################################

class CommonAddSectorForm(forms.ModelForm):
    class Meta:
        model=CommonSectorsModel
        fields=['name','notes']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'notes':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        }
class CommonAddDocFormatForm(forms.ModelForm):
    class Meta:
        model = CommonDocsFormatModel
        fields = ['name','notes']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'notes':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        }
class CommonAddDataSortsForm(forms.ModelForm):
    class Meta:
        model = CommonDataSortsModel
        fields = ['name','notes']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'notes':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        }
class CommonAddCompanyDetailsForm(forms.ModelForm):
    class Meta:
        model = CommonCompanyDetailsModel
        fields = ['company','legalname','sector','owner','phone1','email','website', 'logo','address','phone2','pobox','city','country']
        widgets={
            'company':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'legalname':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            #'username':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'phone1':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'country':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'owner':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'sector':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
           
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'pobox':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'phone2':forms.TextInput(attrs={'class':'form-control'}),
            'website':forms.TextInput(attrs={'class':'form-control'}),
            'logo':forms.FileInput(attrs={'class':'form-control'}),
            'created_date' : DatePickerInput(attrs={'class':'form-control'}),
            'edit_date' : DatePickerInput(attrs={'class':'form-control'}),
            
        }

class CommonEditCompanyDetailsFormByAllifAdmin(forms.ModelForm):
    class Meta:
        model = CommonCompanyDetailsModel
        fields = ['company','legalname','can_delete','sector','owner','phone1','email','website', 'logo','address','phone2','pobox','city','country']
        widgets={
            'company':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'legalname':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            #'username':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'phone1':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'country':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'owner':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'sector':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'can_delete':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
           
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'pobox':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'phone2':forms.TextInput(attrs={'class':'form-control'}),
            'website':forms.TextInput(attrs={'class':'form-control'}),
            'logo':forms.FileInput(attrs={'class':'form-control'}),
            'created_date' : DatePickerInput(attrs={'class':'form-control'}),
            'edit_date' : DatePickerInput(attrs={'class':'form-control'}),
            
        }
class CommonAddByClientCompanyDetailsForm(forms.ModelForm):
    class Meta:
        model = CommonCompanyDetailsModel
        fields = ['company','can_delete','legalname','sector','owner','phone1','email','website', 'logo','address','phone2','pobox','city','country']
        widgets={
            'company':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'legalname':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            #'username':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'phone1':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'country':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'owner':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'sector':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'can_delete':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'pobox':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'phone2':forms.TextInput(attrs={'class':'form-control'}),
            'website':forms.TextInput(attrs={'class':'form-control'}),
            'logo':forms.FileInput(attrs={'class':'form-control'}),
             #'passwrd':forms.TextInput(attrs={'class':'form-control','type':'password'}),
        
        }


class CommonAddDivisionForm(forms.ModelForm):
    class Meta:
        model =CommonDivisionsModel
        fields = ['division','legalname','comments','phone','email','address','pobox','city']
        widgets={
            'division':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'legalname':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            #'username':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
           
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'pobox':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'created_date' : DatePickerInput(attrs={'class':'form-control'}),
            'edit_date' : DatePickerInput(attrs={'class':'form-control'}),
            
        }
    #def __init__(self, allifmaalparameter, *args, **kwargs):
        #super(CommonAddDivisionForm, self).__init__(*args, **kwargs)
        #self.fields['company'].queryset = CommonCompanyDetailsModel.objects.filter(company=allifmaalparameter)
       
class CommonAddBranchForm(forms.ModelForm):
    class Meta:
        model =CommonBranchesModel
        fields = ['branch','division','legalname','phone','email','address','pobox','city']
        widgets={
            'branch':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'legalname':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            #'username':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
           
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'pobox':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'created_date' : DatePickerInput(attrs={'class':'form-control'}),
            'edit_date' : DatePickerInput(attrs={'class':'form-control'}),
            
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['division'].queryset = CommonDivisionsModel.all_objects.filter(company=allifmaalparameter)

class CommonAddDepartmentForm(forms.ModelForm):
    class Meta:
        model = CommonDepartmentsModel
        fields = ['department','branch','division','phone','email','address','city','pobox']
        widgets={
            'department':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'pobox':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddDepartmentForm, self).__init__(*args, **kwargs)
       
        self.fields['division'].queryset = CommonDivisionsModel.all_objects.filter(company=allifmaalparameter)
        
        self.fields['branch'].queryset = CommonBranchesModel.all_objects.filter(company=allifmaalparameter)
# forms.py



class CommonAddOperationYearForm(forms.ModelForm):
    class Meta:
        model=CommonOperationYearsModel
        fields = ['department','branch','division','is_current','description','comments','starts','ends','year']
        widgets={
            
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'year':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'starts': DatePickerInput(attrs={'class': 'form-control'}),
            'is_current':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'ends': DatePickerInput(attrs={'class': 'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddOperationYearForm, self).__init__(*args, **kwargs)
       
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        


class CommonAddOperationYearTermForm(forms.ModelForm):
    class Meta:
        model=CommonOperationYearTermsModel
        fields = ['department','branch','division','description','name','comments','starts','ends','operation_year']
        widgets={
            
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'year':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'starts': DatePickerInput(attrs={'class': 'form-control'}),
            'ends': DatePickerInput(attrs={'class': 'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'operation_year':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddOperationYearTermForm, self).__init__(*args, **kwargs)
       
        self.fields['division'].queryset = CommonDivisionsModel.all_objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.all_objects.filter(company=allifmaalparameter)
        
        self.fields['branch'].queryset = CommonBranchesModel.all_objects.filter(company=allifmaalparameter)
        self.fields['operation_year'].queryset = CommonOperationYearsModel.all_objects.filter(company=allifmaalparameter)
        
     

# --- 1. CommonBaseForm: Encapsulates shared fields and widgets ---
class CommonBaseForm(forms.ModelForm):
    """
    An abstract base form for models inheriting CommonBaseModel.
    Includes common fields and their default widgets.
    """
    class Meta:
        model=CommonBaseModel
        fields=['name','description','code','balance','quantity','operation_year','operation_term','comments','number',
                'starts','ends','status','priority','delete_status','reference','division','branch','department',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'balance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'rows': 3}),
            'comments': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'rows': 2}),
            'starts': DatePickerInput(attrs={'class': 'form-control'}),
            'ends': DatePickerInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'status': forms.Select(attrs=SELECT2_ATTRS),
            'operation_year': forms.Select(attrs=SELECT2_ATTRS),
            'operation_term': forms.Select(attrs=SELECT2_ATTRS),
            'priority': forms.Select(attrs=SELECT2_ATTRS),
            'delete_status': forms.Select(attrs=SELECT2_ATTRS),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            # Organizational Foreign Key fields also use Select2
            'company': forms.Select(attrs=SELECT2_ATTRS),
            'division': forms.Select(attrs=SELECT2_ATTRS),
            'branch': forms.Select(attrs=SELECT2_ATTRS),
            'department': forms.Select(attrs=SELECT2_ATTRS),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        starts = cleaned_data.get('starts')
        ends = cleaned_data.get('ends')

        # Example common validation: Ensure end date is not before start date
        if starts and ends and ends < starts:
            self.add_error('ends', "End date cannot be before start date.")
        
        return cleaned_data

    def __init__(self, allifmaalparameter=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply queryset filtering for organizational fields if a company_id is provided
        # This allows child forms to pass their allifmaalparameter (which seems to be a company ID)
        if allifmaalparameter:
            # Filter division, branch, department by the provided company ID
            self.fields['division'].queryset = CommonDivisionsModel.all_objects.filter(company_id=allifmaalparameter)
            self.fields['branch'].queryset = CommonBranchesModel.all_objects.filter(company_id=allifmaalparameter)
            self.fields['department'].queryset = CommonDepartmentsModel.all_objects.filter(company_id=allifmaalparameter)
            self.fields['operation_year'].queryset = CommonOperationYearsModel.all_objects.filter(company_id=allifmaalparameter)
            self.fields['operation_term'].queryset = CommonOperationYearTermsModel.all_objects.filter(company_id=allifmaalparameter)
            
            # Optionally, you might also want to set the initial company field, or restrict its queryset
            # For instance, if the form is always for a specific company, you might hide the 'company' field
            # or pre-select it:
            # self.fields['company'].queryset = CommonCompanyDetailsModel.objects.filter(id=company_id_for_queryset_filter)
            # if 'company' in self.fields and not self.initial.get('company'):
            #     self.initial['company'] = company_id_for_queryset_filter
            #     self.fields['company'].widget = forms.HiddenInput() # Or make it read-only
        else:
            # If no company_id is provided, you might want to show an empty queryset or all
            # Showing none is safer to prevent accidental selection of wrong org units
            self.fields['division'].queryset = CommonDivisionsModel.objects.none()
            self.fields['branch'].queryset = CommonBranchesModel.objects.none()
            self.fields['department'].queryset = CommonDepartmentsModel.objects.none()
            self.fields['operation_year'].queryset = CommonOperationYearsModel.objects.none()
            self.fields['operation_term'].queryset = CommonOperationYearTermsModel.objects.none()
            
            # The 'company' field itself should probably show all companies if no specific filter
            # self.fields['company'].queryset = CommonCompanyDetailsModel.objects.all()


# --- 2. CommonAddCompanyScopeForm: Inherits from CommonBaseForm ---
class CommonAddCompanyScopeForm(CommonBaseForm):
    """
    Form for CommonCompanyScopeModel, inheriting common fields from CommonBaseForm.
    """
    class Meta(CommonBaseForm.Meta): # Inherit Meta options from CommonBaseForm
        model = CommonCompanyScopeModel # Specify the concrete model for this form
  
        fields = CommonBaseForm.Meta.fields + []
        
        # Override or add specific widgets for CommonCompanyScopeModel's own fields.
        # Use **CommonBaseForm.Meta.widgets to bring in all parent widgets.
        widgets = {
            **CommonBaseForm.Meta.widgets, # Bring in all common widgets
            'scope_type': forms.Select(attrs=SELECT2_ATTRS),
            # Use Textarea for TextField model fields
            'scope_resources': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'rows': 3}),
            'scope_constraints': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'rows': 3}),
            'scope_assumptions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'rows': 3}),
            'scope_exclusions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'rows': 3}),
            'scope_stakeholders': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'rows': 3}),
            'scope_risks': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'rows': 3}),
            # Add widgets for 'sponsor' and 'related_scopes' if you added them to the model
            # 'sponsor': forms.Select(attrs=SELECT2_ATTRS),
            # 'related_scopes': forms.SelectMultiple(attrs=SELECT2_ATTRS),
             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }
    
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        

        # If 'sponsor' or 'related_scopes' were added to CommonCompanyScopeModel
        # self.fields['sponsor'].queryset = User.objects.filter(is_staff=True) # Example filter
        # if self.instance and self.instance.pk:
        #     self.fields['related_scopes'].queryset = CommonCompanyScopeModel.objects.exclude(pk=self.instance.pk)


# --- 3. Example: CommonAddTaxParametersForm inheriting from CommonBaseForm.. ---
class CommonAddTaxParameterForm(CommonBaseForm):
    """
    Form for CommonTaxParametersModel, inheriting common fields from CommonBaseForm.
    """
    class Meta(CommonBaseForm.Meta): # Inherit Meta options from CommonBaseForm
        model = CommonTaxParametersModel # Specify the concrete model for this form
        
        # Define fields specific to CommonTaxParametersModel
        fields = CommonBaseForm.Meta.fields + ['taxtype','taxrate']
        
        # Override or add specific widgets for new fields
        widgets = {
            **CommonBaseForm.Meta.widgets, # Bring in all common widgets
            'taxtype': forms.Select(attrs=SELECT2_ATTRS),
            'taxrate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tax Rate'}),
           
        }

    # Keep your specific clean method for taxrate
    def clean_taxrate(self):
        taxrate = self.cleaned_data.get('taxrate')
        if taxrate is not None and taxrate < 0: # Check for None explicitly
            raise ValidationError("Tax Rate cannot be negative")
        return taxrate
 
    def __init__(self, allifmaalparameter, *args, **kwargs): # Assuming this form also needs the company parameter
        super().__init__(allifmaalparameter, *args, **kwargs)
        # Add specific queryset filtering for this form if needed, e.g., for taxtype
        pass
    



# --- 2. CommonAddOperationYearTermForm: Inherits from CommonBaseForm ---

   
             
"""
class CommonAddOperationYearTermForm(forms.ModelForm):
    class Meta:
        model=CommonOperationYearTermsModel
        fields = ['operation_year','name','is_active','comments','department','is_current','branch','division']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'end_date':DatePickerInput(attrs={'class':'form-control'}),
            'start_date':DatePickerInput(attrs={'class':'form-control'}),
            'is_current':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'operation_year':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddOperationYearTermForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['operation_year'].queryset =CommonOperationYearsModel.objects.filter(company=allifmaalparameter)
"""
 
"""
class CommonAddCompanyScopeForm(models.Model):
    class Meta:
        model = CommonCompanyScopeModel
        fields = ['name','comments','division','reference','branch','department','starts','ends','delete_status','description','status','priority',
                  'scope_type','scope_resources','scope_constraints','scope_assumptions','scope_exclusions',
                  'scope_stakeholders','scope_risks'
                  ]
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'scope_resources':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'scope_constraints':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'scope_assumptions':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'scope_exclusions':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'scope_stakeholders':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'scope_risks':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
            
            
            'reference':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'starts' : DatePickerInput(attrs={'class':'form-control'}),
            'ends' : DatePickerInput(attrs={'class':'form-control'}),
            'delete_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'priority':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'scope_type':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        } 
    def __init__(self,allifmaalparameter,*args,**kwargs):
        super (CommonAddCompanyScopeForm,self).__init__(*args,**kwargs) # populates the post
        self.fields['department'].queryset=CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset =CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset=CommonBranchesModel.objects.filter(company=allifmaalparameter)
"""

class CommonAddStaffProfileForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonEmployeesModel
        fields=CommonBaseForm.Meta.fields + ['firstName','lastName','middleName','gender','department','title','education',
                  'salary','total_salary_paid','salary_payable','salary_balance','username','sysperms']
        widgets = {
            **CommonBaseForm.Meta.widgets,
            'operation_year': forms.Select(attrs=SELECT2_ATTRS), # Assuming operation_year is a ForeignKey
            
            'firstName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'lastName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'middleName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'education':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'salary':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'total_salary_paid':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'salary_payable':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'salary_balance':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'gender':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'username':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'sysperms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
       
        }

    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['username'].queryset =User.objects.filter(usercompany=allifmaalparameter)
            self.fields['username'].queryset =User.objects.all()
            
        else:
            self.fields['username'].queryset =User.objects.none()
    
    
      
#################### taxes #####################3


class CommonSupplierAddTaxParameterForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonSupplierTaxParametersModel
        
       
        fields=CommonBaseForm.Meta.fields + ['taxtype','taxrate',]
        
        widgets = {
            **CommonBaseForm.Meta.widgets,
             'taxrate':forms.TextInput(attrs={'class':'form-control'}),
             'taxtype':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        }


######################################### chart of accounts ########################

class CommonAddBankForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonBanksModel
        fields=CommonBaseForm.Meta.fields + ['account','comments','deposit','withdrawal']
        widgets = {
            **CommonBaseForm.Meta.widgets,
            'deposit':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'withdrawal':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'account':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        }

######################################### chart of accounts ########################

class CommonAddGeneralLedgerForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonGeneralLedgersModel
        fields=CommonBaseForm.Meta.fields + []
        widgets = {
            **CommonBaseForm.Meta.widgets,
           
        }



class CommonAddChartofAccountForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonChartofAccountsModel
        fields=CommonBaseForm.Meta.fields + ['category','statement']
        widgets = {
            **CommonBaseForm.Meta.widgets,
            'category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'statement':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }

    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['category'].queryset = CommonGeneralLedgersModel.objects.filter(company=allifmaalparameter)
            web= self.fields.get('website')
            log= self.fields.get('logo')
        else:
            self.fields['category'].queryset = CommonGeneralLedgersModel.objects.none()
             
       


class CommonFilterCOAForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonChartofAccountsModel
        fields=CommonBaseForm.Meta.fields + ['category']
        widgets = {
            **CommonBaseForm.Meta.widgets,
             'category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
        }

    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['category'].queryset = CommonGeneralLedgersModel.objects.filter(company=allifmaalparameter)
           
        else:
            self.fields['category'].queryset = CommonGeneralLedgersModel.objects.none()
             
       

class CommonBankDepositAddForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonShareholderBankDepositsModel
        fields=CommonBaseForm.Meta.fields + ['bank','amount','asset','equity']
        widgets = {
            **CommonBaseForm.Meta.widgets,
            'bank':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'equity':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
         
            'asset':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
        }

    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['bank'].queryset = CommonBanksModel.objects.filter(company=allifmaalparameter)
            self.fields['asset'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999).order_by('code')
            self.fields['equity'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=39999,code__gte=29999).order_by('code')
          
        else:
            self.fields['bank'].queryset = CommonBanksModel.objects.none()
            self.fields['asset'].queryset = CommonChartofAccountsModel.objects.none()
            self.fields['equity'].queryset = CommonChartofAccountsModel.objects.none()
    
    
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        # Define the map for this specific form's fields and their models
        field_model_map = {
            'items': CommonStocksModel,
            'trans_number': CommonTransactionsModel,
        }
        # Call the utility function
        allif_initialize_form_select_querysets(self, allifmaalparameter, field_model_map)

       
       


class CommonBankWithdrawalsAddForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonBankWithdrawalsModel
        fields=CommonBaseForm.Meta.fields + ['bank','amount','asset','bankcoa',]
        widgets = {
            **CommonBaseForm.Meta.widgets,
            'bank':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'equity':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
         
            'asset':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
        }

    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['bank'].queryset = CommonBanksModel.objects.filter(company=allifmaalparameter)
            self.fields['asset'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999).order_by('code')
            self.fields['bankcoa'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999).order_by('code')
        
        else:
            self.fields['bank'].queryset = CommonBanksModel.objects.none()
            self.fields['asset'].queryset = CommonChartofAccountsModel.objects.none()
            self.fields['bankcoa'].queryset = CommonChartofAccountsModel.objects.none()
        


class CommonAddSupplierForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonSuppliersModel
        fields=CommonBaseForm.Meta.fields + ['phone','email','address','city','balance','turnover','contact','country','coverage']
        widgets = {
            **CommonBaseForm.Meta.widgets,
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':''}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'coverage':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
            'turnover':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'contact':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'country':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        }



class CommonCustomerAddForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonCustomersModel
        fields=CommonBaseForm.Meta.fields + ['uid','seen','register','triaged','phone','email',
                                             'address','city','sales','country',
                  'turnover','gender','contact','nextkin','relationship','age','paymentType',
                  'document_number','nationality','blood_group']
        
        widgets = {
            **CommonBaseForm.Meta.widgets,
           'uid':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'document_number':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'nationality':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':''}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'sales':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'balance':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'turnover':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'contact':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'nextkin':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'relationship':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'age':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'country':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'blood_group':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'gender':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'paymentType':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           

             # --- Add widgets for BooleanFields here ---
            'register': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'register-checkbox'}), # Example class and ID
            'triaged': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'triaged-checkbox'}),
            'seen': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'seen-checkbox'}),
        
        
        }




class CommonAddCurrencyForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonCurrenciesModel
        fields=CommonBaseForm.Meta.fields + []
        widgets = {
        **CommonBaseForm.Meta.widgets,
        }



class CommonAddPaymentTermForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonPaymentTermsModel
        fields=CommonBaseForm.Meta.fields + []
        widgets = {
        **CommonBaseForm.Meta.widgets,
        }
  


class CommonAddUnitForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonUnitsModel
        fields=CommonBaseForm.Meta.fields + []
        widgets = {
        **CommonBaseForm.Meta.widgets,
        }
  
    
class CommonAssetsAddForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonAssetsModel
        fields=CommonBaseForm.Meta.fields + ['supplier','current_value','salvage_value','depreciated_by',
                                             'depreciation','terms','asset_account','cost_account',
                                             'quantity','value','lifespan',
                  'acquired','category','employee_in_charge','expires','deposit','asset_status',
'next_service_due','last_service_date','capacity_kg','plate_number','energy_usage','oil_capacity','oil_type',
'primary_meter','starting_odometer','manufactured_year','equipment_model','maker_name'
                  
                  ]
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'quantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'capacity_kg':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
            'plate_number':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'energy_usage':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'oil_capacity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'starting_odometer':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'manufactured_year':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'equipment_model':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'maker_name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
            'oil_type':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'primary_meter':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            
            'value':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'deposit':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'lifespan':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'terms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'asset_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'cost_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'acquired' : DatePickerInput(attrs={'class':'form-control'}),
            'expires' : DatePickerInput(attrs={'class':'form-control'}),
            'next_service_due' : DatePickerInput(attrs={'class':'form-control'}),
            'last_service_date' : DatePickerInput(attrs={'class':'form-control'}),
           
            'category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'employee_in_charge':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'asset_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'current_value':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'depreciated_by':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'salvage_value':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'depreciation':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['asset_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999).order_by('code')
            self.fields['cost_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999).order_by('code')
            self.fields['supplier'].queryset = CommonSuppliersModel.objects.filter(company=allifmaalparameter,)
            self.fields['category'].queryset = CommonCategoriesModel.objects.filter(company=allifmaalparameter,)
            self.fields['employee_in_charge'].queryset = CommonEmployeesModel.objects.filter(company=allifmaalparameter,)
           
        else:
            self.fields['asset_account'].queryset = CommonChartofAccountsModel.objects.none()
            self.fields['cost_account'].queryset = CommonChartofAccountsModel.objects.none()
            self.fields['supplier'].queryset = CommonSuppliersModel.objects.none()
            self.fields['category'].queryset = CommonCategoriesModel.objects.none()
            self.fields['employee_in_charge'].queryset = CommonEmployeesModel.objects.none()
     

class CommonExpensesAddForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonExpensesModel
        fields=CommonBaseForm.Meta.fields +  ['supplier','mode','expense_account','amount',]
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
          
            'mode':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'expense_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          
        }
        
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['expense_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=59999,code__gte=49999)
            self.fields['supplier'].queryset = CommonSuppliersModel.objects.filter(company=allifmaalparameter,)
     
        else:
            self.fields['expense_account'].queryset = CommonChartofAccountsModel.objects.none()
            self.fields['supplier'].queryset = CommonSuppliersModel.objects.none()
         
    
    """
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        # Define the map for this specific form's fields and their models
        field_model_map = {
            'expense_account': CommonChartofAccountsModel,
            'supplier': CommonSuppliersModel,
        }
        # Call the utility function
        initialize_form_select_querysets(self, allifmaalparameter, field_model_map)

        """


class CommonAddSpaceItemForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonSpaceItemsModel
        fields=CommonBaseForm.Meta.fields +  ['items','quantity']
        widgets = {
        **CommonBaseForm.Meta.widgets,
           'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
           self.fields['items'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)
        else:
            self.fields['items'].queryset = CommonStocksModel.objects.none()
    

class CommonAddSpaceBookingItemForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonSpaceBookingItemsModel
        fields=CommonBaseForm.Meta.fields + ['space','space_unit','quantity']
        widgets = {
        **CommonBaseForm.Meta.widgets,
           'space':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'space_unit':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['space'].queryset = CommonSpacesModel.objects.filter(company=allifmaalparameter)
            self.fields['space_unit'].queryset = CommonSpaceUnitsModel.objects.filter(company=allifmaalparameter)
       
        else:
            self.fields['space'].queryset = CommonSpacesModel.objects.none()
            self.fields['space_unit'].queryset = CommonSpaceUnitsModel.objects.none()
          


class CommonAddTransferOrderDetailsForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonStockTransferOrdersModel
        fields=CommonBaseForm.Meta.fields + ['from_store','to_store']
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'from_store':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'to_store':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['from_store'].queryset =CommonSpacesModel.objects.filter(company=allifmaalparameter or 1)
            self.fields['to_store'].queryset = CommonSpacesModel.objects.filter(company=allifmaalparameter or 1)
        else:
            self.fields['from_store'].queryset =CommonSpacesModel.objects.none()
            self.fields['to_store'].queryset = CommonSpacesModel.objects.none()


class CommonAddTransferOrderItemForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonStockTransferOrderItemsModel
        fields=CommonBaseForm.Meta.fields + ['items','quantity','trans_ord_items_con']
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['items'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)
    
        else:
           self.fields['items'].queryset = CommonStocksModel.objects.none()
       
      

class CommonAddApproverForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonApproversModel
        fields=CommonBaseForm.Meta.fields + ['approvers',]
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'approvers':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['approvers'].queryset=CommonEmployeesModel.objects.filter(company=allifmaalparameter or 1)
    
        else:
            self.fields['approvers'].queryset=CommonEmployeesModel.objects.none()


class CommonAddCodeForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonCodesModel
        fields=CommonBaseForm.Meta.fields + []
        widgets = {
        **CommonBaseForm.Meta.widgets,
            
        }



class CommonAddCreditNoteDetailsForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonCreditNotesModel
        fields=CommonBaseForm.Meta.fields + ['customer','return_location','approval_status','original_invoice','reasons','total_amount']
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'original_invoice':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'total_amount':forms.TextInput(attrs={'class':'form-control'}),
            'reasons':forms.TextInput(attrs={'class':'form-control'}),
            'approval_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'return_location':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['original_invoice'].queryset = CommonInvoicesModel.objects.filter(company=allifmaalparameter or 1)
            self.fields['customer'].queryset = CommonCustomersModel.objects.filter(company=allifmaalparameter or 1)
            self.fields['return_location'].queryset = CommonSpacesModel.objects.filter(company=allifmaalparameter or 1)

        else:
            self.fields['original_invoice'].queryset = CommonInvoicesModel.objects.none()
            self.fields['customer'].queryset = CommonCustomersModel.objects.none()
            self.fields['return_location'].queryset = CommonSpacesModel.objects.none()



class CommonAddCreditNoteItemForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonCreditNoteItemsModel
        fields=CommonBaseForm.Meta.fields + ['items','quantity']
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['items'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)
        else:
            self.fields['items'].queryset = CommonStocksModel.objects.none()
    
####################################3 CATEGORIES ##############################33

class CommonCategoryAddForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonCategoriesModel
        fields=CommonBaseForm.Meta.fields + []
        widgets = {
        **CommonBaseForm.Meta.widgets,
          
        }
    

class CommonStockItemAddForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonStocksModel
        fields=CommonBaseForm.Meta.fields +  ['category','total_units_sold','weight','expires','item_state','normal_range',
                  'length','height','width','units',
                  'warehouse','suppliertaxrate',
                 'taxrate','criticalnumber','buyingPrice', 'quantity','unitcost','unitPrice','inventory_account','income_account','expense_account','standardUnitCost']
        widgets = {
        **CommonBaseForm.Meta.widgets,
           
            'normal_range':forms.TextInput(attrs={'class':'form-control'}),
            
            'weight':forms.TextInput(attrs={'class':'form-control'}),
            'height':forms.TextInput(attrs={'class':'form-control'}),
            'length':forms.TextInput(attrs={'class':'form-control'}),
            'width':forms.TextInput(attrs={'class':'form-control'}),
            'expires' : DatePickerInput(attrs={'class':'form-control'}),
            
          
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'unitcost':forms.TextInput(attrs={'class':'form-control'}),
            'total_units_sold':forms.TextInput(attrs={'class':'form-control'}),
            'unitPrice':forms.TextInput(attrs={'class':'form-control'}),
            'criticalnumber':forms.TextInput(attrs={'class':'form-control'}),
            'standardUnitCost':forms.TextInput(attrs={'class':'form-control'}),
            'buyingPrice':forms.TextInput(attrs={'class':'form-control'}),
            'item_state':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'units':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'warehouse':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'inventory_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'taxrate':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'suppliertaxrate':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'income_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'expense_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            
          # the css class that we are passing
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['inventory_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999)
            self.fields['expense_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999)
            self.fields['income_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=49999,code__gte=39999)
            self.fields['category'].queryset = CommonCategoriesModel.objects.filter(company=allifmaalparameter)
           
            self.fields['warehouse'].queryset=CommonSpacesModel.objects.filter(company=allifmaalparameter)
            self.fields['suppliertaxrate'].queryset=CommonSupplierTaxParametersModel.objects.filter(company=allifmaalparameter)
            self.fields['taxrate'].queryset=CommonTaxParametersModel.objects.filter(company=allifmaalparameter)
        else:
            self.fields['inventory_account'].queryset = CommonChartofAccountsModel.objects.none()
            self.fields['expense_account'].queryset = CommonChartofAccountsModel.objects.none()
            self.fields['income_account'].queryset = CommonChartofAccountsModel.objects.none()
            self.fields['category'].queryset = CommonCategoriesModel.objects.none()
           
            self.fields['warehouse'].queryset=CommonSpacesModel.objects.none()
            self.fields['suppliertaxrate'].queryset=CommonSupplierTaxParametersModel.objects.none()
            self.fields['taxrate'].queryset=CommonTaxParametersModel.objects.none()



class CommonPOAddForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonPurchaseOrdersModel
        fields=CommonBaseForm.Meta.fields +  ['misccosts','approval_status','uplift','taxrate','currency','delivery',
            'grandtotal','taxamount','amount','supplier','payment_terms','posting_po_status']
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'uplift':forms.TextInput(attrs={'class':'form-control'}),
            'misccosts':forms.TextInput(attrs={'class':'form-control'}),
            'amount':forms.TextInput(attrs={'class':'form-control'}),
            'taxamount':forms.TextInput(attrs={'class':'form-control'}),
            'grandtotal':forms.TextInput(attrs={'class':'form-control'}),
           
            'taxrate':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'payment_terms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'posting_po_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'store':forms.Select(attrs={'class':'form-control'}),
           
            'currency':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'delivery':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'approval_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
          # the css class that we are passing
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['supplier'].queryset = CommonSuppliersModel.objects.filter(company=allifmaalparameter)
            self.fields['taxrate'].queryset = CommonSupplierTaxParametersModel.objects.filter(company=allifmaalparameter)
            self.fields['currency'].queryset = CommonCurrenciesModel.objects.filter(company=allifmaalparameter)
            self.fields['payment_terms'].queryset = CommonPaymentTermsModel.objects.filter(company=allifmaalparameter)
        else:
            self.fields['supplier'].queryset = CommonSuppliersModel.objects.none()
            self.fields['taxrate'].queryset = CommonSupplierTaxParametersModel.objects.none()
            self.fields['currency'].queryset = CommonCurrenciesModel.objects.none()
            self.fields['payment_terms'].queryset = CommonPaymentTermsModel.objects.none()
   


class CommonPOItemAddForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonPurchaseOrderItemsModel
        fields=CommonBaseForm.Meta.fields +  ['items','quantity', 'unitcost','discount']
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'quantity':forms.TextInput(attrs={'class':'form-control'}),
        'unitcost':forms.TextInput(attrs={'class':'form-control'}),
        'discount':forms.TextInput(attrs={'class':'form-control'}),
        'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'})
          # the css class that we are passing
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['items'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)
        else:
            self.fields['items'].queryset = CommonStocksModel.objects.none()



class CommonPOMiscCostAddForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonPurchaseOrderMiscCostsModel
        fields=CommonBaseForm.Meta.fields +  ['supplier','unitcost','quantity','po_misc_cost_con']
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'amount':forms.TextInput(attrs={'class':'form-control'}),
        'unitcost':forms.TextInput(attrs={'class':'form-control'}),
        'quantity':forms.TextInput(attrs={'class':'form-control'}),
        'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        'po_misc_cost_con':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
          # the css class that we are passing
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['supplier'].queryset = CommonSuppliersModel.objects.filter(company=allifmaalparameter)
        else:
            self.fields['supplier'].queryset = CommonSuppliersModel.objects.none()

####################################### SPACES ################


class CommonAddSpaceForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonSpacesModel
        fields=CommonBaseForm.Meta.fields + ['asset','emplyee_in_charge','number_of_units',
                  'capacity','amenities',
                  'max_occupancy','monthly_rent','base_price_per_night',
                  'current_status','name','space_floor','space_type','number_of_bedrooms',
                  'number_of_bathrooms']
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'number_of_units':forms.TextInput(attrs={'class':'form-control'}),
        'number_of_bedrooms':forms.TextInput(attrs={'class':'form-control'}),
        'number_of_bathrooms':forms.TextInput(attrs={'class':'form-control'}),
        'contact_phone':forms.TextInput(attrs={'class':'form-control'}),
           
        'capacity':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),
        'address':forms.TextInput(attrs={'class':'form-control'}),
        'amenities':forms.TextInput(attrs={'class':'form-control'}),
        'max_occupancy':forms.TextInput(attrs={'class':'form-control'}),
        'monthly_rent':forms.TextInput(attrs={'class':'form-control'}),
        'base_price_per_night':forms.TextInput(attrs={'class':'form-control'}),
        'description':forms.TextInput(attrs={'class':'form-control'}),
        'asset':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'space_type':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'space_floor':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'current_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        #'inventory_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'emplyee_in_charge':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
          # the css class that we are passing
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['asset'].queryset=CommonAssetsModel.objects.filter(company=allifmaalparameter)

        else:
            self.fields['asset'].queryset=CommonAssetsModel.objects.none()



class CommonAddSpaceUnitForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonSpaceUnitsModel
        fields=CommonBaseForm.Meta.fields + ['space','number','unitcost','unitprice','area_sqm','rooms','washrooms','unit_type',
                  'emplyee_in_charge','capacity','amenities','max_occupancy','monthly_rent','base_price_per_night','current_status','name','space_floor','space_type',
                 ]
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'unitcost':forms.TextInput(attrs={'class':'form-control'}),
        'unitprice':forms.TextInput(attrs={'class':'form-control'}),
        'area_sqm':forms.TextInput(attrs={'class':'form-control'}),
        'rooms':forms.TextInput(attrs={'class':'form-control'}),
        'washrooms':forms.TextInput(attrs={'class':'form-control'}),
        
        'contact_phone':forms.TextInput(attrs={'class':'form-control'}),
            #'taxname':forms.TextInput(attrs={'class':'form-control','value':mydefault}),
        'space_number':forms.TextInput(attrs={'class':'form-control'}),
        'capacity':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),
        'address':forms.TextInput(attrs={'class':'form-control'}),
        'amenities':forms.TextInput(attrs={'class':'form-control'}),
        'max_occupancy':forms.TextInput(attrs={'class':'form-control'}),
        'monthly_rent':forms.TextInput(attrs={'class':'form-control'}),
        'base_price_per_night':forms.TextInput(attrs={'class':'form-control'}),
        'description':forms.TextInput(attrs={'class':'form-control'}),
        'asset':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'space_type':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'space_floor':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'current_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'inventory_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'emplyee_in_charge':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'unit_type':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'space':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
          # the css class that we are passing
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['space'].queryset=CommonSpacesModel.objects.filter(company=allifmaalparameter)

        else:
            self.fields['space'].queryset=CommonSpacesModel.objects.none()
  
##################### quotes ################

class CommonAddQuoteDetailsForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonQuotesModel
        fields=CommonBaseForm.Meta.fields + ['customer','delivery','payment_terms','currency','prospect','currency','discount','tax','discountValue','salestax']
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'tax':forms.TextInput(attrs={'class':'form-control'}),
            'discountValue':forms.TextInput(attrs={'class':'form-control'}),
            'currency':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'delivery':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'terms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'prospect':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'currency':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'discount':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'payment_terms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'salestax':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
          # the css class that we are passing
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['customer'].queryset = CommonCustomersModel.objects.filter(company=allifmaalparameter)
            self.fields['salestax'].queryset = CommonTaxParametersModel.objects.filter(company=allifmaalparameter)
            self.fields['currency'].queryset = CommonCurrenciesModel.objects.filter(company=allifmaalparameter)
            self.fields['payment_terms'].queryset = CommonPaymentTermsModel.objects.filter(company=allifmaalparameter)
        
          
        else:
            self.fields['customer'].queryset = CommonCustomersModel.objects.none()
            self.fields['salestax'].queryset = CommonTaxParametersModel.objects.none()
            self.fields['currency'].queryset = CommonCurrenciesModel.objects.none()
            self.fields['payment_terms'].queryset = CommonPaymentTermsModel.objects.none()
       


class CommonAddQuoteItemsForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonQuoteItemsModel
        fields=CommonBaseForm.Meta.fields + ['quantity','discount','items' ]
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'quantity':forms.TextInput(attrs={'class':'form-control'}),
        'discount':forms.TextInput(attrs={'class':'form-control'}),
        'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          # the css class that we are passing
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['items'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)

        else:
            self.fields['items'].queryset = CommonStocksModel.objects.none()

            


class CommonAddInvoiceDetailsForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonInvoicesModel
        fields=CommonBaseForm.Meta.fields +['customer','posting_inv_status','invoice_status','delivery','payment_terms','currency','discount','tax','discountValue','salestax']
        widgets = {
        **CommonBaseForm.Meta.widgets,
      
        'tax':forms.TextInput(attrs={'class':'form-control'}),
        'delivery':forms.TextInput(attrs={'class':'form-control'}),
        'discountValue':forms.TextInput(attrs={'class':'form-control'}),
        'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        'invoice_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),

        'posting_inv_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        'payment_terms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        'currency':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        'discount':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        'salestax':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
          # the css class that we are passing
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['customer'].queryset = CommonCustomersModel.objects.filter(company=allifmaalparameter)
            self.fields['salestax'].queryset = CommonTaxParametersModel.objects.filter(company=allifmaalparameter)
            self.fields['currency'].queryset = CommonCurrenciesModel.objects.filter(company=allifmaalparameter)
            self.fields['payment_terms'].queryset = CommonPaymentTermsModel.objects.filter(company=allifmaalparameter)
           
        else:
            self.fields['customer'].queryset = CommonCustomersModel.objects.none()
            self.fields['salestax'].queryset = CommonTaxParametersModel.objects.none()
            self.fields['currency'].queryset = CommonCurrenciesModel.objects.none()
            self.fields['payment_terms'].queryset = CommonPaymentTermsModel.objects.none()
    


class CommonAddInvoiceItemsForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonInvoiceItemsModel
        fields=CommonBaseForm.Meta.fields + ['quantity','discount','items' ]
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'quantity':forms.TextInput(attrs={'class':'form-control'}),
        'discount':forms.TextInput(attrs={'class':'form-control'}),
        'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          # the css class that we are passing
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['items'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)

        else:
            self.fields['items'].queryset = CommonStocksModel.objects.none()
                  



class CommonAddSupplierPaymentForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonSupplierPaymentsModel
        fields=CommonBaseForm.Meta.fields + ['supplier','amount','account','mode']
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        'mode':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        'account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
          # the css class that we are passing
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['supplier'].queryset =CommonSuppliersModel.objects.filter(company=allifmaalparameter)
            self.fields['account'].queryset =CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=29999).order_by('code')
            self.fields['account'].queryset =CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=29999).order_by('code')

        else:########
            self.fields['supplier'].queryset =CommonSuppliersModel.objects.none()
            self.fields['account'].queryset =CommonChartofAccountsModel.objects.none()

     

class CommonAddCustomerPaymentForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonCustomerPaymentsModel
        fields=CommonBaseForm.Meta.fields + ['customer','amount','mode','account']
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
       'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        'mode':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
       
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['customer'].queryset =CommonCustomersModel.objects.filter(company=allifmaalparameter)
            self.fields['account'].queryset =CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999)
        else:
            self.fields['customer'].queryset =CommonCustomersModel.objects.none()
            self.fields['account'].queryset =CommonChartofAccountsModel.objects.none()


class CommonAddSalaryForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonSalariesModel
        fields=CommonBaseForm.Meta.fields +["staff",'amount','account','mode','salary_payable']
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'staff':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'salary_payable':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
          
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'mode':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['staff'].queryset =CommonEmployeesModel.objects.filter(company=allifmaalparameter)
            self.fields['account'].queryset =CommonChartofAccountsModel.objects.filter(company=allifmaalparameter)
        else:
            self.fields['staff'].queryset =CommonEmployeesModel.objects.none()
            self.fields['account'].queryset =CommonChartofAccountsModel.objects.none()
     
####################################3 Transactions ##############################33

class CommonAddTransactionDetailsForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonTransactionsModel
        fields=CommonBaseForm.Meta.fields + ['customer','payment_mode','employee_in_charge','amount']
        widgets = {
        **CommonBaseForm.Meta.widgets,
       'employee_in_charge':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        'payment_mode':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        
      
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['customer'].queryset = CommonCustomersModel.objects.filter(company=allifmaalparameter)
        
            self.fields['payment_mode'].queryset = CommonPaymentTermsModel.objects.filter(company=allifmaalparameter)
        
        else:
            self.fields['customer'].queryset = CommonCustomersModel.objects.none()
            self.fields['payment_mode'].queryset = CommonPaymentTermsModel.objects.none()
        
####################################3 Transactions ##############################33

class CommonAddTransactionItemForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonTransactionItemsModel
        fields=CommonBaseForm.Meta.fields + ['items','trans_number']
        widgets = {
        **CommonBaseForm.Meta.widgets,
       'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
       'trans_number':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['items'].queryset =CommonStocksModel.objects.filter(company=allifmaalparameter)
            self.fields['trans_number'].queryset=CommonTransactionsModel.objects.filter(company=allifmaalparameter)
        else:
            self.fields['items'].queryset =CommonStocksModel.objects.none()
            self.fields['trans_number'].queryset=CommonTransactionsModel.objects.none()

class CommonAddJobDetailsForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonJobsModel
        fields=CommonBaseForm.Meta.fields + ['customer','job_status','payment_terms','currency']
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        'job_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        'payment_terms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        'currency':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['customer'].queryset =CommonCustomersModel.objects.filter(company=allifmaalparameter)
            self.fields['currency'].queryset =CommonCurrenciesModel.objects.filter(company=allifmaalparameter)
        else:
            self.fields['customer'].queryset =CommonCustomersModel.objects.none()
            self.fields['currency'].queryset =CommonCurrenciesModel.all_objects.none()
       


class CommonAddJobItemsForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonJobItemsModel
        fields=CommonBaseForm.Meta.fields + ['item']
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'item':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['item'].queryset =CommonStocksModel.objects.filter(company=allifmaalparameter)
       
        else:
            self.fields['item'].queryset =CommonStocksModel.objects.none()
       



class CommonAddTasksForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonTasksModel
        fields=CommonBaseForm.Meta.fields + ['task','task_status','taskDay','assignedto']
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'task':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        'dueDate':DatePickerInput(attrs={'class':'form-control','placeholder':'Task due date'}),
        'taskDay':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        'task_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        'assignedto':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['assignedto'].queryset = CommonEmployeesModel.objects.filter(company=allifmaalparameter)
       
        else:
            self.fields['assignedto'].queryset = CommonEmployeesModel.objects.none()
       
      
 ############################### shipments... ##################3
 
####################################3 Transactions ##############################33


class CommonAddTransitDetailsForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonTransitModel
        fields=CommonBaseForm.Meta.fields + ['carrier','received_on','expected','origin','via','terms','currency',
                  'dispatched_by','customer','received_by','transit_status',
                  'destination','delivery_confirmed_by_employee','delivery_confirmation_date_time',
                  'exit_warehouse','supplier','delivery_confirmed_by_customer','delivery_notes',
                  'entry_warehouse',]
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'delivery_notes':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'delivery_confirmed_by_employee':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'delivery_confirmed_by_customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'dispatched_by':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'received_by':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'terms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'currency':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'carrier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'shipment_number':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'transit_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'origin':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'entry_warehouse':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'exit_warehouse':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'via':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          
            'employee_in_charge':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'destination':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'expected':DatePickerInput(attrs={'class':'form-control'}),
            
            'received_on':DatePickerInput(attrs={'class':'form-control'}),
            'delivery_confirmation_date_time':DatePickerInput(attrs={'class':'form-control'}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['exit_warehouse'].queryset =CommonSpacesModel.objects.filter(company=allifmaalparameter)
            self.fields['entry_warehouse'].queryset =CommonSpacesModel.objects.filter(company=allifmaalparameter)
            self.fields['supplier'].queryset =CommonSuppliersModel.objects.filter(company=allifmaalparameter)

   
        else:
            self.fields['exit_warehouse'].queryset =CommonSpacesModel.objects.none()
            self.fields['entry_warehouse'].queryset =CommonSpacesModel.objects.none()
            self.fields['supplier'].queryset =CommonSuppliersModel.objects.none()



class CommonAddTransitItemsForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonTransitItemsModel
        fields=CommonBaseForm.Meta.fields + ['items','unit_of_measure','expected','dispatched_by',
                                             'expires','delivered_on',
                  'consigner','consignee','weight','length','width','height','received','value','rate',
                  'shipment_status','destination','origin',
                  ]
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'origin':forms.TextInput(attrs={'class':'form-control'}),
            'weight':forms.TextInput(attrs={'class':'form-control'}),
            'length':forms.TextInput(attrs={'class':'form-control'}),
            'width':forms.TextInput(attrs={'class':'form-control'}),
            'height':forms.TextInput(attrs={'class':'form-control'}),
            'value':forms.TextInput(attrs={'class':'form-control'}),
            'rate':forms.TextInput(attrs={'class':'form-control'}),
            'destination':forms.TextInput(attrs={'class':'form-control'}),
           
            'received':DatePickerInput(attrs={'class':'form-control'}),
            'expires':DatePickerInput(attrs={'class':'form-control'}),
            'expected':DatePickerInput(attrs={'class':'form-control'}),
            'delivered_on':DatePickerInput(attrs={'class':'form-control'}),
            'consigner':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'consignee':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'shipment_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'dispatched_by':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
           'unit_of_measure':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(allifmaalparameter, *args, **kwargs)
        if allifmaalparameter:
            self.fields['items'].queryset =CommonStocksModel.objects.filter(company=allifmaalparameter)
            self.fields['unit_of_measure'].queryset =CommonUnitsModel.objects.filter(company=allifmaalparameter)
            self.fields['consigner'].queryset =CommonCustomersModel.objects.filter(company=allifmaalparameter)
           
            self.fields['consignee'].queryset =CommonCustomersModel.objects.filter(company=allifmaalparameter)
       
        else:
            self.fields['items'].queryset =CommonStocksModel.objects.none()
            self.fields['unit_of_measure'].queryset =CommonUnitsModel.objects.none()
            self.fields['consigner'].queryset =CommonCustomersModel.objects.none()
           
            self.fields['consignee'].queryset =CommonCustomersModel.objects.none()
 
################################### PROGRESS REPORTING/RECORDINGS .....################

 

class CommonAddProgressForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonProgressModel
        fields=CommonBaseForm.Meta.fields + []
        widgets = {
        **CommonBaseForm.Meta.widgets,
      
        }
  
 