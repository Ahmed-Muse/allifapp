from django.contrib import admin

# Register your models here.
from .models import CommonSectorsModel,CommonCompanyDetailsModel
admin.site.register(CommonSectorsModel)
admin.site.register(CommonCompanyDetailsModel)