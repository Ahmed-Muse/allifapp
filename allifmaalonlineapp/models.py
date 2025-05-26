from django.db import models
#from django.contrib.auth.models import User
from allifmaalusersapp.models import User



# Create your models here.

class OnlineCustomersModel(models.Model):
    systemUser=models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    #onetoone relationship means that a user can only have one customer and customer can have one user
    #on_delete relationship means that delete the item if the user is deleted
    
    customerName = models.CharField(max_length=200, null=True)
    customerEmail = models.CharField(max_length=200)
    
    
    def __str__(self):
    		return self.customerName

# Create your models here.
class OnlineProductsModel(models.Model):
    name = models.CharField(max_length=255, null=True,blank=True)
    price=models.DecimalField(max_digits=7,decimal_places=2,blank=True)
    digital = models.BooleanField(default=False,blank=True, null=True)#If the item is digital, we dont need to ship
    #and if digital is false, then it means we need to ship as it is physical item
    product_image=models.ImageField(null=True, blank=True,upload_to='ecommerceapp/images/products')
       
    def __str__(self):
        return self.name
    @property# this is property decorator that will enable us to access this as an attribute rather as a method
    def imageURL(self):#this method will query if there is an image, if there isnt, it will return empty string
        #if we dont do this method, we may get errors if one of the images is deleted.
        try:
            url=self.product_image.url
        except:
            url = ''
        return url

	
class OnlineOrdersModel(models.Model):
    customerName = models.ForeignKey(OnlineCustomersModel, on_delete=models.SET_NULL, null=True,blank=True)#if customer is deleted, we dont want to delete the order but rather set the customer value to null
    dateOrdered=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False, null=True, blank=False)
    transaction_id=models.CharField(max_length=100, null=True,blank=True)
    
    def __str__(self):
        return str(self.id) #it was giving errors hence commented out
        #return self.customer

    @property
    def shipping(self):
        shipping=False#by default shipping is false
        orderitems=self.onlineordereditemsmodel_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True
        return shipping
    
    @property
    def get_cart_total(self):# sin
        orderitems = self.onlineordereditemsmodel_set.all()
        total=sum([item.get_total for item in orderitems])
        return total
    
    @property # since now this is a property, we can access it in the template
    def get_cart_items(self):
        orderitems = self.onlineordereditemsmodel_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

    
class OnlineOrderedItemsModel(models.Model):
    product = models.ForeignKey(OnlineProductsModel, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(OnlineOrdersModel, on_delete=models.SET_NULL, null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    #calculate totals for the order items by creating the method below
    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total
    
class OnlineCustomerShippingAddressModel(models.Model):
     customerName = models.ForeignKey(OnlineCustomersModel, on_delete=models.SET_NULL, null=True,blank=True)
     order = models.ForeignKey(OnlineOrdersModel, on_delete=models.SET_NULL, null=True,blank=True)
     address=models.CharField(max_length=200, null=True)
     
     date_added = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
           return str(self.address)


   