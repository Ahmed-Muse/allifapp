from allifmaalusersapp.models import User
from django.db import models
from allifmaalcommonapp.models import (CommonCompanyDetailsModel, CommonCustomersModel,CommonDivisionsModel, CommonBranchesModel, CommonDepartmentsModel,)

class AirportsModel(models.Model):
    owner=models.ForeignKey(User,related_name="airports_owner",on_delete=models.SET_NULL,null=True,blank=True)
    company=models.ForeignKey(CommonCompanyDetailsModel,related_name="airports_company_relname",on_delete=models.CASCADE,null=True,blank=True)
    division=models.ForeignKey(CommonDivisionsModel,related_name="airports_division",on_delete=models.SET_NULL,null=True,blank=True)
    branch=models.ForeignKey(CommonBranchesModel,related_name="airports_branch",on_delete=models.SET_NULL,null=True,blank=True)
    department=models.ForeignKey(CommonDepartmentsModel,related_name="airports_department",on_delete=models.SET_NULL,null=True,blank=True)
    
    airport_name=models.CharField(max_length=100,blank=True,null=True)
    airport_code=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=60,blank=True,null=True)
    city=models.CharField(max_length=60,blank=True,null=True)
    
    def __str__(self):
        return f"{self.code}: {self.city}:"


class FlightsModel(models.Model):
    flight_origin=models.ForeignKey(AirportsModel,blank=True,null=True,on_delete=models.CASCADE,related_name="departures")
    flight_destination=models.ForeignKey(AirportsModel,blank=True,null=True,on_delete=models.CASCADE,related_name="arrivals")
    flight_duration=models.IntegerField(blank=True,null=True)
    def __str__(self):
        return f"{self.id}: {self.flight_origin}:{self.flight_destination}"
    
class PassengersModel(models.Model):
    
    # you may change these two below for manytomany field in future
    passenger=models.ForeignKey(CommonCustomersModel,blank=True,null=True,on_delete=models.CASCADE,related_name="passengers")
    flights=models.ForeignKey(FlightsModel,blank=True,null=True,on_delete=models.CASCADE,related_name="passengers")
    comments=models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return f"{self.passenger}:{self.flights}"
