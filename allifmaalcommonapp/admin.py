from django.contrib import admin

# Register your models here.
from .models import CommonSectorsModel,CommonCustomersModel,CommonCompanyDetailsModel,CommonSuppliersModel,CommonDivisionsModel,CommonBranchesModel,CommonDepartmentsModel
admin.site.register(CommonSectorsModel)
admin.site.register(CommonCompanyDetailsModel)
admin.site.register(CommonSuppliersModel)
admin.site.register([CommonBranchesModel,CommonDepartmentsModel,CommonDivisionsModel,CommonCustomersModel])