from django import forms
from .models import *
from allifmaalcommonapp.forms import CommonBaseForm
############################# start of datepicker customization ##############################
class DatePickerInput(forms.DateInput):#use this class whereever you have a date and it will give you the calender
    input_type='date'#
class TimePickerInput(forms.TimeInput):#use this wherever you have time input
    input_type='time'
class DateTimePickerInput(forms.DateTimeInput):#use this wherever you have datetime input
    input_type='datetime'
    
############################# end of datepicker customization ##############################
######################### FLIGHTS #########################
class AddFlightDetailsForm(CommonBaseForm):
    company_filtered_fields = {
        'origin': CommonCodesModel,
        'destination': CommonCodesModel,
       
        }
    class Meta(CommonBaseForm.Meta):
        model=FlightsModel
        fields=CommonBaseForm.Meta.fields + ['carrier','origin','destination','departure','arrival','transit',
                    'ticket_price','tax_amount','captain','co_pilot','flight_status',
                    'flight_capacity','seats_available','seats_booked']
        widgets = {
        **CommonBaseForm.Meta.widgets,
       
            'carrier':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'origin':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'destination':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'departure' : DateTimePickerInput(attrs={'class':'form-control'}),
            'arrival' : DateTimePickerInput(attrs={'class':'form-control'}),
            'transit':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'ticket_price':forms.TextInput(attrs={'class':'form-control','placeholder':'in USD'}),
            'tax_amount':forms.TextInput(attrs={'class':'form-control','placeholder':'in USD'}),
            'captain':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'co_pilot':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'flight_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'flight_capacity':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'seats_available':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'seats_booked':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        }
class AddFlightTicketDetailsForm(CommonBaseForm):
    company_filtered_fields = {
        'flight': FlightsModel,
        'passenger': CommonCustomersModel,
        'nationality': CommonCountriesModel,
        'origin': CommonCodesModel,
        'destination': CommonCodesModel,
        'payment': CommonPaymentTermsModel,
    }
    class Meta(CommonBaseForm.Meta):
        model=TicketsModel
        fields=CommonBaseForm.Meta.fields + ['passenger','passport','nationality','seat_number',
                    'price','tax_amount','total_amount','travel_date','booking_date',
                    'ticket_status','origin','destination','ticket_type','payment',
                    'luggage','children']
        widgets = {
        **CommonBaseForm.Meta.widgets,
       
            
            'passenger':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'passport':forms.ClearableFileInput(attrs={'class':'form-control','placeholder':''}),
            'nationality':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),  
            'seat_number':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'price':forms.TextInput(attrs={'class':'form-control','placeholder':'in USD'}),
            'tax_amount':forms.TextInput(attrs={'class':'form-control','placeholder':'in USD'}),
            'total_amount':forms.TextInput(attrs={'class':'form-control','placeholder':'in USD'}),
            'travel_date' : DateTimePickerInput(attrs={'class':'form-control'}),
            'booking_date' : DateTimePickerInput(attrs={'class':'form-control'}),
            'ticket_status':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'origin':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'destination':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'ticket_type':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'payment':forms.Select(attrs={'class':'form-control custom-field-class-for-seclect2','placeholder':''}),
            'luggage':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'children':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
        }