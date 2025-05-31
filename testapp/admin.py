from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Company)
admin.site.register(ChartOfAccount)
admin.site.register(Location)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(TransferOrder)
admin.site.register(TransferOrderItem)