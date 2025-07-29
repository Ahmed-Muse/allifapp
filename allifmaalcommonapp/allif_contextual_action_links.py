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
    
    {'name': 'DeleteSupplierConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteSupplier', 'requires_pk': True},
  
    {'name': 'DeleteSupplier', 'url_name': 'allifmaalcommonapp:commonDeleteSupplier', 'requires_pk': True},
    
    {'name': 'DeleteCustomerConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteCustomer', 'requires_pk': True},
  
    {'name': 'DeleteCustomer', 'url_name': 'allifmaalcommonapp:commonDeleteSupplier', 'requires_pk': True},
    
    {'name': 'TopUpCustomerAccount', 'url_name': 'allifmaalcommonapp:commonTopUpCustomerAccount', 'requires_pk': True},
    {'name': 'CustomerLedgers', 'url_name': 'allifmaalcommonapp:commonCustomerLedgerEntries', 'requires_pk': True},
   
   {'name': 'DeleteAssetConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteAsset', 'requires_pk': True},
    {'name': 'DeleteAsset', 'url_name': 'allifmaalcommonapp:commonDeleteAsset', 'requires_pk': True},
   

{'name': 'DeleteExpenseConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteExpense', 'requires_pk': True},
    {'name': 'DeleteExpense', 'url_name': 'allifmaalcommonapp:commonDeleteExpense', 'requires_pk': True},
   
{'name': 'DeleteTransactionConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteTransaction', 'requires_pk': True},
    {'name': 'DeleteTransaction', 'url_name': 'allifmaalcommonapp:commonDeleteTransaction', 'requires_pk': True},
   
  {'name': 'commonAddTransactionDetails', 'url_name': 'allifmaalcommonapp:commonAddTransactionDetails', 'requires_pk': True},
   
   {'name': 'commonTransactionDetails', 'url_name': 'allifmaalcommonapp:commonTransactionDetails', 'requires_pk': True},
   
  {'name': 'DeleteSpaceConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteSpace', 'requires_pk': True},
   
   {'name': 'DeleteSpace', 'url_name': 'allifmaalcommonapp:commonDeleteSpace', 'requires_pk': True},
   
   {'name': 'DeleteSpaceUnitConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteSpaceUnit', 'requires_pk': True},
    {'name': 'DeleteSpaceUnit', 'url_name': 'allifmaalcommonapp:commonDeleteSpaceUnit', 'requires_pk': True},
   
   {'name': 'DeleteStockItemConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteStockItem', 'requires_pk': True},
    {'name': 'DeleteStockItem', 'url_name': 'allifmaalcommonapp:commonDeleteStockItem', 'requires_pk': True},
   
  
  {'name': 'DeletePurchaseOrderConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeletePO', 'requires_pk': True},
    {'name': 'DeletePurchaseOrder', 'url_name': 'allifmaalcommonapp:commonDeletePO', 'requires_pk': True},
       {'name': 'potopdf', 'url_name': 'allifmaalcommonapp:common_purchase_order_pdf', 'requires_pk': True},
    {'name': 'pomiscosts', 'url_name': 'allifmaalcommonapp:commonPOMiscCost', 'requires_pk': True},
   
   {'name': 'DeleteTransferOrderConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteTransferOrder', 'requires_pk': True},
    {'name': 'DeleteTransferOrder', 'url_name': 'allifmaalcommonapp:commonDeleteTransferOrder', 'requires_pk': True},
   {'name': 'trfpdf', 'url_name': 'allifmaalcommonapp:commonTransferOrderPdf', 'requires_pk': True},
   
   {'name': 'quotepdf', 'url_name': 'allifmaalcommonapp:commonQuoteToPdf', 'requires_pk': True},
   {'name': 'addquotedetails', 'url_name': 'allifmaalcommonapp:commonAddQuoteDetails', 'requires_pk': True},
  {'name': 'addquoteitems', 'url_name': 'allifmaalcommonapp:commonAddQuoteItems', 'requires_pk': True},
   
   {'name': 'DeleteQuoteConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteQuote', 'requires_pk': True},
   
   {'name': 'DeleteQuote', 'url_name': 'allifmaalcommonapp:commonDeleteQuote', 'requires_pk': True},
   
   {'name': 'InvoiceDetails', 'url_name': 'allifmaalcommonapp:commonAddInvoiceDetails', 'requires_pk': True},
   {'name': 'DeleteInvoice', 'url_name': 'allifmaalcommonapp:commonDeleteInvoice', 'requires_pk': True},
   {'name': 'DeleteInvoiceConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteInvoice', 'requires_pk': True},
   {'name': 'PostInvoice', 'url_name': 'allifmaalcommonapp:commonPostInvoice', 'requires_pk': True},
   {'name': 'invoicepdf', 'url_name': 'allifmaalcommonapp:commonInvoiceToPdf', 'requires_pk': True},
   
   
   {'name': 'CreditNotePdf', 'url_name': 'allifmaalcommonapp:commonCreditNotePdf', 'requires_pk': True},
   {'name': 'PostCreditNote', 'url_name': 'allifmaalcommonapp:commonPostCreditNote', 'requires_pk': True},
   {'name': 'AddCNDetails', 'url_name': 'allifmaalcommonapp:commonAddCreditNoteDetails', 'requires_pk': True},
   {'name': 'DeleteCreditNote', 'url_name': 'allifmaalcommonapp:commonDeleteCreditNote', 'requires_pk': True},
   {'name': 'DeleteCreditNoteConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteCreditNote', 'requires_pk': True},
  
  {'name': 'StaffLedgerEntries', 'url_name': 'allifmaalcommonapp:commonStaffLedgerEntries', 'requires_pk': True},
    {'name': 'CustomerLedgerEntries', 'url_name': 'allifmaalcommonapp:commonCustomerLedgerEntries', 'requires_pk': True},
    
    {'name': 'SupplierLedgerEntries', 'url_name': 'allifmaalcommonapp:commonSupplierLedgerEntries', 'requires_pk': True},
    {'name': 'DeleteLedgerEntryConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteLedgerEntry', 'requires_pk': True},
    {'name': 'DeleteLedgerEntry', 'url_name': 'allifmaalcommonapp:commonDeleteLedgerEntry', 'requires_pk': True},
    
    {'name': 'PaySupplier', 'url_name': 'allifmaalcommonapp:commonPaySupplier', 'requires_pk': True},
    {'name': 'DeleteSupplierPaymentConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteSupplierPayment', 'requires_pk': True},
    {'name': 'DeleteSupplierPayment', 'url_name': 'allifmaalcommonapp:commonDeleteSupplierPayment', 'requires_pk': True},
    {'name': 'SupplierPaymentDetails', 'url_name': 'allifmaalcommonapp:commonSupplierPaymentDetails', 'requires_pk': True},
    
    {'name': 'PostSupplierPayment', 'url_name': 'allifmaalcommonapp:commonPostSupplierPayment', 'requires_pk': True},
    
     {'name': 'SupplierPaymentPdf', 'url_name': 'allifmaalcommonapp:commonSupplierStatementpdf', 'requires_pk': True},
   
   
   {'name': 'DeleteCustomerPayment', 'url_name': 'allifmaalcommonapp:commonDeleteCustomerPayment', 'requires_pk': True},
   
   {'name': 'CustomerPaymentDetails', 'url_name': 'allifmaalcommonapp:commonCustomerPaymentDetails', 'requires_pk': True},
   
   {'name': 'PostCustomerPayment', 'url_name': 'allifmaalcommonapp:commonPostCustomerPayment', 'requires_pk': True},
   
   {'name': 'CustomerStatementPdf', 'url_name': 'allifmaalcommonapp:commonCustomerStatementpdf', 'requires_pk': True},
   
   {'name': 'DeleteCustomerPaymentConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteCustomerPayment', 'requires_pk': True},
   
   {'name': 'SalaryDetails', 'url_name': 'allifmaalcommonapp:commonSalaryDetails', 'requires_pk': True},
   {'name': 'EditSalary', 'url_name': 'allifmaalcommonapp:commonEditSalaryDetails', 'requires_pk': True},
   {'name': 'PostSalary', 'url_name': 'allifmaalcommonapp:commonPostSalary', 'requires_pk': True},
   
   {'name': 'DeleteSalaryConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteSalary', 'requires_pk': True},
   
  {'name': 'DeleteJobConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteJob', 'requires_pk': True},
   {'name': 'DeleteJob', 'url_name': 'allifmaalcommonapp:commonDeleteJob', 'requires_pk': True},
   {'name': 'AddJobDetails', 'url_name': 'allifmaalcommonapp:commonAddJobDetails', 'requires_pk': True},
   {'name': 'InvoiceJob', 'url_name': 'allifmaalcommonapp:commonInvoiceJob', 'requires_pk': True},
   {'name': 'JobInvoicePdf', 'url_name': 'allifmaalcommonapp:commonJobInvoicePdf', 'requires_pk': True},
   {'name': 'JobTransactionPdf', 'url_name': 'allifmaalcommonapp:commonJobTransactionReportpdf', 'requires_pk': True},
   {'name': 'AddJobItems', 'url_name': 'allifmaalcommonapp:commonAddJobItems', 'requires_pk': True},
   
   {'name': 'DeleteTransitConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteTransit', 'requires_pk': True},
   {'name': 'DeleteTransit', 'url_name': 'allifmaalcommonapp:commonDeleteTransit', 'requires_pk': True},
   {'name': 'AddTransitDetails', 'url_name': 'allifmaalcommonapp:commonAddTransitDetails', 'requires_pk': True},
   {'name': 'AddShipmentItems', 'url_name': 'allifmaalcommonapp:commonAddShipmentItems', 'requires_pk': True},
   {'name': 'TransitPdf', 'url_name': 'allifmaalcommonapp:commonTransitToPdf', 'requires_pk': True},
   
   {'name': 'TransitItemDetails', 'url_name': 'allifmaalcommonapp:commonShipmentItemDetails', 'requires_pk': True},
    {'name': 'DeleteShipmentItem', 'url_name': 'allifmaalcommonapp:commonDeleteShipmentItem', 'requires_pk': True},
   {'name': 'DeleteProgressConfirm', 'url_name': 'allifmaalcommonapp:commonWantToDeleteProgress', 'requires_pk': True},
   
    {'name': 'AddProgress', 'url_name': 'allifmaalcommonapp:commonAddProgress', 'requires_pk': True},
   
   
  
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