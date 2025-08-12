from .models import *
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


# --- 1. CommonBaseForm: Encapsulates shared fields and widgets ---
class SharedForm(forms.ModelForm):
    """
    An abstract base form for models inheriting SharedBaseModel.
    Includes common fields and their default widgets...
    """
    class Meta:
        model=SharedModel
        fields=['name','notes']
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
           }
        
class CommonAddSectorForm(SharedForm):
    class Meta(SharedForm.Meta):
        model=CommonSectorsModel
        fields=SharedForm.Meta.fields + []
        widgets={**SharedForm.Meta.widgets}
        
class CommonAddDocFormatForm(SharedForm):
    class Meta(SharedForm.Meta):
        model=CommonDocsFormatModel
        fields=SharedForm.Meta.fields + []
        widgets={**SharedForm.Meta.widgets}

class CommonAddDataSortsForm(SharedForm):
    class Meta(SharedForm.Meta):
        model=CommonDataSortsModel
        fields=SharedForm.Meta.fields + []
        widgets={**SharedForm.Meta.widgets}


class BaseForm(forms.ModelForm):
    class Meta:
        model = BaseModel
        fields = ['legalname','name','is_current','reference','starts','ends','priority',
                  'description','comments','status','can_delete','phone','phone1','email','website', 'logo',
                  'address','phone2','pobox','city','country']
        widgets={
            
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
             'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
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
            
             
            'comments': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'rows': 2}),
            'starts': DatePickerInput(attrs={'class': 'form-control'}),
            'ends': DatePickerInput(attrs={'class': 'form-control'}),
           'phone':forms.TextInput(attrs={'class':'form-control'}),
            'can_delete': forms.Select(attrs=SELECT2_ATTRS),
            'status': forms.Select(attrs=SELECT2_ATTRS),
            'is_current': forms.Select(attrs=SELECT2_ATTRS),
           'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'rows': 2}),
            'priority': forms.Select(attrs=SELECT2_ATTRS),
        }
        
        
class CommonAddCompanyDetailsForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=CommonCompanyDetailsModel
        fields=BaseForm.Meta.fields + ['company','sector']
        widgets={**BaseForm.Meta.widgets,
        'sector': forms.Select(attrs=SELECT2_ATTRS),
        'company':forms.TextInput(attrs={'class':'form-control','placeholder':''}),    
        }
     
class CommonEditCompanyDetailsFormByAllifAdmin(BaseForm):
    class Meta(BaseForm.Meta):
        model=CommonCompanyDetailsModel
        fields=BaseForm.Meta.fields + ['company','sector']
        widgets={**BaseForm.Meta.widgets,
        'sector': forms.Select(attrs=SELECT2_ATTRS),
        'company':forms.TextInput(attrs={'class':'form-control','placeholder':''}),    
        }
         
class CommonAddByClientCompanyDetailsForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=CommonCompanyDetailsModel
        fields=BaseForm.Meta.fields + ['company','sector']
        widgets={**BaseForm.Meta.widgets,
        'sector': forms.Select(attrs=SELECT2_ATTRS),
        'company':forms.TextInput(attrs={'class':'form-control','placeholder':''}),    
        }

class CommonAddDivisionForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=CommonDivisionsModel
        fields=BaseForm.Meta.fields + ['division']
        widgets={**BaseForm.Meta.widgets,
        'division':forms.TextInput(attrs={'class':'form-control','placeholder':''}),    
        }

class CommonAddBranchForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=CommonBranchesModel
        fields=BaseForm.Meta.fields + ['division','branch']
        widgets={**BaseForm.Meta.widgets,
        'division': forms.Select(attrs=SELECT2_ATTRS),
        'branch':forms.TextInput(attrs={'class':'form-control','placeholder':''}),    
        }

class CommonAddBranchForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=CommonBranchesModel
        fields=BaseForm.Meta.fields + ['division','branch']
        widgets={**BaseForm.Meta.widgets,
        'division': forms.Select(attrs=SELECT2_ATTRS),
        'branch':forms.TextInput(attrs={'class':'form-control','placeholder':''}),    
        }

    def __init__(self, allifmaalparameter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['division'].queryset = CommonDivisionsModel.all_objects.filter(company=allifmaalparameter)

class CommonAddDepartmentForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=CommonDepartmentsModel
        fields=BaseForm.Meta.fields + ['division','branch','department']
        widgets={**BaseForm.Meta.widgets,
        'division': forms.Select(attrs=SELECT2_ATTRS),
        'branch': forms.Select(attrs=SELECT2_ATTRS),
        'department':forms.TextInput(attrs={'class':'form-control','placeholder':''}),    
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddDepartmentForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.all_objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.all_objects.filter(company=allifmaalparameter)


class CommonAddOperationYearForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=CommonOperationYearsModel
        fields=BaseForm.Meta.fields + ['division','branch','department','year']
        widgets={**BaseForm.Meta.widgets,
        'division': forms.Select(attrs=SELECT2_ATTRS),
        'branch': forms.Select(attrs=SELECT2_ATTRS),
        'department': forms.Select(attrs=SELECT2_ATTRS),
        
        'year':forms.TextInput(attrs={'class':'form-control','placeholder':''}),  
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddOperationYearForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.all_objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.all_objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.all_objects.filter(company=allifmaalparameter)


class CommonAddOperationYearTermForm(BaseForm):
    class Meta(BaseForm.Meta):
        model=CommonOperationYearTermsModel
        fields=BaseForm.Meta.fields + ['division','branch','department','operation_year','operation_term']
        widgets={**BaseForm.Meta.widgets,
        'division': forms.Select(attrs=SELECT2_ATTRS),
        'branch': forms.Select(attrs=SELECT2_ATTRS),
        'department': forms.Select(attrs=SELECT2_ATTRS),
        'operation_year': forms.Select(attrs=SELECT2_ATTRS),
       
        'operation_term':forms.TextInput(attrs={'class':'form-control','placeholder':''}),  
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddOperationYearTermForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.all_objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.all_objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.all_objects.filter(company=allifmaalparameter)
        self.fields['operation_year'].queryset = CommonOperationYearsModel.all_objects.filter(company=allifmaalparameter)
        

# --- 1. CommonBaseForm: Encapsulates shared fields and widgets ---

# --- 1. CommonBaseForm: Encapsulates shared fields and widgets and filtering logic ---
class CommonBaseForm(forms.ModelForm):
    """
    An abstract base form that handles common fields, widgets, and dynamic
    queryset filtering based on the 'allifmaalparameter' (company ID).
    """
    class Meta:
        model = CommonBaseModel
        fields = [
            'name', 'description', 'code', 'balance', 'quantity',
            'operation_year', 'operation_term', 'comments', 'number',
            'starts', 'ends', 'status', 'priority', 'delete_status',
            'reference', 'division', 'branch', 'department',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'balance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '', 'rows': 3}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '', 'rows': 2}),
            'starts': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ends': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'status': forms.Select(attrs=SELECT2_ATTRS),
            'operation_year': forms.Select(attrs=SELECT2_ATTRS),
            'operation_term': forms.Select(attrs=SELECT2_ATTRS),
            'priority': forms.Select(attrs=SELECT2_ATTRS),
            'delete_status': forms.Select(attrs=SELECT2_ATTRS),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            # Organizational Foreign Key fields also use Select2
            'company': forms.Select(attrs=SELECT2_ATTRS),
            'division': forms.Select(attrs=SELECT2_ATTRS),
            'branch': forms.Select(attrs=SELECT2_ATTRS),
            'department': forms.Select(attrs=SELECT2_ATTRS),
        }
        
    # This is a class-level attribute.
    # It contains a default map of fields to their respective models.
    # Child forms can override or extend this.
    company_filtered_fields = {
        'division': CommonDivisionsModel,
        'branch': CommonBranchesModel,
        'department': CommonDepartmentsModel,
        'operation_year': CommonOperationYearsModel,
        'operation_term': CommonOperationYearTermsModel,
    }

    def __init__(self, allifmaalparameter=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # This is the key change!
        # It now iterates over the dictionary, which can be extended by child classes.
        if allifmaalparameter:
            # Loop through all fields that need filtering for this specific form instance
            for field_name, model in self.company_filtered_fields.items():
                if field_name in self.fields:
                    self.fields[field_name].queryset = model.objects.filter(company=allifmaalparameter)
        else:
            for field_name in self.company_filtered_fields.keys():
                if field_name in self.fields:
                    self.fields[field_name].queryset = self.fields[field_name].queryset.none()
    
    def clean(self):
        cleaned_data = super().clean()
        starts = cleaned_data.get('starts')
        ends = cleaned_data.get('ends')
        if starts and ends and ends < starts:
            self.add_error('ends', "End date cannot be before start date.")
        return cleaned_data

class CommonAddCompanyScopeForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonCompanyScopeModel
        fields=CommonBaseForm.Meta.fields + []
        widgets = {
            **CommonBaseForm.Meta.widgets,
            'category': forms.Select(attrs=SELECT2_ATTRS),
            'statement': forms.Select(attrs=SELECT2_ATTRS),
        }

class CommonAddTaxParameterForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonTaxParametersModel
        fields=CommonBaseForm.Meta.fields + ['taxtype','taxrate']
        widgets = {
            **CommonBaseForm.Meta.widgets,
            'taxtype': forms.Select(attrs=SELECT2_ATTRS),
            'taxrate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tax Rate'}),
        }
        
class CommonAddStaffProfileForm(CommonBaseForm):
    # We override the parent's attribute to specify the new fields for THIS form.
    # The parent's __init__ will see this new dictionary and filter these fields.
    company_filtered_fields = {
        'username':User,
        }
    
    class Meta(CommonBaseForm.Meta):
        model = CommonEmployeesModel
        fields = CommonBaseForm.Meta.fields + ['firstName','lastName','middleName','gender','department','title','education',
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
    company_filtered_fields = {
        'category': CommonGeneralLedgersModel,
        }
    
    class Meta(CommonBaseForm.Meta):
        model = CommonChartofAccountsModel
        fields = CommonBaseForm.Meta.fields + ['category', 'statement']
        widgets = {
            **CommonBaseForm.Meta.widgets,
            'category': forms.Select(attrs=SELECT2_ATTRS),
            'statement': forms.Select(attrs=SELECT2_ATTRS),
        }

class CommonFilterCOAForm(CommonBaseForm):
    company_filtered_fields = {
        'category': CommonGeneralLedgersModel,
        }
    class Meta(CommonBaseForm.Meta):
        model=CommonChartofAccountsModel
        fields=CommonBaseForm.Meta.fields + ['category']
        widgets = {
            **CommonBaseForm.Meta.widgets,
             'category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
        }

class CommonBankDepositAddForm(CommonBaseForm):
    company_filtered_fields = {
        'bank': CommonBanksModel,
        'equity': CommonChartofAccountsModel,
        'asset': CommonChartofAccountsModel,
        }
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

   
class CommonBankWithdrawalsAddForm(CommonBaseForm):
    company_filtered_fields = {
        'bank': CommonBanksModel,
        'bankcoa': CommonChartofAccountsModel,
        'asset': CommonChartofAccountsModel,
        }
    
    class Meta(CommonBaseForm.Meta):
        model=CommonBankWithdrawalsModel
        fields=CommonBaseForm.Meta.fields + ['bank','amount','asset','bankcoa',]
        widgets = {
            **CommonBaseForm.Meta.widgets,
            'bank':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'bankcoa':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
         
            'asset':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
        }

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
    company_filtered_fields = {
        'paymentType': CommonPaymentTermsModel,
      
        }
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
    company_filtered_fields = {
        'employee_in_charge': CommonEmployeesModel,
        'asset_account': CommonChartofAccountsModel,
        'cost_account': CommonChartofAccountsModel,
        'supplier': CommonSuppliersModel,
        'category': CommonCategoriesModel,
        'terms': CommonPaymentTermsModel,
        }
    
    class Meta(CommonBaseForm.Meta):
        model=CommonAssetsModel
        fields=CommonBaseForm.Meta.fields + ['supplier','current_value','salvage_value','depreciated_by',
                                             'depreciation','terms','asset_account','cost_account',
                                             'quantity','value','lifespan',
                            'acquired','category','employee_in_charge','expires','deposit','asset_status',
    'next_service_due','last_service_date','capacity_kg',
    'plate_number','energy_usage','oil_capacity','oil_type',
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
   

class CommonExpensesAddForm(CommonBaseForm):
    company_filtered_fields = {
        'expense_account': CommonChartofAccountsModel,
        'supplier': CommonSuppliersModel,
        }
    
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
   

class CommonAddSpaceItemForm(CommonBaseForm):
    company_filtered_fields = {
        'items': CommonStocksModel,
        }
    class Meta(CommonBaseForm.Meta):
        model=CommonSpaceItemsModel
        fields=CommonBaseForm.Meta.fields +  ['items','quantity']
        widgets = {
        **CommonBaseForm.Meta.widgets,
           'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
        }
   
   
class CommonAddSpaceBookingItemForm(CommonBaseForm):
    company_filtered_fields = {
        'space': CommonSpacesModel,
        'space_unit': CommonSpaceUnitsModel,
        }
    
    class Meta(CommonBaseForm.Meta):
        model=CommonSpaceBookingItemsModel
        fields=CommonBaseForm.Meta.fields + ['space','space_unit','quantity']
        widgets = {
        **CommonBaseForm.Meta.widgets,
           'space':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'space_unit':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
        }
   

class CommonAddTransferOrderDetailsForm(CommonBaseForm):
    company_filtered_fields = {
        'from_store': CommonSpacesModel,
        'to_store': CommonSpacesModel,
        }
    class Meta(CommonBaseForm.Meta):
        model=CommonStockTransferOrdersModel
        fields=CommonBaseForm.Meta.fields + ['from_store','to_store']
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'from_store':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'to_store':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        }
   

class CommonAddTransferOrderItemForm(CommonBaseForm):
    company_filtered_fields = {
        'items': CommonStocksModel,
        }
    class Meta(CommonBaseForm.Meta):
        model=CommonStockTransferOrderItemsModel
        fields=CommonBaseForm.Meta.fields + ['items','quantity']
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
        }
   
   
class CommonAddApproverForm(CommonBaseForm):
    company_filtered_fields = {
        'approvers': CommonEmployeesModel,
        }
    
    class Meta(CommonBaseForm.Meta):
        model=CommonApproversModel
        fields=CommonBaseForm.Meta.fields + ['approvers',]
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'approvers':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            
        }
   
class CommonAddCodeForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonCodesModel
        fields=CommonBaseForm.Meta.fields + []
        widgets = {
        **CommonBaseForm.Meta.widgets,
            
        }


class CommonAddCreditNoteDetailsForm(CommonBaseForm):
    company_filtered_fields = {
        'original_invoice': CommonInvoicesModel,
        'customer': CommonCustomersModel,
        'return_location': CommonSpacesModel,
        }
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
   

class CommonAddCreditNoteItemForm(CommonBaseForm):
    company_filtered_fields = {
        'items': CommonStocksModel,
      
        }
    
    class Meta(CommonBaseForm.Meta):
        model=CommonCreditNoteItemsModel
        fields=CommonBaseForm.Meta.fields + ['items','quantity']
        widgets = {
        **CommonBaseForm.Meta.widgets,
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
  
####################################3 CATEGORIES ##############################33

class CommonCategoryAddForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonCategoriesModel
        fields=CommonBaseForm.Meta.fields + []
        widgets = {
        **CommonBaseForm.Meta.widgets,
          
        }

class CommonStockItemAddForm(CommonBaseForm):
    company_filtered_fields = {
        'inventory_account': CommonChartofAccountsModel,
        'expense_account':CommonChartofAccountsModel,
        'suppliertaxrate': CommonSupplierTaxParametersModel,
         'income_account': CommonChartofAccountsModel,
        'taxrate': CommonTaxParametersModel,
        'warehouse': CommonSpacesModel,
        'category': CommonCategoriesModel,
        'units': CommonUnitsModel,
        }
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
   

class CommonPOAddForm(CommonBaseForm):
    company_filtered_fields = {
        'payment_terms': CommonPaymentTermsModel,
        'supplier': CommonSuppliersModel,
        'currency': CommonCurrenciesModel,
        'taxrate': CommonTaxParametersModel,
      
        }
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
 

class CommonPOItemAddForm(CommonBaseForm):
    company_filtered_fields = {
        'items': CommonStocksModel,
       
      
        }
    
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
  
class CommonPOMiscCostAddForm(CommonBaseForm):
    company_filtered_fields = {
        'supplier': CommonSuppliersModel,
        }
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
   
####################################### SPACES ################


class CommonAddSpaceForm(CommonBaseForm):
    company_filtered_fields = {
        'asset': CommonAssetsModel,
        'emplyee_in_charge': CommonEmployeesModel,
        }
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
   

class CommonAddSpaceUnitForm(CommonBaseForm):
    company_filtered_fields = {
        'space': CommonSpacesModel,
        'emplyee_in_charge': CommonEmployeesModel,
        }
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
  
##################### quotes ################

class CommonAddQuoteDetailsForm(CommonBaseForm):
    company_filtered_fields = {
        'payment_terms': CommonPaymentTermsModel,
        'customer': CommonCustomersModel,
        'salestax': CommonTaxParametersModel,
        'currency': CommonCurrenciesModel,
        
        }
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
   

class CommonAddQuoteItemsForm(CommonBaseForm):
    company_filtered_fields = {
        'items': CommonStocksModel,
       
        
        }
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
      


class CommonAddInvoiceDetailsForm(CommonBaseForm):
    company_filtered_fields = {
        'payment_terms': CommonPaymentTermsModel,
        'customer': CommonCustomersModel,
        'salestax': CommonTaxParametersModel,
        'currency': CommonCurrenciesModel,
        
        }
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
   

class CommonAddInvoiceItemsForm(CommonBaseForm):
    company_filtered_fields = {
        'items': CommonStocksModel,
        }
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
  


class CommonAddSupplierPaymentForm(CommonBaseForm):
    company_filtered_fields = {
        'account': CommonChartofAccountsModel,
        'supplier': CommonSuppliersModel,
        }
    
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
   
   
class CommonAddCustomerPaymentForm(CommonBaseForm):
    company_filtered_fields = {
        'account': CommonChartofAccountsModel,
        'customer': CommonCustomersModel,
        }
    
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
  

class CommonAddSalaryForm(CommonBaseForm):
    company_filtered_fields = {
        'account': CommonChartofAccountsModel,
        'staff': CommonEmployeesModel,
        }
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
   
####################################3 Transactions ##############################33

class CommonAddTransactionDetailsForm(CommonBaseForm):
    company_filtered_fields = {
        'payment_mode': CommonPaymentTermsModel,
        'customer': CommonCustomersModel,
        'employee_in_charge': CommonEmployeesModel,
        }
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
   
####################################3 Transactions ##############################33

class CommonAddTransactionItemForm(CommonBaseForm):
    company_filtered_fields = {
        'trans_number': CommonTransactionsModel,
        'items': CommonStocksModel,
        }
    
    class Meta(CommonBaseForm.Meta):
        model=CommonTransactionItemsModel
        fields=CommonBaseForm.Meta.fields + ['items','trans_number']
        widgets = {
        **CommonBaseForm.Meta.widgets,
       'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
       'trans_number':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    
class CommonAddJobDetailsForm(CommonBaseForm):
    
    company_filtered_fields = {
        'customer': CommonCustomersModel,
        'currency': CommonCurrenciesModel,
        }
     
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
    
    
class CommonAddJobItemsForm(CommonBaseForm):
    
    company_filtered_fields = {
        'items': CommonStocksModel,
        }
     
    class Meta(CommonBaseForm.Meta):
        model=CommonJobItemsModel
        fields=CommonBaseForm.Meta.fields + ['item']
        widgets = {
        **CommonBaseForm.Meta.widgets,
        'item':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
  
  
class CommonAddTasksForm(CommonBaseForm):
    
    company_filtered_fields = {
        'assignedto': CommonEmployeesModel,
        }
    
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
   
   
class CommonAddTransitDetailsForm(CommonBaseForm):
    company_filtered_fields = {
        'exit_warehouse': CommonSpacesModel,
        'entry_warehouse': CommonSpacesModel,
        'supplier': CommonSuppliersModel,
        }
     
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


class CommonAddTransitItemsForm(CommonBaseForm):
    company_filtered_fields = {
        'unit_of_measure': CommonUnitsModel,
        'items': CommonStocksModel,
        'consigner': CommonCustomersModel,
        'consignee': CommonCustomersModel,
        }
    
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
   
   
################################### PROGRESS REPORTING/RECORDINGS .....################
class CommonAddProgressForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model=CommonProgressModel
        fields=CommonBaseForm.Meta.fields + []
        widgets = {
        **CommonBaseForm.Meta.widgets,
        }


#############################3 EXAMINATIONS ###################
class CommonAddTestForm(CommonBaseForm):
    company_filtered_fields = {
        'space': CommonSpacesModel,
        'items': CommonStocksModel,
       
        }
    
    class Meta(CommonBaseForm.Meta):
        model = CommonAssessmentsModel
        fields = CommonBaseForm.Meta.fields + ['items','space','specimen','test_status',
                 ]
        widgets={
            **CommonBaseForm.Meta.widgets,
           
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          
          
            'space':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'test_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'specimen':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           

        } 
    
###############33results #############

class CommonAddResultForm(CommonBaseForm):
    class Meta(CommonBaseForm.Meta):
        model = CommonResultsModel
        fields = CommonBaseForm.Meta.fields + []
        widgets={
            **CommonBaseForm.Meta.widgets,
         
           
        } 
   