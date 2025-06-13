from django import forms
from .models import *
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
        fields = ['name','form','size','owner','comments','division','department','branch','contact']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'contact':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'size':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'form':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'owner':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            
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

