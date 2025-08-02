from django import forms
from django.contrib.auth.forms import UserCreationForm
from allifmaalusersapp.models import User,UserLoginDetailsModel
from allifmaalcommonapp.models import CommonCompanyDetailsModel
class CreateNewCustomUserForm(UserCreationForm):#this is used for new user creation
    class Meta:
        model=User
        fields=['username','peformance_counter','fullNames','phone','first_name','last_name','email','password1','password2','user_category','usercompany',]#all these fields are from django
        widgets={
            'usercompany':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
           
            'user_category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'password1':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'password2':forms.PasswordInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':''}),  
            'peformance_counter':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        }
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
        fields = ['first_name','peformance_counter', 'company','email','last_name','user_category','usercompany',]
        widgets={
            'user_category':forms.Select(attrs={'class':'form-control'}),
            'usercompany':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
          
            'user_category':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'peformance_counter':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':''}), 
            'company':forms.Select(attrs={'class':'form-control'}), 
          
           
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
            
            # below is for admin only if you want to change the organization of the user...
            #self.fields['company'].queryset = CommonCompanyDetailsModel.all_objects.all()
