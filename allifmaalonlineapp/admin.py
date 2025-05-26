from django.contrib import admin

from allifmaalonlineapp.models import *

# Register your models here.
admin.site.register(OnlineProductsModel)
admin.site.register(OnlineCustomersModel)
admin.site.register(OnlineOrdersModel)
admin.site.register(OnlineOrderedItemsModel)
admin.site.register(OnlineCustomerShippingAddressModel)