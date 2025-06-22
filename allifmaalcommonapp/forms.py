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
        fields = ['company','can_delete','legalName','sector','owner','phone1','email','website', 'logo','address','phone2','pobox','city','country']
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
            'can_delete':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'pobox':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'phone2':forms.TextInput(attrs={'class':'form-control'}),
            'website':forms.TextInput(attrs={'class':'form-control'}),
            'logo':forms.FileInput(attrs={'class':'form-control'}),
             #'passwrd':forms.TextInput(attrs={'class':'form-control','type':'password'}),
        
        }

class CommonAddCompanyScopeForm(forms.ModelForm):
    class Meta:
        model = CommonCompanyScopeModel
        fields = ['name','comments','division','branch','department']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        } 
    def __init__(self,allifmaalparameter,*args,**kwargs):
        super (CommonAddCompanyScopeForm,self).__init__(*args,**kwargs) # populates the post
        self.fields['department'].queryset=CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset =CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset=CommonBranchesModel.objects.filter(company=allifmaalparameter)

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
            'gender':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'username':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'sysperms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

            
        }
    def __init__(self,allifmaalparameter,*args,**kwargs):
        super (CommonAddStaffProfileForm,self).__init__(*args,**kwargs) # populates the post
        self.fields['username'].queryset =User.objects.filter(usercompany=allifmaalparameter.companyslug)
        self.fields['department'].queryset=CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset =CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset=CommonBranchesModel.objects.filter(company=allifmaalparameter)

#################### taxes #####################3
class CommonAddTaxParameterForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model = CommonTaxParametersModel
        fields = ['taxname','taxtype','taxrate', 'taxdescription','division','branch','department']
        widgets={
            'taxname':forms.TextInput(attrs={'class':'form-control'}),
             #'taxname':forms.TextInput(attrs={'class':'form-control','value':mydefault}),
            'taxrate':forms.TextInput(attrs={'class':'form-control'}),
             'taxtype':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
             'taxdescription':forms.TextInput(attrs={'class':'form-control'}),
              'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddTaxParameterForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter or 1)


#################### taxes #####################3
class CommonSupplierAddTaxParameterForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model = CommonSupplierTaxParametersModel
        fields = ['taxname','taxtype','taxrate', 'taxdescription','division','branch','department']
        widgets={
            'taxname':forms.TextInput(attrs={'class':'form-control'}),
             #'taxname':forms.TextInput(attrs={'class':'form-control','value':mydefault}),
            'taxrate':forms.TextInput(attrs={'class':'form-control'}),
             'taxtype':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
             'taxdescription':forms.TextInput(attrs={'class':'form-control'}),
              'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonSupplierAddTaxParameterForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter or 1)


#######3


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
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':'Chart of A/Cs'}),
            'statement':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
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
        fields = ['department','comments','branch','division','phone','email','address','city','pobox']
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
       
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
       
class CommonAddSupplierForm(forms.ModelForm):
    class Meta:
        model = CommonSuppliersModel
        fields = ['name','phone','email','address','city','balance','turnover','contact','comments','country','division','branch','department']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':''}),
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
        fields = ['uid','seen','register','triaged','name','phone','division','branch','department','email','address','city','sales','balance','country','comments',
                  'turnover','gender','contact','nextkin','relationship','age','paymentType']
        widgets={
            'uid':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
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

            'gender':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'paymentType':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            #'form':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            #'className':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
             'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

            
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonCustomerAddForm, self).__init__(*args, **kwargs)
        #self.fields['owner'].queryset = User.objects.filter(first_name=allifformparam)
        #self.fields['className'].queryset = CommonClassesModel.objects.filter(company=allifmaalparameter)
       #self.fields['form'].queryset = CommonFormsModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)


class CommonAddCurrencyForm(forms.ModelForm):
    class Meta:
        model=CommonCurrenciesModel
        fields = ['description','comments','division','branch','department']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddCurrencyForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)


class CommonAddPaymentTermForm(forms.ModelForm):
    class Meta:
        model=CommonPaymentTermsModel
        fields = ['description','comments','division','branch','department']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddPaymentTermForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)


class CommonAddUnitForm(forms.ModelForm):
    class Meta:
        model=CommonUnitsModel
        fields = ['description','comments','division','branch','department']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddUnitForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)


class CommonAddOperationYearForm(forms.ModelForm):
    class Meta:
        model=CommonOperationYearsModel
        fields = ['year','comments','start_date','end_date','department','is_current','branch','division']
        widgets={
            'year':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'end_date':DatePickerInput(attrs={'class':'form-control'}),
            'start_date':DatePickerInput(attrs={'class':'form-control'}),
            'is_current':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddOperationYearForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)


class CommonAddOperationYearTermForm(forms.ModelForm):
    class Meta:
        model=CommonOperationYearTermsModel
        fields = ['operation_year','name','is_active','comments','start_date','end_date','department','is_current','branch','division']
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
                  'acquired','status','comments','category','department','employee_in_charge','expires','deposit','asset_status']
        widgets={
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'quantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'value':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'deposit':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'lifespan':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'terms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'asset_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'cost_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'acquired' : DatePickerInput(attrs={'class':'form-control'}),
            'expires' : DatePickerInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),

            'category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'employee_in_charge':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           'asset_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'current_value':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'depreciated_by':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'salvage_value':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'depreciation':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAssetsAddForm, self).__init__(*args, **kwargs)
        self.fields['asset_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999).order_by('code')
        self.fields['cost_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999).order_by('code')
        self.fields['supplier'].queryset = CommonSuppliersModel.objects.filter(company=allifmaalparameter,)
        self.fields['category'].queryset = CommonCategoriesModel.objects.filter(company=allifmaalparameter,)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter,)
        self.fields['employee_in_charge'].queryset = CommonEmployeesModel.objects.filter(company=allifmaalparameter,)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
class CommonExpensesAddForm(forms.ModelForm):
    class Meta:
        model =CommonExpensesModel
        fields = ['supplier','division','branch','department','mode','expense_account','description','comments','amount','status']
        widgets={
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'mode':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'expense_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
           'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonExpensesAddForm, self).__init__(*args, **kwargs)
        
        self.fields['expense_account'].queryset = CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=59999,code__gte=49999)
        self.fields['supplier'].queryset = CommonSuppliersModel.objects.filter(company=allifmaalparameter,)
        
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)


class CommonAddSpaceItemForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model =CommonSpaceItemsModel
        fields = ['items','quantity']
        widgets={
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
             #'taxname':forms.TextInput(attrs={'class':'form-control','value':mydefault}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
           
             
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddSpaceItemForm, self).__init__(*args, **kwargs)
        self.fields['items'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)


class CommonAddSpaceBookingItemForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model =CommonSpaceBookingItemsModel
        fields = ['space','space_unit','quantity']
        widgets={
            'space':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'space_unit':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
             
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddSpaceBookingItemForm, self).__init__(*args, **kwargs)
        self.fields['space'].queryset = CommonSpacesModel.objects.filter(company=allifmaalparameter)
        self.fields['space_unit'].queryset = CommonSpaceUnitsModel.objects.filter(company=allifmaalparameter)
       


class CommonAddTransferOrderDetailsForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model = CommonStockTransferOrdersModel
        fields = ['from_store','to_store','status','comments','division','branch','department']
        widgets={
            'from_store':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
             #'taxname':forms.TextInput(attrs={'class':'form-control','value':mydefault}),
            'to_store':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
             'comments':forms.TextInput(attrs={'class':'form-control'}),
             'status':forms.Select(attrs={'class':'form-control'}),
              'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddTransferOrderDetailsForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['from_store'].queryset =CommonSpacesModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['to_store'].queryset = CommonSpacesModel.objects.filter(company=allifmaalparameter or 1)

class CommonAddTransferOrderItemForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model = CommonStockTransferOrderItemsModel
        fields = ['items','quantity','comments','trans_ord_items_con']
        widgets={
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
             #'taxname':forms.TextInput(attrs={'class':'form-control','value':mydefault}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
             'comments':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
             
             
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddTransferOrderItemForm, self).__init__(*args, **kwargs)
        #self.fields['trans_ord_items_con'].queryset = CommonWarehouseItemsModel.objects.filter(item__warehouse=allifmaalparameter)
        #self.fields['items'].queryset = CommonWarehouseItemsModel.objects.filter(items__items=allifmaalparameter)
       
        self.fields['items'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)
       
       

class CommonAddApproverForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model = CommonApproversModel
        fields = ['approvers','comments','division','branch','department']
        widgets={
            'approvers':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
             #'taxname':forms.TextInput(attrs={'class':'form-control','value':mydefault}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
          
              'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddApproverForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['approvers'].queryset=CommonEmployeesModel.objects.filter(company=allifmaalparameter or 1)


class CommonAddCodeForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model = CommonCodesModel
        fields = ['code','name','description','division','branch','department']
        widgets={
          
             #'taxname':forms.TextInput(attrs={'class':'form-control','value':mydefault}),
            'code':forms.TextInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
          
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddCodeForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter or 1)
       

class CommonAddCreditNoteDetailsForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model = CommonCreditNotesModel
        fields = ['customer','return_location','approval_status','original_invoice','reasons','total_amount', 'status','division','branch','department']
        widgets={
            'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'original_invoice':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'total_amount':forms.TextInput(attrs={'class':'form-control'}),
             #'taxname':forms.TextInput(attrs={'class':'form-control','value':mydefault}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'reasons':forms.TextInput(attrs={'class':'form-control'}),
             'approval_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
             'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'return_location':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddCreditNoteDetailsForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['original_invoice'].queryset = CommonInvoicesModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['customer'].queryset = CommonCustomersModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['return_location'].queryset = CommonSpacesModel.objects.filter(company=allifmaalparameter or 1)

class CommonAddCreditNoteItemForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model = CommonCreditNoteItemsModel
        fields = ['items','quantity']
        widgets={
           'quantity':forms.TextInput(attrs={'class':'form-control'}),
           
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddCreditNoteItemForm, self).__init__(*args, **kwargs)
        
        self.fields['items'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)
       
####################################3 CATEGORIES ##############################33
class CommonCategoryAddForm(forms.ModelForm):
    class Meta:
        model=CommonCategoriesModel
        fields = ['description','start_date','end_date','is_current','operation_year','operation_term','name','code','division','branch','department','comments']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'code':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'end_date':DatePickerInput(attrs={'class':'form-control'}),
            'start_date':DatePickerInput(attrs={'class':'form-control'}),
            'operation_term':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'is_current':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'operation_year':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
           
        
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonCategoryAddForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        
        self.fields['operation_year'].queryset =CommonOperationYearsModel.objects.filter(company=allifmaalparameter)
        self.fields['operation_term'].queryset =CommonOperationYearTermsModel.objects.filter(company=allifmaalparameter)

class CommonStockItemAddForm(forms.ModelForm):
    class Meta:
        model =CommonStocksModel
        fields = ['category','total_units_sold','weight','expires','item_state','normal_range',
                  'length','height','width','units',
                  'warehouse','suppliertaxrate',
                  'comments','taxrate','criticalnumber','partNumber','division','branch','department','description','buyingPrice', 'quantity','unitcost','unitPrice','inventory_account','income_account','expense_account','standardUnitCost']
        widgets={
            'partNumber':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'normal_range':forms.TextInput(attrs={'class':'form-control'}),
            
            'weight':forms.TextInput(attrs={'class':'form-control'}),
            'height':forms.TextInput(attrs={'class':'form-control'}),
            'length':forms.TextInput(attrs={'class':'form-control'}),
            'width':forms.TextInput(attrs={'class':'form-control'}),
            'expires' : DatePickerInput(attrs={'class':'form-control'}),
            
            'comments':forms.TextInput(attrs={'class':'form-control'}),
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
        self.fields['category'].queryset = CommonCategoriesModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['warehouse'].queryset=CommonSpacesModel.objects.filter(company=allifmaalparameter)
        self.fields['suppliertaxrate'].queryset=CommonSupplierTaxParametersModel.objects.filter(company=allifmaalparameter)
        self.fields['taxrate'].queryset=CommonTaxParametersModel.objects.filter(company=allifmaalparameter)
class CommonPOAddForm(forms.ModelForm):
    class Meta:
        model = CommonPurchaseOrdersModel
        fields = ['misccosts','approval_status','uplift','taxrate','currency','delivery','grandtotal','taxamount','amount','description','division','branch','department', 'comments','supplier','payment_terms','posting_po_status']
        widgets={
            
            'uplift':forms.TextInput(attrs={'class':'form-control'}),
            'misccosts':forms.TextInput(attrs={'class':'form-control'}),
            'amount':forms.TextInput(attrs={'class':'form-control'}),
            'taxamount':forms.TextInput(attrs={'class':'form-control'}),
            'grandtotal':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'taxrate':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'payment_terms':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'posting_po_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'store':forms.Select(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'currency':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'delivery':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'approval_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
       
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonPOAddForm, self).__init__(*args, **kwargs)
       
        self.fields['supplier'].queryset = CommonSuppliersModel.objects.filter(company=allifmaalparameter)
        self.fields['taxrate'].queryset = CommonSupplierTaxParametersModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['currency'].queryset = CommonCurrenciesModel.objects.filter(company=allifmaalparameter)
        self.fields['payment_terms'].queryset = CommonPaymentTermsModel.objects.filter(company=allifmaalparameter)
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

####################################### SPACES ################

class CommonAddSpaceForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model = CommonSpacesModel
        fields = ['asset','contact_phone','space_number','emplyee_in_charge','number_of_units',
                  'capacity','city','address','amenities',
                  'max_occupancy','monthly_rent','base_price_per_night',
                  'current_status','name','space_floor','space_type','description',
                  'division','branch','department','number_of_bedrooms','number_of_bathrooms']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'number_of_units':forms.TextInput(attrs={'class':'form-control'}),
            'number_of_bedrooms':forms.TextInput(attrs={'class':'form-control'}),
            'number_of_bathrooms':forms.TextInput(attrs={'class':'form-control'}),
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
            #'inventory_account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'emplyee_in_charge':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddSpaceForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['asset'].queryset=CommonAssetsModel.objects.filter(company=allifmaalparameter)

    
class CommonAddSpaceUnitForm(forms.ModelForm):
    class Meta:
        #mydefault=TaxParametersModel.objects.all().first().taxname
        model = CommonSpaceUnitsModel
        fields = ['space','space_number','unitcost','unitprice','area_sqm','rooms','washrooms',
                  'unit_type',
                  'emplyee_in_charge','capacity','amenities','max_occupancy','monthly_rent',
                  'base_price_per_night','current_status','name','space_floor','space_type',
                  'description','division','branch','department']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
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
            
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddSpaceUnitForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter or 1)
        self.fields['space'].queryset=CommonSpacesModel.objects.filter(company=allifmaalparameter)

##################### quotes ################
class CommonAddQuoteDetailsForm(forms.ModelForm):
    class Meta:
        model = CommonQuotesModel
        fields = ['customer','description','delivery','payment_terms','currency','division','branch','department','prospect','currency','comments','discount','tax','discountValue','salestax']

        widgets={
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
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
        self.fields['salestax'].queryset = CommonTaxParametersModel.objects.filter(company=allifmaalparameter)
        self.fields['currency'].queryset = CommonCurrenciesModel.objects.filter(company=allifmaalparameter)
        self.fields['payment_terms'].queryset = CommonPaymentTermsModel.objects.filter(company=allifmaalparameter)
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
        fields = ['customer','posting_inv_status','invoice_status','description','delivery','payment_terms','division','branch','department','status','currency','comments','discount','tax','discountValue','salestax']

        widgets={
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
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
        self.fields['salestax'].queryset = CommonTaxParametersModel.objects.filter(company=allifmaalparameter)
        self.fields['currency'].queryset = CommonCurrenciesModel.objects.filter(company=allifmaalparameter)
        self.fields['payment_terms'].queryset = CommonPaymentTermsModel.objects.filter(company=allifmaalparameter)
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
            'mode':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

            'account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),

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
        fields = ['customer','amount','comments','description','account','mode','status','division','branch','department']
        widgets={
            'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'amount':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'mode':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'account':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddCustomerPaymentForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset =CommonCustomersModel.objects.filter(company=allifmaalparameter)
        self.fields['account'].queryset =CommonChartofAccountsModel.objects.filter(company=allifmaalparameter,code__lte=19999)
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

    
####################################3 Transactions ##############################33
class CommonAddTransactionDetailsForm(forms.ModelForm):
    class Meta:
        model=CommonTransactionsModel
        fields = ['description','customer','payment_mode','employee_in_charge','start_date','end_date',
                  'operation_year','operation_term',
                  'name','code','division','branch','department','comments']
        widgets={
           
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'employee_in_charge':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'code':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'payment_mode':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'end_date':DatePickerInput(attrs={'class':'form-control'}),
            'end_date_time':DatePickerInput(attrs={'class':'form-control'}),
            'start_date':DatePickerInput(attrs={'class':'form-control'}),
            'operation_term':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            'operation_year':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
           
        
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddTransactionDetailsForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['payment_mode'].queryset = CommonPaymentTermsModel.objects.filter(company=allifmaalparameter)
        
        self.fields['operation_year'].queryset =CommonOperationYearsModel.objects.filter(company=allifmaalparameter)
        self.fields['operation_term'].queryset =CommonOperationYearTermsModel.objects.filter(company=allifmaalparameter)

####################################3 Transactions ##############################33
class CommonAddTransactionItemForm(forms.ModelForm):
    class Meta:
        model=CommonTransactionItemsModel
        fields = ['trans_number','items','quantity','comments','date','description','division','branch','department']
        widgets={
            'trans_number':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'quantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'date':DatePickerInput(attrs={'class':'form-control'}),
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
        
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddTransactionItemForm, self).__init__(*args, **kwargs)
        self.fields['items'].queryset =CommonStocksModel.objects.filter(company=allifmaalparameter)
        self.fields['trans_number'].queryset=CommonTransactionsModel.objects.filter(company=allifmaalparameter)
       
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
           
            'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
           
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            
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
        fields = ['quantity','item']

        widgets={
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
           
           
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
            'taskDay':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            
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
 
 ############################### shipments... ##################3
 
####################################3 Transactions ##############################33
class CommonAddTransitDetailsForm(forms.ModelForm):
    class Meta:
        model=CommonTransitModel
        fields = ['carrier','shipment_number','received_on','description','status','expected','origin','via',
                  'dispatched_by','customer','received_by',
                  'destination','delivery_confirmed_by_employee','delivery_confirmation_date_time',
                  'exit_warehouse','supplier','delivery_confirmed_by_customer','delivery_notes',
                  'entry_warehouse','division','branch','department','comments',]
        widgets={
            'delivery_notes':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'delivery_confirmed_by_employee':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'delivery_confirmed_by_customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'dispatched_by':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'received_by':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
            'carrier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'shipment_number':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'origin':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'entry_warehouse':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'exit_warehouse':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'supplier':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'via':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'main_complaints':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'employee_in_charge':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'destination':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'customer':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'expected':DatePickerInput(attrs={'class':'form-control'}),
            
            'received_on':DatePickerInput(attrs={'class':'form-control'}),
            'delivery_confirmation_date_time':DatePickerInput(attrs={'class':'form-control'}),
         
        }
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddTransitDetailsForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        
        self.fields['exit_warehouse'].queryset =CommonSpacesModel.objects.filter(company=allifmaalparameter)
        self.fields['entry_warehouse'].queryset =CommonSpacesModel.objects.filter(company=allifmaalparameter)
        self.fields['supplier'].queryset =CommonSuppliersModel.objects.filter(company=allifmaalparameter)

   
class CommonAddTransitItemsForm(forms.ModelForm):
    class Meta:
        model=CommonTransitItemsModel
        fields = ['quantity','items','unit_of_measure','expected','dispatched_by','expires','delivered_on',
                  'consigner','consignee','details','weight','length','width','height','received','value','rate',
                  'status','destination','origin','comments','department','branch','division',
                  ]

        widgets={
            'details':forms.TextInput(attrs={'class':'form-control'}),
            'origin':forms.TextInput(attrs={'class':'form-control'}),
            'weight':forms.TextInput(attrs={'class':'form-control'}),
            'length':forms.TextInput(attrs={'class':'form-control'}),
            'width':forms.TextInput(attrs={'class':'form-control'}),
            'height':forms.TextInput(attrs={'class':'form-control'}),
            'value':forms.TextInput(attrs={'class':'form-control'}),
            'rate':forms.TextInput(attrs={'class':'form-control'}),
            'destination':forms.TextInput(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
            'received':DatePickerInput(attrs={'class':'form-control'}),
            'expires':DatePickerInput(attrs={'class':'form-control'}),
            'expected':DatePickerInput(attrs={'class':'form-control'}),
            'delivered_on':DatePickerInput(attrs={'class':'form-control'}),
            'consigner':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'consignee':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'dispatched_by':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           'unit_of_measure':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'items':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddTransitItemsForm, self).__init__(*args, **kwargs)
        self.fields['items'].queryset =CommonStocksModel.objects.filter(company=allifmaalparameter)
        self.fields['unit_of_measure'].queryset =CommonUnitsModel.objects.filter(company=allifmaalparameter)
        self.fields['consigner'].queryset =CommonCustomersModel.objects.filter(company=allifmaalparameter)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        
        self.fields['consignee'].queryset =CommonCustomersModel.objects.filter(company=allifmaalparameter)
 

################################### PROGRESS REPORTING/RECORDINGS ################

 
 
class CommonAddProgressForm(forms.ModelForm):
    class Meta:
        model =CommonProgressModel
        fields = ['description','recorded_on','division','branch','department']

        widgets={
           
            'recorded_on':DatePickerInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
           
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(CommonAddProgressForm, self).__init__(*args, **kwargs)
      
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        
 
 
 
 
 
 
 
 
 
 
 ###############3 you might delete below is not used so far... ##########3
 
class CommonAddProgramForm(forms.ModelForm):
    class Meta:
        model=CommonProgramsModel
        fields = ['name','start_date','operation_year','operation_term','end_date','code','description',
                  'department','is_current','branch','division']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'code':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'end_date':DatePickerInput(attrs={'class':'form-control'}),
            'start_date':DatePickerInput(attrs={'class':'form-control'}),
            'operation_term':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'is_current':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'operation_year':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
             # --- Add is_active here ---
         
        
        }
        
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddProgramForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['operation_year'].queryset =CommonOperationYearsModel.objects.filter(company=allifmaalparameter)
        self.fields['operation_term'].queryset =CommonOperationYearTermsModel.objects.filter(company=allifmaalparameter)


class CommonAddServiceForm(forms.ModelForm):
    class Meta:
        model=CommonServicesModel
        fields = ['description','name','start_date','operation_year','unitprice','unitcost','quantity',
                  'operation_term','comments','end_date','code','normal_range_info','unit_of_measure',
                  'program','credits','department','is_current','branch','division']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'credits':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'code':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'unitprice':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'unitcost':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'quantity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'normal_range_info':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'end_date':DatePickerInput(attrs={'class':'form-control'}),
            'program':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'unit_of_measure':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'start_date':DatePickerInput(attrs={'class':'form-control'}),
            'operation_term':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'is_current':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'operation_year':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
           
        
        }
        
    def __init__(self,allifmaalparameter, *args, **kwargs):
        super(CommonAddServiceForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['operation_year'].queryset =CommonOperationYearsModel.objects.filter(company=allifmaalparameter)
        self.fields['operation_term'].queryset =CommonOperationYearTermsModel.objects.filter(company=allifmaalparameter)

        self.fields['unit_of_measure'].queryset =CommonUnitsModel.objects.filter(company=allifmaalparameter)
        self.fields['program'].queryset =CommonProgramsModel.objects.filter(company=allifmaalparameter)
    