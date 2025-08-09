from django import forms
from django.contrib.auth.forms import UserCreationForm
from allifmaalusersapp.models import User,UserLoginDetailsModel
from allifmaalcommonapp.models import CommonOperationYearsModel,CommonOperationYearTermsModel,CommonCompanyDetailsModel,CommonDivisionsModel,CommonBranchesModel,CommonDepartmentsModel
class CreateNewCustomUserForm(UserCreationForm):#this is used for new user creation
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )
    
    class Meta:
        model=User
        fields=['username','division','branch','department','peformance_counter','fullNames','phone','first_name','last_name','email','password1','password2','user_category']#all these fields are from django
        widgets={
            
            'user_category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'password1':forms.PasswordInput(attrs={'class':'form-control','placeholder':''}),
            'password2':forms.PasswordInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':''}),  
            'peformance_counter':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
             'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
       
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
       
        }
    def __init__(self, *args, **kwargs):
        # Pop your custom argument before calling super()
        allifmaalparameter = kwargs.pop('allifmaalparameter', None)
        super().__init__(*args, **kwargs)

        # Your custom logic now goes here, after the parent form is initialized.
        if allifmaalparameter:
            # Assuming you want to filter companies by the owner of the current user's company
           
            self.fields['division'].queryset = CommonDivisionsModel.all_objects.none()
            self.fields['branch'].queryset = CommonBranchesModel.all_objects.filter(company=allifmaalparameter)
            self.fields['department'].queryset = CommonDepartmentsModel.all_objects.filter(company=allifmaalparameter)
            
            # below is for admin only if you want to change the organization of the user...
            #self.fields['company'].queryset = CommonCompanyDetailsModel.all_objects.all()


class CustomUserLoginForm(forms.ModelForm): #this is used for user login
    class Meta:
        model =UserLoginDetailsModel
        fields = ["username",'password']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
             'password':forms.TextInput(attrs={'class':'form-control','placeholder':'','type':'password'}),
        }
        

class UpdateCustomUserForm(forms.ModelForm):#this updates the user details...
    first_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    user_category=forms.Select()
    class Meta:
        model = User
        fields = ['first_name','username','division','branch','department','peformance_counter', 'company','email','last_name','user_category','operation_year','operation_term']
        widgets={
            'user_category':forms.Select(attrs={'class':'form-control'}),
          
            'user_category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'peformance_counter':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':''}), 
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           'company':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
       
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
       
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
       
            'operation_year':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'operation_term':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
        }
     # Pass custom arguments as keyword arguments and handle them separately.
    def __init__(self, *args, **kwargs):
        # Pop your custom argument before calling super()
        allifmaalparameter = kwargs.pop('allifmaalparameter', None)
        super().__init__(*args, **kwargs)

        # Your custom logic now goes here, after the parent form is initialized.
        if allifmaalparameter:
            # Assuming you want to filter companies by the owner of the current user's company
            self.fields['company'].queryset = CommonCompanyDetailsModel.all_objects.filter(owner=allifmaalparameter.owner)
            self.fields['division'].queryset = CommonDivisionsModel.all_objects.filter(company=allifmaalparameter)
            self.fields['branch'].queryset = CommonBranchesModel.all_objects.filter(company=allifmaalparameter)
            self.fields['department'].queryset = CommonDepartmentsModel.all_objects.filter(company=allifmaalparameter)
            
            self.fields['operation_year'].queryset = CommonOperationYearsModel.all_objects.filter(company=allifmaalparameter)
            self.fields['operation_term'].queryset = CommonOperationYearTermsModel.all_objects.filter(company=allifmaalparameter)
            
            # below is for admin only if you want to change the organization of the user...
            #self.fields['company'].queryset = CommonCompanyDetailsModel.all_objects.all()
