from allifmaalusersapp.models import User
from django.db import models
from allifmaalcommonapp.models import (CommonCompanyDetailsModel,CommonBaseModel, CommonTransitModel,CommonCustomersModel,CommonDivisionsModel, CommonBranchesModel, CommonDepartmentsModel,)


class PassengersModel(CommonBaseModel):
    
    # you may change these two below for manytomany field in future
    passenger=models.ForeignKey(CommonCustomersModel,blank=True,null=True,on_delete=models.CASCADE,related_name="passengers")
    flights=models.ForeignKey(CommonTransitModel,blank=True,null=True,on_delete=models.CASCADE,related_name="passengers")
 
    def __str__(self):
        return f"{self.passenger}:{self.flights}"
