
# Define general links accessible to all sectors
# Each dictionary should have 'name', 'url_name', and 'description' (optional but good for search)
allifmaal_general_links = [
    {'name': 'ERP Home', 'url_name': 'allifmaalcommonapp:commonHome', 'description': 'Allifapp ERP Home'},
    {'name': 'Dashboard Overview', 'url_name': 'allifmaalcommonapp:commonSpecificDashboard', 'description': 'View the specific dashboard for your company.'},
    {'name': 'Company Details', 'url_name': 'allifmaalcommonapp:commonCompanyDetailsForClients', 'description': 'View and manage your company profile.'},
    {'name': 'HRM', 'url_name': 'allifmaalcommonapp:commonhrm', 'description': 'Human Resources Management module.'},
    {'name': 'Banks', 'url_name': 'allifmaalcommonapp:commonBanks', 'description': 'Manage bank accounts and transactions.'},
    {'name': 'Customers', 'url_name': 'allifmaalcommonapp:commonCustomers', 'description': 'Manage customer information.'},
    {'name': 'Suppliers', 'url_name': 'allifmaalcommonapp:commonSuppliers', 'description': 'Manage supplier information.'},
    
    {'name': 'Assets', 'url_name': 'allifmaalcommonapp:commonAssets', 'description': 'Track and manage company assets.'},
    {'name': 'Expenses', 'url_name': 'allifmaalcommonapp:commonExpenses', 'description': 'Record and categorize company expenses.'},
    {'name': 'Stocks', 'url_name': 'allifmaalcommonapp:commonStocks', 'description': 'Manage inventory and stock levels.'},
    {'name': 'Transactions', 'url_name': 'allifmaalcommonapp:commonTransactions', 'description': 'View all financial transactions.'},
    
    {'name': 'Transport', 'url_name': 'allifmaalcommonapp:commonTransits', 'description': 'Manage transportation and logistics.'},
    {'name': 'Procurement', 'url_name': 'allifmaalcommonapp:commonPurchaseOrders', 'description': 'Handle purchase orders and vendor management.'},
    {'name': 'Quotations', 'url_name': 'allifmaalcommonapp:commonQuotes', 'description': 'Create and manage customer quotations.'},
    {'name': 'Invoices', 'url_name': 'allifmaalcommonapp:commonInvoices', 'description': 'Generate and track customer invoices.'},
    
    {'name': 'Ledgers', 'url_name': 'allifmaalcommonapp:commonLedgerEntries', 'description': 'Manage general ledger entries.'},
    {'name': 'Payments', 'url_name': 'allifmaalcommonapp:commonCustomerPayments', 'description': 'Process and track customer payments.'},
    {'name': 'Jobs', 'url_name': 'allifmaalcommonapp:commonJobs', 'description': 'Manage job orders and projects.'},
    {'name': 'Profit & Loss', 'url_name': 'allifmaalcommonapp:commonProfitAndLoss', 'description': 'View financial profit and loss statements.'},

    # Add other general ERP features
    {'name': 'Tax Parameters List', 'url_name': 'allifmaalcommonapp:commonTaxParameters', 'description': 'Manage and view all applicable tax parameters.'},
    {'name': 'Add New Tax Parameter', 'url_name': 'allifmaalcommonapp:commonTaxParameters', 'description': 'Access the form to add a new tax rate or type.'},
    {'name': 'Export Tax Data (CSV)', 'url_name': 'allifmaalcommonapp:export_tax_parameters_csv', 'description': 'Download all tax parameters as a CSV file.'},
    {'name': 'Manage Taxes (Formset)', 'url_name': 'allifmaalcommonapp:manage_tax_parameters_formset', 'description': 'Bulk add, edit, or delete multiple tax parameters.'},
   
]

# Define sector-specific links
# Each list holds dictionaries for links specific to that sector
# Use the exact string representation of your company sector (e.g., 'Healthcare', 'Education')
# Add 'description' for better searchability
allifmaal_sector_specific_links = {
    'Healthcare': [
        {'name': 'Patients', 'url_name': 'allifmaalcommonapp:commonCustomers', 'description': 'Manage patient records and appointments.'},
        {'name': 'Triage Data', 'url_name': 'allifmaalshaafiapp:triageData', 'description': 'Record and review patient triage information.'},
        {'name': 'Doctor Assessments', 'url_name': 'allifmaalshaafiapp:doctorAssessments', 'description': 'Access medical assessment forms.'},
        {'name': 'Medical Inventory', 'url_name': 'allifmaalshaafiapp:medicalInventory', 'description': 'Manage medical supplies and equipment.'},
        {'name': 'Prescriptions', 'url_name': 'allifmaalshaafiapp:prescriptions', 'description': 'Issue and track patient prescriptions.'},
    ],
    'Education': [
        {'name': 'Students', 'url_name': 'allifmaalcommonapp:commonCustomers', 'description': 'Manage student records and enrollment.'},
        {'name': 'Examinations', 'url_name': 'allifmaalilmapp:examinations', 'description': 'Schedule and manage academic examinations.'},
        {'name': 'Exam Results', 'url_name': 'allifmaalilmapp:examResults', 'description': 'Record and view student examination results.'},
        {'name': 'Courses', 'url_name': 'allifmaalilmapp:courses', 'description': 'Manage academic courses and curriculum.'},
        {'name': 'Faculty Management', 'url_name': 'allifmaalilmapp:faculty', 'description': 'Manage faculty and staff profiles.'},
    ],
    'Hospitality': [
        {'name': 'Reservations', 'url_name': 'allifmaalhospitalityapp:reservations', 'description': 'Manage guest bookings and reservations.'},
        {'name': 'Room Management', 'url_name': 'allifmaalhospitalityapp:room_management', 'description': 'Oversee room availability and status.'},
        {'name': 'Guest Services', 'url_name': 'allifmaalhospitalityapp:guest_services', 'description': 'Handle guest requests and amenities.'},
    ],
    'Real Estate': [
        {'name': 'Properties', 'url_name': 'allifmaalrealestateapp:properties', 'description': 'Manage property listings and details.'},
        {'name': 'Leases', 'url_name': 'allifmaalrealestateapp:leases', 'description': 'Administer lease agreements.'},
        {'name': 'Client Portfolios', 'url_name': 'allifmaalrealestateapp:client_portfolios', 'description': 'Manage client property portfolios.'},
    ],
    'Logistics': [
        {'name': 'Shipments', 'url_name': 'allifmaallogisticsapp:shipments', 'description': 'Track and manage cargo shipments.'},
        {'name': 'Fleet Management', 'url_name': 'allifmaallogisticsapp:fleet_management', 'description': 'Oversee vehicle fleet and maintenance.'},
        {'name': 'Routes', 'url_name': 'allifmaallogisticsapp:routes', 'description': 'Plan and optimize delivery routes.'},
    ],
    'Service': [
        {'name': 'Service Requests', 'url_name': 'allifmaalserviceapp:service_requests', 'description': 'Manage customer service requests.'},
        {'name': 'Technician Scheduling', 'url_name': 'allifmaalserviceapp:tech_scheduling', 'description': 'Schedule and dispatch service technicians.'},
        {'name': 'Service Contracts', 'url_name': 'allifmaalserviceapp:service_contracts', 'description': 'Administer service contracts.'},
    ],
    # You can also have a 'default' or 'fallback' set of links if 'else' is important
    # 'Default': [
    #     {'name': 'Generic Module 1', 'url_name': 'common_app:generic_module_1', 'description': 'Generic feature for all.'},
    # ]
}
