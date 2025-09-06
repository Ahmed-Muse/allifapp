from allifmaalusersapp.models import User
from django.db import models
from allifmaalcommonapp.models import (CommonCompanyDetailsModel,CommonPaymentTermsModel,CommonCountriesModel,CommonCodesModel,CommonBaseModel, CommonTransitModel,CommonCustomersModel,CommonDivisionsModel, CommonBranchesModel, CommonDepartmentsModel,)
from allifmaalcommonapp.constants import flight_status,Flight_Ticket_Type,Flight_Ticket_Status

##################3 EXPENSES ###########################     
class FlightsModel(CommonBaseModel):
    carrier=models.CharField(blank=True,null=True,default="destination",max_length=250)
    origin=models.ForeignKey(CommonCodesModel,blank=True,null=True,on_delete=models.SET_NULL,related_name="origin_code")
    destination=models.ForeignKey(CommonCodesModel,blank=True,null=True,on_delete=models.SET_NULL,related_name="destination_code")
    
    departure=models.DateTimeField(blank=True,null=True)
    arrival=models.DateTimeField(blank=True,null=True)
    transit=models.CharField(blank=True,null=True,default="No Transit",max_length=250)
    ticket_price=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=2,default=0.00)
    tax_amount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=2,default=0)
    captain=models.CharField(blank=True,null=True,default="captain",max_length=250)
    co_pilot=models.CharField(blank=True,null=True,default="co_pilot",max_length=250)
    flight_status=models.CharField(choices=flight_status,max_length=100,blank=True,null=True,default="Scheduled")
    flight_capacity=models.IntegerField(blank=True,null=True,default=0)
    seats_available=models.IntegerField(blank=True,null=True,default=0)
    seats_booked=models.IntegerField(blank=True,null=True,default=0)
   
    def __str__(self):
        return str(self.number)
   
class TicketsModel(CommonBaseModel):
    
    # you may change these two below for manytomany field in future
    flight=models.ForeignKey(FlightsModel,blank=True,null=True,on_delete=models.SET_NULL,related_name="passengers")
    passenger=models.ForeignKey(CommonCustomersModel,blank=True,null=True,on_delete=models.SET_NULL,related_name="passengers")
    passport=models.FileField(upload_to='myfiles/',null=True, blank=True)
    nationality=models.ForeignKey(CommonCountriesModel,blank=True,null=True,on_delete=models.SET_NULL,related_name="passengers")
    seat_number=models.CharField(blank=True,null=True,default="A1",max_length=250)
    price=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=2,default=0.00)
    tax_amount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=2,default=0)
    total_amount=models.DecimalField(max_digits=30,blank=True,null=True,decimal_places=2,default=0)
    travel_date=models.DateTimeField(blank=True,null=True)
    booking_date=models.DateTimeField(blank=True,null=True)
    ticket_status=models.CharField(choices=Flight_Ticket_Status,max_length=100,blank=True,null=True,default="Booked")
    origin=models.ForeignKey(CommonCodesModel,blank=True,null=True,on_delete=models.SET_NULL,related_name="origin_ticket")
    destination=models.ForeignKey(CommonCodesModel,blank=True,null=True,on_delete=models.SET_NULL,related_name="destination_ticket")
    
    ticket_type=models.CharField(choices=Flight_Ticket_Type,max_length=100,blank=True,null=True,default="Economy")
    payment=models.ForeignKey(CommonPaymentTermsModel,blank=True,null=True, on_delete=models.SET_NULL, related_name='terms_payment_mode_tickets')
    luggage=models.CharField(blank=True,null=True,default="30KGs Bag",max_length=250)
    children=models.CharField(blank=True,null=True,default="No Children",max_length=250)
    def __str__(self):
        return f"{self.passenger}: {self.flight} - {self.seat_number}"
