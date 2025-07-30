from django.db import models
from allifmaalcommonapp.models import *

# for educational institutions
class ExaminationsModel(CommonBaseModel):
    subject=models.ForeignKey(CommonStocksModel,related_name="subject_education_exams",on_delete=models.SET_NULL,null=True,blank=True)
    exam_file=models.ForeignKey(CommonTransactionsModel,related_name="division_education_exams",on_delete=models.SET_NULL,null=True,blank=True)
    description=models.CharField(max_length=50,blank=True,null=True)
   
    def __str__(self):
        return self.subject

class ExamResultsModel(CommonBaseModel):
    subject=models.ForeignKey(ExaminationsModel,on_delete=models.SET_NULL,blank=True,null=True)
    exam_file=models.ForeignKey(CommonTransactionsModel,related_name="exam_file_education_exams_results",on_delete=models.SET_NULL,null=True,blank=True)
    
    result=models.CharField(max_length=50,blank=True,null=True)
    grade=models.CharField(max_length=50,blank=True,null=True)
   
    def __str__(self):
        return self.subject

