from django.db import models
from allifmaalcommonapp.models import *

# for educational institutions
class CommonFormsModel(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)
    owner=models.ForeignKey(User, related_name="cmnusfrm",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmnfrmcmp",on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=30,blank=True,null=True, default='comment')
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsforms",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchforms",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="deptforms",on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.name

class CommonClassesModel(models.Model):
    form=models.ForeignKey(CommonFormsModel,on_delete=models.SET_NULL,blank=True,null=True)
    name=models.CharField(max_length=50,blank=True,null=True)
    contact=models.CharField(max_length=50,blank=True,null=True)
    size=models.IntegerField(blank=True,null=True)
    owner=models.ForeignKey(User, related_name="cmnusrclsrln",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="cmnclscmpy",on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(auto_now=True)
    comments=models.CharField(max_length=30,blank=True,null=True, default='comment')
    division=models.ForeignKey(CommonDivisionsModel,related_name="dvsclsss",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="brnchclss",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="dptclss",on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.name

