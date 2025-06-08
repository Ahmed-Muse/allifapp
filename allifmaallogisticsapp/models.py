from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import register, slugify
from uuid import uuid4
from allifmaalcommonapp.models import CommonCustomersModel

from django.http.response import HttpResponse
# realestateapp/models.py (Conceptual BaseModel)
from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from allifmaalusersapp.models import User

import uuid # For generating unique IDs if needed


# logisticsapp/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import uuid # For generating unique IDs if needed

# Import common models from allifmaalcommonapp
from allifmaalcommonapp.models import (
    CommonCompanyDetailsModel, CommonCustomersModel,
    CommonDivisionsModel, CommonBranchesModel, CommonDepartmentsModel,
    # CommonPaymentTermsModel # Assuming you have a payment terms model if needed
)

    
# Create your models here.
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
