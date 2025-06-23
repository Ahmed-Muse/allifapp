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

class AddExamDetailsForm(forms.ModelForm):
    class Meta:
        model =ExaminationsModel
        fields = ['subject','comments','description','exam_file','exam_date','division','branch','department']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'subject':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'exam_file':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(AddExamDetailsForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['subject'].queryset = CommonStocksModel.objects.filter(company=allifmaalparameter)
        self.fields['exam_file'].queryset = CommonTransactionsModel.objects.filter(company=allifmaalparameter)
        

class AddExamResultsForm(forms.ModelForm):
    class Meta:
        model =ExamResultsModel
        fields = ['subject','comments','result','grade','description','exam_file','result_date','division','branch','department']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'comments':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'result':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'grade':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'subject':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'exam_file':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'division':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'branch':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'department':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
        }
    def __init__(self, allifmaalparameter, *args, **kwargs):
        super(AddExamResultsForm, self).__init__(*args, **kwargs)
        self.fields['division'].queryset = CommonDivisionsModel.objects.filter(company=allifmaalparameter)
        self.fields['branch'].queryset = CommonBranchesModel.objects.filter(company=allifmaalparameter)
        self.fields['department'].queryset = CommonDepartmentsModel.objects.filter(company=allifmaalparameter)
        self.fields['subject'].queryset = ExaminationsModel.objects.filter(company=allifmaalparameter)
        self.fields['exam_file'].queryset = CommonTransactionsModel.objects.filter(company=allifmaalparameter)
        

