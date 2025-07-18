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
    {'name': 'Add_New_Currency', 'url_name': 'allifmaalcommonapp:commonAddCurrency'},
    
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