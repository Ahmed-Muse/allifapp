from django.contrib import admin

# Register your models here.
from .models import CommonSectorsModel,CommonDivisionsModel
admin.site.register(CommonSectorsModel)
admin.site.register(CommonDivisionsModel)