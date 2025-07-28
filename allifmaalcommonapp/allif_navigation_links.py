# your_app_name/configs/navigation_links.py
 
# Define general links accessible to all sectors
allifmaal_general_links = [
    {'name': 'Dashboard', 'url_name': 'allifmaalcommonapp:commonSpecificDashboard'},
    {'name': 'Company', 'url_name': 'allifmaalcommonapp:commonCompanyDetailsForClients'},
    {'name': 'HRM', 'url_name': 'allifmaalcommonapp:commonhrm'},
    {'name': 'Banks', 'url_name': 'allifmaalcommonapp:commonBanks'},
    {'name': 'Customers', 'url_name': 'allifmaalcommonapp:commonCustomers'},
    {'name': 'Suppliers', 'url_name': 'allifmaalcommonapp:commonSuppliers'},
    {'name': 'Currencies', 'url_name': 'allifmaalcommonapp:commonCurrencies'},
  
    {'name': 'Assets', 'url_name': 'allifmaalcommonapp:commonAssets'},
    {'name': 'Expenses', 'url_name': 'allifmaalcommonapp:commonExpenses'},
    {'name': 'Stocks', 'url_name': 'allifmaalcommonapp:commonStocks'},
    {'name': 'Transactions', 'url_name': 'allifmaalcommonapp:commonTransactions'},
    
    {'name': 'Transport', 'url_name': 'allifmaalcommonapp:commonTransits'},
    {'name': 'Procurement', 'url_name': 'allifmaalcommonapp:commonPurchaseOrders'},
    {'name': 'Quotations', 'url_name': 'allifmaalcommonapp:commonQuotes'},
    {'name': 'Invoices', 'url_name': 'allifmaalcommonapp:commonInvoices'},
    
    {'name': 'Ledgers', 'url_name': 'allifmaalcommonapp:commonLedgerEntries'},
    {'name': 'Payments', 'url_name': 'allifmaalcommonapp:commonCustomerPayments'},
    {'name': 'Jobs', 'url_name': 'allifmaalcommonapp:commonJobs'},
    {'name': 'Profit & Loss', 'url_name': 'allifmaalcommonapp:commonProfitAndLoss'},
    
]

# Define sector-specific links
# Each list holds dictionaries for links specific to that sector
# Use the exact string representation of your company sector (e.g., 'Healthcare', 'Education')

allifmaal_sector_specific_links= {
    'Healthcare': [
        {'name': 'Patients', 'url_name': 'allifmaalcommonapp:commonCustomers'}, 
        {'name': 'Triage', 'url_name': 'allifmaalshaafiapp:triageData'}, 
        {'name': 'Assessments', 'url_name': 'allifmaalshaafiapp:doctorAssessments'},
      
    ],
    'Education': [
        {'name': 'Students', 'url_name': 'allifmaalcommonapp:commonCustomers'},
        {'name': 'Examinations', 'url_name': 'allifmaalilmapp:examinations'},
        {'name': 'Exam Results', 'url_name': 'allifmaalilmapp:examResults'},
      
    ],
    'Hospitality': [
       
    ],
    'Real Estate': [
        
    ],
    'Logistics': [
       
    ],
    'Service': [
       
    ],
    # You can also have a 'default' or 'fallback' set of links if 'else' is important
    # 'Default': [
    #     {'name': 'Generic Module 1', 'url_name': 'common_app:generic_module_1'},
    # ]
}



# Define general links accessible to all sectors
allif_single_access_general_links = [
    {'name': 'Dashboard', 'url_name': 'allifmaalcommonapp:commonSpecificDashboard'},
    {'name': 'Company', 'url_name': 'allifmaalcommonapp:commonCompanyDetailsForClients'},
    {'name': 'HRM', 'url_name': 'allifmaalcommonapp:commonhrm'},
    {'name': 'Banks', 'url_name': 'allifmaalcommonapp:commonBanks'},
    {'name': 'Customers', 'url_name': 'allifmaalcommonapp:commonCustomers'},
    {'name': 'Suppliers', 'url_name': 'allifmaalcommonapp:commonSuppliers'},
    {'name': 'Currencies', 'url_name': 'allifmaalcommonapp:commonCurrencies'},
    {'name': 'Add_New_Currency', 'url_name': 'allifmaalcommonapp:commonAddCurrency'},
    
    {'name': 'Payment_Terms', 'url_name': 'allifmaalcommonapp:commonPaymentTerms'},
    {'name': 'Add_Payment_Term', 'url_name': 'allifmaalcommonapp:commonAddPaymentTerm'},
    {'name': 'MeasuringUnits', 'url_name': 'allifmaalcommonapp:commonUnits'},
    {'name': 'AddUnit', 'url_name': 'allifmaalcommonapp:commonAddUnit'},
    
    {'name': 'Categories', 'url_name': 'allifmaalcommonapp:commonCategories'},
    {'name': 'AddCategory', 'url_name': 'allifmaalcommonapp:commonAddCategory'},
    
    {'name': 'Codes', 'url_name': 'allifmaalcommonapp:commonCodes'},
    {'name': 'AddCode', 'url_name': 'allifmaalcommonapp:commonAddCode'},
    
    {'name': 'CompanyScopes', 'url_name': 'allifmaalcommonapp:commonCompanyScopes'},
    {'name': 'AddScope', 'url_name': 'allifmaalcommonapp:commonAddCompanyScope'},
    
    
    {'name': 'Approvers', 'url_name': 'allifmaalcommonapp:commonApprovers'},
    {'name': 'AddApprover', 'url_name': 'allifmaalcommonapp:commonAddApprover'},
    
    {'name': 'TaxParameters', 'url_name': 'allifmaalcommonapp:commonTaxParameters'},
    {'name': 'AddATaxParameter', 'url_name': 'allifmaalcommonapp:commonAddATaxParameter'},
    
    {'name': 'SupplierTaxParameters', 'url_name': 'allifmaalcommonapp:commonSupplierTaxParameters'},
    {'name': 'AddSupplierTaxParameter', 'url_name': 'allifmaalcommonapp:commonAddSupplierTaxParameter'},
    
    {'name': 'Banks', 'url_name': 'allifmaalcommonapp:commonBanks'},
    {'name': 'AddBank', 'url_name': 'allifmaalcommonapp:commonAddBank'},
    
     {'name': 'Deposits', 'url_name': 'allifmaalcommonapp:commonBankShareholderDeposits'},
    {'name': 'Withdrawals', 'url_name': 'allifmaalcommonapp:commonBankWithdrawals'},
    
    {'name': 'AddDeposits', 'url_name': 'allifmaalcommonapp:commonAddBankShareholderDeposit'},
    {'name': 'AddWithdrawals', 'url_name': 'allifmaalcommonapp:commonAddBankWithdrawal'},
    
    {'name': 'Suppliers', 'url_name': 'allifmaalcommonapp:commonSuppliers'},
    {'name': 'AddSupplier', 'url_name': 'allifmaalcommonapp:commonAddSupplier'},
    
    {'name': 'Clients', 'url_name': 'allifmaalcommonapp:commonCustomers'},
    {'name': 'AddClient', 'url_name': 'allifmaalcommonapp:commonAddCustomer'},
    
    
    {'name': 'Assets', 'url_name': 'allifmaalcommonapp:commonAssets'},
    {'name': 'AddAsset', 'url_name': 'allifmaalcommonapp:commonAddAsset'},
    
     {'name': 'Expenses', 'url_name': 'allifmaalcommonapp:commonExpenses'},
    {'name': 'AddExpense', 'url_name': 'allifmaalcommonapp:commonAddExpense'},
 
    
    {'name': 'Stocks', 'url_name': 'allifmaalcommonapp:commonStocks'},
    {'name': 'AddStockItem', 'url_name': 'allifmaalcommonapp:commonAddStockItem'},
    {'name': 'Transactions', 'url_name': 'allifmaalcommonapp:commonTransactions'},
    {'name': 'AddTransaction', 'url_name': 'allifmaalcommonapp:commonNewTransaction'},
    
    {'name': 'Spaces', 'url_name': 'allifmaalcommonapp:commonSpaces'},
    {'name': 'AddSpace', 'url_name': 'allifmaalcommonapp:commonAddSpace'},
    {'name': 'SpaceUnits', 'url_name': 'allifmaalcommonapp:commonSpaceUnits'},
    {'name': 'AddSpaceUnit', 'url_name': 'allifmaalcommonapp:commonAddSpaceUnit'},
    
     {'name': 'PurchaseOrders', 'url_name': 'allifmaalcommonapp:commonPurchaseOrders'},
    {'name': 'AddPurchaseOrder', 'url_name': 'allifmaalcommonapp:commonNewPurchaseOrder'},
    
     {'name': 'TransferOrders', 'url_name': 'allifmaalcommonapp:commonTransferOrders'},
    {'name': 'AddTransferOrder', 'url_name': 'allifmaalcommonapp:commonNewTransferOrder'},
    
    {'name': 'Quotes', 'url_name': 'allifmaalcommonapp:commonQuotes'},
    {'name': 'AddQuote', 'url_name': 'allifmaalcommonapp:commonNewQuote'},
    
     {'name': 'Invoices', 'url_name': 'allifmaalcommonapp:commonInvoices'},
    {'name': 'AddInvoice', 'url_name': 'allifmaalcommonapp:commonNewInvoice'},
    
    {'name': 'CreditNotes', 'url_name': 'allifmaalcommonapp:commonCreditNotes'},
    {'name': 'AddCreditNote', 'url_name': 'allifmaalcommonapp:commonNewCreditNote'},
    
    {'name': 'Transport', 'url_name': 'allifmaalcommonapp:commonTransits'},
    {'name': 'Procurement', 'url_name': 'allifmaalcommonapp:commonPurchaseOrders'},
    {'name': 'Quotations', 'url_name': 'allifmaalcommonapp:commonQuotes'},
    {'name': 'Invoices', 'url_name': 'allifmaalcommonapp:commonInvoices'},
    
    {'name': 'LedgerEntries', 'url_name': 'allifmaalcommonapp:commonLedgerEntries'},
    {'name': 'CustomerPayments', 'url_name': 'allifmaalcommonapp:commonCustomerPayments'},
    
    {'name': 'ReceiptClientPayment', 'url_name': 'allifmaalcommonapp:commonReceiveCustomerMoney'},
    
     {'name': 'PostedCustomerPayments', 'url_name': 'allifmaalcommonapp:commonPostedCustomerPayments'},
     {'name': 'SupplierPayments', 'url_name': 'allifmaalcommonapp:commonSupplierPayments'},
     {'name': 'PostedSupplierPayments', 'url_name': 'allifmaalcommonapp:commonPostedSupplierPayments'},
     {'name': 'DirectSupplierPayment', 'url_name': 'allifmaalcommonapp:commonPaySupplierDirect'},
     
     
    {'name': 'Salaries', 'url_name': 'allifmaalcommonapp:commonSalaries'},
    {'name': 'AddSalary', 'url_name': 'allifmaalcommonapp:commonAddSalary'},
    {'name': 'PostedSalaries', 'url_name': 'allifmaalcommonapp:commonPostedSalaries'},
     
     
    
    {'name': 'Jobs', 'url_name': 'allifmaalcommonapp:commonJobs'},
    {'name': 'Profit & Loss', 'url_name': 'allifmaalcommonapp:commonProfitAndLoss'},
    
]

# Define sector-specific links
# Each list holds dictionaries for links specific to that sector
# Use the exact string representation of your company sector (e.g., 'Healthcare', 'Education')