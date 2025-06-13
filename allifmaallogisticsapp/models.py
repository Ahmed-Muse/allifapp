from allifmaalusersapp.models import User
from django.db import models
from allifmaalcommonapp.models import (CommonCompanyDetailsModel, CommonTransitModel,CommonCustomersModel,CommonDivisionsModel, CommonBranchesModel, CommonDepartmentsModel,)


    
class PassengersModel(models.Model):
    
    # you may change these two below for manytomany field in future
    passenger=models.ForeignKey(CommonCustomersModel,blank=True,null=True,on_delete=models.CASCADE,related_name="passengers")
    flights=models.ForeignKey(CommonTransitModel,blank=True,null=True,on_delete=models.CASCADE,related_name="passengers")
    comments=models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return f"{self.passenger}:{self.flights}"
