from django.contrib import admin

# Register your models here.
from .models import CommonSectorsModel,CommonDivisionsModel,Product,CommonCompanyDetailsModel
admin.site.register(CommonSectorsModel)
admin.site.register(CommonDivisionsModel)
admin.site.register(Product)
admin.site.register(CommonCompanyDetailsModel)