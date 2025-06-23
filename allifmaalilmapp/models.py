from django.db import models
from allifmaalcommonapp.models import *



# for educational institutions
class ExaminationsModel(models.Model):
    subject=models.ForeignKey(CommonStocksModel,related_name="subject_education_exams",on_delete=models.SET_NULL,null=True,blank=True)
    exam_file=models.ForeignKey(CommonTransactionsModel,related_name="division_education_exams",on_delete=models.SET_NULL,null=True,blank=True)
    description=models.CharField(max_length=50,blank=True,null=True)
    comments=models.CharField(max_length=30,blank=True,null=True, default='comment')
    date=models.DateField(auto_now=True)
    exam_date=models.DateTimeField(blank=True,null=True)
    owner=models.ForeignKey(User, related_name="owner_exams",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="company_exams",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="division_exams",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="branch_exams",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="dept_exams",on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.subject

class ExamResultsModel(models.Model):
    subject=models.ForeignKey(ExaminationsModel,on_delete=models.SET_NULL,blank=True,null=True)
    exam_file=models.ForeignKey(CommonTransactionsModel,related_name="exam_file_education_exams_results",on_delete=models.SET_NULL,null=True,blank=True)
    description=models.CharField(max_length=50,blank=True,null=True)
    comments=models.CharField(max_length=30,blank=True,null=True, default='comment')
    result=models.CharField(max_length=50,blank=True,null=True)
    grade=models.CharField(max_length=50,blank=True,null=True)
    date=models.DateField(auto_now=True)
    result_date=models.DateTimeField(blank=True,null=True)
    
    owner=models.ForeignKey(User, related_name="owner_exam_results",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="company_exam_results",on_delete=models.SET_NULL,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="divison_exam_results",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="branch_exam_results",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="dpt_exam_results",on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.subject

