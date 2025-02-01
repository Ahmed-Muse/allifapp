from django import forms
from django.contrib.auth.forms import UserCreationForm#this django form fields tha django creates automatically for us
from .models import AllifmaalUsersModel,AllifmaalUsersLoginModel

class AllifmaalCreateUserForm(UserCreationForm):
  
    class Meta:
        model=AllifmaalUsersModel
        fields=['username','first_name','last_name','email','password1','password2','allifmaalcategory']#all these fields are from django
        widgets={
            
            'allifmaalcategory':forms.Select(attrs={'class':'form-control','placeholder':''}),
            
            }
        
class AllifmaalUserLoginForm(forms.ModelForm): #this is used for user login
    class Meta:
        model =AllifmaalUsersLoginModel
        fields = ["username",'password']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
             'password':forms.TextInput(attrs={'class':'form-control','placeholder':'','type':'password'}),
        }

class AllifmaalUpdateCustomUserForm(forms.ModelForm):#this updates the user details...
    first_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    allifmaalcategory=forms.Select()
    class Meta:
        model = AllifmaalUsersModel
        fields = ['first_name', 'email','last_name','allifmaalcategory']
        widgets={
             'allifmaalcategory':forms.Select(attrs={'class':'form-control'}),
        }