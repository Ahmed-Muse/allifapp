from django import forms
from .models import *



############################# start of datepicker customization ##############################
class DatePickerInput(forms.DateInput):#use this class whereever you have a date and it will give you the calender
    input_type = 'date'#
class TimePickerInput(forms.TimeInput):#use this wherever you have time input
    input_type = 'time'
class DateTimePickerInput(forms.DateTimeInput):#use this wherever you have datetime input
    input_type = 'datetime'
    ################################# end of datepicker customization ################################

class CommonAddSectorForm(forms.ModelForm):
    class Meta:
        model = CommonSectorsModel
        fields = ['name','notes']
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
        fields = ['company','legalName','created_date','edit_date','sector','owner','phone1','email','website', 'logo','address','phone2','pobox','city','country']
        widgets={
            'company':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'legalName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
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
        fields = ['company','legalName','can_delete','created_date','edit_date','sector','owner','phone1','email','website', 'logo','address','phone2','pobox','city','country']
        widgets={
            'company':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'legalName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            #'username':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'phone1':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'country':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'owner':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'sector':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'can_delete':forms.Select(attrs={'class':'form-control','placeholder':''}),
            
           
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
        fields = ['company','branch','can_delete','legalName','sector','owner','phone1','email','website', 'logo','address','phone2','pobox','city','country']
        widgets={
            'company':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'legalName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            #'username':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'phone1':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'country':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'owner':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'sector':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'can_delete':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'branch':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'pobox':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'phone2':forms.TextInput(attrs={'class':'form-control'}),
            'website':forms.TextInput(attrs={'class':'form-control'}),
            'logo':forms.FileInput(attrs={'class':'form-control'}),
             #'passwrd':forms.TextInput(attrs={'class':'form-control','type':'password'}),
        
        }

class CommonAddCompanyScopeForm(forms.ModelForm):
    class Meta:
        model = CommonCompanyScopeModel
        fields = ['name']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        } 
class CommonAddDivisionForm(forms.ModelForm):
    class Meta:
        model =CommonDivisionsModel
        fields = ['division','legalname','comments','created_date','edit_date','phone','email','address','pobox','city']
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
        fields = ['branch','division','legalname','created_date','edit_date','phone','email','address','pobox','city']
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
        super(CommonAddBranchForm, self).__init__(*args, **kwargs)
        
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
       

class CommonAddStaffProfileForm(forms.ModelForm):
    class Meta:
        model = CommonEmployeesModel
        fields = ['staffNo','division','branch','department','firstName','lastName','middleName','gender','department','title','education',
                  'comment','salary','total_salary_paid','salary_payable','salary_balance','username','sysperms']
        widgets={
            'staffNo':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'firstName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'lastName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'middleName':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'department':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'education':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comment':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'salary':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'total_salary_paid':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'salary_payable':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'salary_balance':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'gender':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'username':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'sysperms':forms.Select(attrs={'class':'form-control','placeholder':''}),
            
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

            
        }

#################### taxes #####################3
class CommonAddTaxParameterForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model = CommonTaxParametersModel
        fields = ['taxname','taxtype','taxrate', 'taxdescription']
        widgets={
            'taxname':forms.TextInput(attrs={'class':'form-control'}),
             #'taxname':forms.TextInput(attrs={'class':'form-control','value':mydefault}),
            'taxrate':forms.TextInput(attrs={'class':'form-control'}),
             'taxtype':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
             'taxdescription':forms.TextInput(attrs={'class':'form-control'}),
             
            
        }
######################################### chart of accounts ########################
class CommonAddBankForm(forms.ModelForm):
    class Meta:
        model = CommonBanksModel
        fields = ['name','balance','division','branch','department','account','comments','deposit','withdrawal']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'balance':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'deposit':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'withdrawal':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'account':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddBankForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
######################################### chart of accounts ########################
class CommonAddGeneralLedgerForm(forms.ModelForm):
    class Meta:
        model = CommonGeneralLedgersModel
        fields = ['description','balance','division','branch','department']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'balance':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddGeneralLedgerForm, self).__init__(*args, **kwargs)
        
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)

class CommonAddChartofAccountForm(forms.ModelForm):
    class Meta:
        model = CommonChartofAccountsModel
        fields = ['description','balance','code','category','comments','statement','division','branch','department']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'balance':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'code':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'statement':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddChartofAccountForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = CommonGeneralLedgersModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        web= self.fields.get('website')
        log= self.fields.get('logo')
        #if web and log.widget.attrs['address'] == 'CUSTOM':
        self.fields['comments'].widget.attrs['disabled'] = 'True'
       
class CommonFilterCOAForm(forms.ModelForm):
    class Meta:
        model =CommonChartofAccountsModel
        fields = ['category','description']
        widgets={'category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),}
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonFilterCOAForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = CommonGeneralLedgersModel.objects.filter(company=allifmaalparameter)
class CommonBankDepositAddForm(forms.ModelForm):
    class Meta:
        model =CommonShareholderBankDepositsModel
        fields = ['description','bank','amount','comments','asset','equity','division','branch','department']
        widgets={
            'bank':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'equity':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
         
            'asset':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          
           
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonBankDepositAddForm, self).__init__(*args, **kwargs)
        self.fields['bank'].queryset = CommonBanksModel.objects.filter(company=allifmaalparameter)
        self.fields['asset'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999).order_by('code')
        self.fields['equity'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=39999,code__gte=29999).order_by('code')

        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
class CommonBankWithdrawalsAddForm(forms.ModelForm):
    class Meta:
        model =CommonBankWithdrawalsModel
        fields = ['description','bank','amount','comments','asset','bankcoa','division','branch','department']
        widgets={
            'bank':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'asset':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'bankcoa':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          
      
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonBankWithdrawalsAddForm, self).__init__(*args, **kwargs)
        self.fields['bank'].queryset = CommonBanksModel.objects.filter(company=allifmaalparameter)
        self.fields['asset'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999).order_by('code')
        self.fields['bankcoa'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999).order_by('code')
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        
class CommonAddDepartmentForm(forms.ModelForm):
    class Meta:
        model = CommonDepartmentsModel
        fields = ['description','comments','branch','division']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddDepartmentForm, self).__init__(*args, **kwargs)
       
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
       
class CommonAddSupplierForm(forms.ModelForm):
    class Meta:
        model = CommonSuppliersModel
        fields = ['name','phone','email','address','city','balance','turnover','contact','comments','country','division','branch','department']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'balance':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'turnover':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'contact':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'country':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
             'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddSupplierForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)


class CommonCustomerAddForm(forms.ModelForm):
    class Meta:
        model = CommonCustomersModel
        fields = ['uid','name','phone','division','branch','department','email','address','city','sales','balance','country','comments',
                  'turnover','gender','contact','nextkin','relationship','age','paymentType','className','form']
        widgets={
            'uid':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
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

            'gender':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'paymentType':forms.Select(attrs={'class':'form-control','placeholder':''}),
           
            'form':forms.Select(attrs={'class':'form-control','placeholder':''}),
            
            'className':forms.Select(attrs={'class':'form-control','placeholder':''}),
             'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

            
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonCustomerAddForm, self).__init__(*args, **kwargs)
        #self.fields['owner'].queryset = User.objects.filter(first_name=allifformparam)
        self.fields['className'].queryset = CommonClassesModel.objects.filter(company=allifmaalparameter)
        self.fields['form'].queryset = CommonFormsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)


class CommonFormsAddForm(forms.ModelForm):
    class Meta:
        model =CommonFormsModel
        fields = ['name','comments','division','branch','department']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonFormsAddForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        

class CommonClassesAddForm(forms.ModelForm):
    class Meta:
        model =CommonClassesModel
        fields = ['name','form','size','owner','company','comments','division','department','branch','contact']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'contact':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'size':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'form':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'owner':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'company':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonClassesAddForm, self).__init__(*args, **kwargs)
        #self.fields['owner'].queryset = User.objects.filter(first_name=allifformparam)
        #self.fields['company'].queryset = CommonCompanyDetailsModel.objects.filter(owner=allifformparam)
        self.fields['form'].queryset = CommonFormsModel.objects.filter(company=allifmaalparameter,)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)



class CommonAddAssetCategoryForm(forms.ModelForm):
    class Meta:
        model = CommonAssetCategoriesModel
        fields = ['description','comments','division','branch','department']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddAssetCategoryForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
class CommonAssetsAddForm(forms.ModelForm):
    class Meta:
        model =CommonAssetsModel
        fields = ['supplier','division','branch','current_value','salvage_value','depreciated_by','depreciation','terms','asset_account','cost_account','description','quantity','value','lifespan',
                  'acquired','status','comments','category','department','employee','expires','deposit','asset_status']
        widgets={
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'quantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'value':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'deposit':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'lifespan':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'terms':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'asset_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'cost_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'acquired' : DatePickerInput(attrs={'class':'form-control'}),
            'expires' : DatePickerInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'employee':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           'asset_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'current_value':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'depreciated_by':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'salvage_value':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'depreciation':forms.Select(attrs={'class':'form-control','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAssetsAddForm, self).__init__(*args, **kwargs)
        self.fields['asset_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999).order_by('code')
        self.fields['cost_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999).order_by('code')
        self.fields['supplier'].queryset = CommonSuppliersModel.objects.filter(company=allifmaalparameter,)
        self.fields['category'].queryset = CommonAssetCategoriesModel.objects.filter(company=allifmaalparameter,)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter,)
        self.fields['employee'].queryset = CommonEmployeesModel.objects.filter(company=allifmaalparameter,)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
class CommonExpensesAddForm(forms.ModelForm):
    class Meta:
        model =CommonExpensesModel
        fields = ['supplier','division','branch','department','mode','equity_account','funding_account','expense_account','description','comments','amount','status','quantity']
        widgets={
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'quantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'mode':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'funding_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'expense_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control','placeholder':''}),
           'equity_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonExpensesAddForm, self).__init__(*args, **kwargs)
        self.fields['funding_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter)
        self.fields['expense_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter)
        self.fields['supplier'].queryset = CommonSuppliersModel.objects.filter(company=allifmaalparameter,)
        self.fields['equity_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
####################################3 STOCK ##############################33
class CommonStockCatAddForm(forms.ModelForm):
    class Meta:
        model =CommonStockCategoriesModel
        fields = ['description','division','branch','department','comments']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
             'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
        
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonStockCatAddForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)

class CommonStockItemAddForm(forms.ModelForm):
    class Meta:
        model =CommonStocksModel
        fields = ['category','comments','taxrate','criticalnumber','partNumber','division','branch','department','description','buyingPrice', 'quantity','unitcost','unitPrice','inventory_account','income_account','expense_account','standardUnitCost']
        widgets={
            'partNumber':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'unitcost':forms.TextInput(attrs={'class':'form-control'}),
            'unitPrice':forms.TextInput(attrs={'class':'form-control'}),
            'criticalnumber':forms.TextInput(attrs={'class':'form-control'}),
            'standardUnitCost':forms.TextInput(attrs={'class':'form-control'}),
            'buyingPrice':forms.TextInput(attrs={'class':'form-control'}),
            
            'inventory_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'taxrate':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'income_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'expense_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
          # the css class that we are passing
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonStockItemAddForm, self).__init__(*args, **kwargs)
        self.fields['inventory_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999)
        self.fields['expense_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999)
        self.fields['income_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=49999,code__gte=39999)
        self.fields['category'].queryset = CommonStockCategoriesModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['taxrate'].queryset = CommonTaxParametersModel.objects.filter(company=allifmaalparameter)
class CommonPOAddForm(forms.ModelForm):
    class Meta:
        model = CommonPurchaseOrdersModel
        fields = ['misccosts','uplift','grandtotal','taxamount','amount','description','division','branch','department', 'comments','supplier','payment_terms','posting_po_status']
        widgets={
            
            'uplift':forms.TextInput(attrs={'class':'form-control'}),
            'misccosts':forms.TextInput(attrs={'class':'form-control'}),
            'amount':forms.TextInput(attrs={'class':'form-control'}),
            'taxamount':forms.TextInput(attrs={'class':'form-control'}),
            'grandtotal':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'payment_terms':forms.Select(attrs={'class':'form-control'}),
            'posting_po_status':forms.Select(attrs={'class':'form-control'}),
            'store':forms.Select(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
       
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonPOAddForm, self).__init__(*args, **kwargs)
       
        self.fields['supplier'].queryset = CommonSuppliersModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)

class CommonPOItemAddForm(forms.ModelForm):
    class Meta:
        model =CommonPurchaseOrderItemsModel
        fields = ['items','quantity', 'unitcost','discount']
        widgets={
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'unitcost':forms.TextInput(attrs={'class':'form-control'}),
            'discount':forms.TextInput(attrs={'class':'form-control'}),
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'})
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonPOItemAddForm, self).__init__(*args, **kwargs)
        self.fields['items'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)
       

class CommonPOMiscCostAddForm(forms.ModelForm):
    class Meta:
        model = CommonPurchaseOrderMiscCostsModel
        fields = ['supplier','description','unitcost','quantity','po_misc_cost_con']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'amount':forms.TextInput(attrs={'class':'form-control'}),
            'unitcost':forms.TextInput(attrs={'class':'form-control'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'po_misc_cost_con':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonPOMiscCostAddForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].queryset = CommonSuppliersModel.objects.filter(company=allifmaalparameter)

##################### quotes ################
class CommonAddQuoteDetailsForm(forms.ModelForm):
    class Meta:
        model = CommonQuotesModel
        fields = ['customer','description','terms','division','branch','department','prospect','currency','comments','discount','tax','discountValue','salestax']

        widgets={
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'tax':forms.TextInput(attrs={'class':'form-control'}),
            'discountValue':forms.TextInput(attrs={'class':'form-control'}),
            'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'terms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'prospect':forms.Select(attrs={'class':'form-control'}),
            'currency':forms.Select(attrs={'class':'form-control'}),
            'discount':forms.Select(attrs={'class':'form-control'}),
            'salestax':forms.Select(attrs={'class':'form-control'}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddQuoteDetailsForm, self).__init__(*args, **kwargs)
       
        self.fields['customer'].queryset = CommonCustomersModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)

class CommonAddQuoteItemsForm(forms.ModelForm):
    class Meta:
        model = CommonQuoteItemsModel
        fields = ['description','quantity','discount' ]
        widgets={
            'description':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'discount':forms.TextInput(attrs={'class':'form-control'}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddQuoteItemsForm, self).__init__(*args, **kwargs)
        self.fields['description'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)


class CommonAddInvoiceDetailsForm(forms.ModelForm):
    class Meta:
        model =CommonInvoicesModel
        fields = ['customer','description','terms','division','branch','department','status','currency','comments','discount','tax','discountValue','salestax']

        widgets={
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'tax':forms.TextInput(attrs={'class':'form-control'}),
            'discountValue':forms.TextInput(attrs={'class':'form-control'}),
            'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'terms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'currency':forms.Select(attrs={'class':'form-control'}),
            'discount':forms.Select(attrs={'class':'form-control'}),
            'salestax':forms.Select(attrs={'class':'form-control'}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddInvoiceDetailsForm, self).__init__(*args, **kwargs)
       
        self.fields['customer'].queryset = CommonCustomersModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)

class CommonAddInvoiceItemsForm(forms.ModelForm):
    class Meta:
        model = CommonInvoiceItemsModel
        fields = ['description','quantity','discount']

        widgets={
            'description':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'discount':forms.TextInput(attrs={'class':'form-control'}),
           
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddInvoiceItemsForm, self).__init__(*args, **kwargs)
        self.fields['description'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)


class CommonAddSupplierPaymentForm(forms.ModelForm):
    class Meta:
        model = CommonSupplierPaymentsModel
        fields = ['supplier','amount','description','comments','account','mode','status','division','branch','department']
        widgets={
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'mode':forms.Select(attrs={'class':'form-control','placeholder':''}),

            'account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control','placeholder':''}),

            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter,dept, *args, **kwargs):
        super(CommonAddSupplierPaymentForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].queryset =CommonSuppliersModel.objects.filter(company=allifmaalparameter,department=dept)
        self.fields['account'].queryset =CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=29999,department=dept).order_by('code')
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
class CommonAddCustomerPaymentForm(forms.ModelForm):
    class Meta:
        model = CommonCustomerPaymentsModel
        fields = ['customer','amount','comments','account','mode','status','division','branch','department']
        widgets={
            'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'mode':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddCustomerPaymentForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset =CommonCustomersModel.objects.filter(company=allifmaalparameter)
        self.fields['account'].queryset =CommonChartofAccountsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)

class CommonAddSalaryForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = CommonSalariesModel
        fields = ["staff",'description','amount','division','branch','department','account','comments','mode','status','salary_payable']
        widgets={
            'staff':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'salary_payable':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'mode':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           

            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddSalaryForm, self).__init__(*args, **kwargs)
        self.fields['staff'].queryset =CommonEmployeesModel.objects.filter(company=allifmaalparameter)
        self.fields['account'].queryset =CommonChartofAccountsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)


class CommonAddJobDetailsForm(forms.ModelForm):
    class Meta:
        model =CommonJobsModel
        fields = ['customer','description','ending_date','status','comments','division','department','branch']

        widgets={
            'description':forms.TextInput(attrs={'class':'form-control'}),
            
            'comments':forms.TextInput(attrs={'class':'form-control'}),
           
            'customer':forms.Select(attrs={'class':'form-control'}),
           
            'status':forms.Select(attrs={'class':'form-control'}),
            
            #'ending_date':forms.DateInput(attrs={'class':'form-control'}),
            'ending_date' : DatePickerInput(attrs={'class':'form-control'}),
             'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddJobDetailsForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset =CommonCustomersModel.objects.filter(company=allifmaalparameter)
       
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)

class CommonAddJobItemsForm(forms.ModelForm):
    class Meta:
        model =CommonJobItemsModel
        fields = ['description', 'quantity','comments','item']

        widgets={
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'item':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddJobItemsForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset =CommonStocksModel.objects.filter(company=allifmaalparameter)
       
class CommonAddTasksForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = CommonTasksModel
        fields = ['task','status','dueDate','taskDay','description','assignedto','division','department','branch']
        widgets={
            
            'task':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
            'dueDate':DatePickerInput(attrs={'class':'form-control','placeholder':'Task due date'}),
            'taskDay':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            
            'assignedto':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            #form-control here is the css class that we are passing
        } 
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddTasksForm, self).__init__(*args, **kwargs)
        
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['assignedto'].queryset = CommonEmployeesModel.objects.filter(company=allifmaalparameter,)
     
##########################3 testing links ####################
class TemplateLinkForm(forms.ModelForm):
    class Meta:
        model = TemplateLink
        fields = ['name', 'url_name', 'url_params']