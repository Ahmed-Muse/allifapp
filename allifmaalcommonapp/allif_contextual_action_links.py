# myerpapp/configs/contextual_actions.py

allif_sector_contextual_action_require_pk_links= {
    'Healthcare': [
    {'name': 'AddTriageData', 'url_name': 'allifmaalshaafiapp:AddTriageData', 'requires_pk': True},
    {'name': 'addDoctorAssessment', 'url_name': 'allifmaalshaafiapp:addDoctorAssessment', 'requires_pk': True},
    {'name': 'common_currency_pdf', 'url_name': 'allifmaalcommonapp:common_currency_pdf', 'requires_pk': True},
    {'name': 'commonWantToDeleteCurrency', 'url_name': 'allifmaalcommonapp:commonWantToDeleteCurrency', 'requires_pk': True},
    
    {'name': 'commonWantToDeletePaymentTerm', 'url_name': 'allifmaalcommonapp:commonWantToDeletePaymentTerm', 'requires_pk': True},
    {'name': 'commonDeletePaymentTerm', 'url_name': 'allifmaalcommonapp:commonDeletePaymentTerm', 'requires_pk': True},
    
    {'name': 'commonConfirmDeleteUnits', 'url_name': 'allifmaalcommonapp:commonConfirmDeleteUnits', 'requires_pk': True},
    {'name': 'commonDeleteUnit', 'url_name': 'allifmaalcommonapp:commonDeleteUnit', 'requires_pk': True},
   
    {'name': 'commonWantToDeleteCategory', 'url_name': 'allifmaalcommonapp:commonWantToDeleteCategory', 'requires_pk': True},
    {'name': 'commonDeleteCategory', 'url_name': 'allifmaalcommonapp:commonDeleteCategory', 'requires_pk': True},
    
    {'name': 'commonWantToDeleteCode', 'url_name': 'allifmaalcommonapp:commonWantToDeleteCode', 'requires_pk': True},
    {'name': 'commonDeleteCode', 'url_name': 'allifmaalcommonapp:commonDeleteCode', 'requires_pk': True},
    
    {'name': 'commonWantToDeleteScope', 'url_name': 'allifmaalcommonapp:commonWantToDeleteScope', 'requires_pk': True},
    {'name': 'commonDeleteCompanyScope', 'url_name': 'allifmaalcommonapp:commonDeleteCompanyScope', 'requires_pk': True},
    
    {'name': 'commonWantToDeleteApprover', 'url_name': 'allifmaalcommonapp:commonWantToDeleteApprover', 'requires_pk': True},
    {'name': 'commonDeleteApprover', 'url_name': 'allifmaalcommonapp:commonDeleteApprover', 'requires_pk': True},
    
    {'name': 'CommonDeleteTaxParameter', 'url_name': 'allifmaalcommonapp:CommonDeleteTaxParameter', 'requires_pk': True},
    {'name': 'commonWantToDeleteTaxParameter', 'url_name': 'allifmaalcommonapp:commonWantToDeleteTaxParameter', 'requires_pk': True},
  
    {'name': 'commonWantToDeleteSupplierTaxParameter', 'url_name': 'allifmaalcommonapp:commonWantToDeleteSupplierTaxParameter', 'requires_pk': True},
    {'name': 'CommonSupplierDeleteTaxParameter', 'url_name': 'allifmaalcommonapp:CommonSupplierDeleteTaxParameter', 'requires_pk': True},
    
    {'name': 'wanttodeletebank', 'url_name': 'allifmaalcommonapp:commonWantToDeleteBank', 'requires_pk': True},
    {'name': 'commonDeleteBank', 'url_name': 'allifmaalcommonapp:commonDeleteBank', 'requires_pk': True},
    
    {'name': 'DeleteDeposit', 'url_name': 'allifmaalcommonapp:commonWantToDeleteDeposit', 'requires_pk': True},
  
     {'name': 'DeleteWithdrawal', 'url_name': 'allifmaalcommonapp:commonWantToDeleteWithdrawal', 'requires_pk': True},
  
  
  
    ],
    
    'Education': [
         {'name': 'addExamDetails', 'url_name': 'allifmaalilmapp:addExamDetails', 'requires_pk': True},
    ],
    'Real Estate': [
    ],
    # You can also add a 'Default' key here if you want actions that appear
    # when no specific sector matches, or for a 'General' sector.
} # <--- REMOVE THE TRAILING COMMA HERE!

#{% url 'allifmaalcommonapp:common_currency_pdf' allifquery.id user_var glblslug %}