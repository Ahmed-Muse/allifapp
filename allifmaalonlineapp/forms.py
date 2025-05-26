from django import forms
from .models import *
from django.forms import (formset_factory, modelformset_factory)

#
class AddOnlineStockForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = OnlineProductsModel
        fields = ['name','price','digital','product_image']
        
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name'}),
            'price':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Price'}),
            
            #form-control here is the css class that we are passing
        } 
class AddOnlineCustomerForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = OnlineCustomersModel
        fields = ["systemUser",'customerName','customerEmail']
class AddOnlineOrdersForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = OnlineOrdersModel
        fields = ["customerName",'status','transaction_id']
class AddOnlineItemsToOrderForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = OnlineOrderedItemsModel
        fields = ["product",'order','quantity']

class AddOnlineCustomerShippingAddressForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = OnlineCustomerShippingAddressModel
        fields = ["customerName",'order','address']
