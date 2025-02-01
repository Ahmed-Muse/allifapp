from import_export import resources
from .models import *

class commonCompanyResource(resources.ModelResource):
    class Meta:
        model = CommonCompanyDetailsModel

class commonBankDepositsResource(resources.ModelResource):
    class Meta:
        model = CommonShareholderBankDepositsModel

class commonBankWithdrawalResource(resources.ModelResource):
    class Meta:
        model = CommonBankWithdrawalsModel