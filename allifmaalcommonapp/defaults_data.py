# your_app_name/defaults_data.py

# Define default Company Scopes
DEFAULT_COMPANY_SCOPES = [
    {'name': 'General Service', 'comments': 'Covers all services and products offered by the company.'},
    {'name': 'Sales', 'comments': 'Scope for sales operations.'},
    {'name': 'Marketing', 'comments': 'Scope for marketing activities.'},
    {'name': 'Operations', 'comments': 'Scope for daily operational activities.'},
    {'name': 'Finance', 'comments': 'Scope for financial management.'},
]

# Define default Taxes (e.g., Sales Tax, VAT)
DEFAULT_TAXES = [
    {'taxname': 'Sales Tax', 'taxdescription': 'Standard Sales Tax applicable to goods and services.', 'taxrate': 5.0},
    {'taxname': 'VAT', 'taxdescription': 'Value Added Tax', 'taxrate': 15.0}, # Example VAT rate
    {'taxname': 'Withholding Tax', 'taxdescription': 'Tax withheld from payments to suppliers/employees.', 'taxrate': 10.0},
]
 
# Define default Currencies
DEFAULT_CURRENCIES = [
    {'description': 'USD', 'comments': 'United States Dollar'},
    {'description': 'EUR', 'comments': 'Euro'},
    {'description': 'SSH', 'comments': 'Somali Shilling'}, # Added for local relevance
    {'description': 'KES', 'comments': 'Kenyan Shilling'},
    {'description': 'DJF', 'comments': 'Djiboutian Franc'}, # Added for local relevance
]

# Define default Payment Terms
DEFAULT_PAYMENT_TERMS = [
    {'description': 'Cash', 'comments': 'Immediate payment upon delivery/service'},
    {'description': 'Credit', 'comments': 'Payment terms based on credit agreement'},
    {'description': 'Net 15', 'comments': 'Payment due 15 days from invoice date'},
    {'description': 'Net 30', 'comments': 'Payment due 30 days from invoice date'},
    {'description': 'Net 60', 'comments': 'Payment due 60 days from invoice date'},
    {'description': 'Upon Receipt', 'comments': 'Payment due immediately upon receipt of invoice'},
]

# Define default Units of Measure
DEFAULT_UNITS_OF_MEASURE = [
    {'description': 'Kgs', 'comments': 'Kilograms - standard weight unit'},
    {'description': 'Liters', 'comments': 'Liters - standard volume unit'},
    {'description': 'mm', 'comments': 'Millimeters - standard length unit'},
    {'description': 'gm', 'comments': 'Grams - small weight unit'},
    {'description': 'Pcs', 'comments': 'Pieces - for individual items'},
    {'description': 'Box', 'comments': 'Standard box unit'},
    {'description': 'Bottle', 'comments': 'Standard bottle unit'},
    {'description': 'Roll', 'comments': 'Standard roll unit'},
    {'description': 'Pack', 'comments': 'Standard pack unit'},
    {'description': 'Hour', 'comments': 'Time unit for services'},
    {'description': 'Day', 'comments': 'Time unit for services'},
    {'description': 'Unit', 'comments': 'Generic unit for various items'},
]

# Define default Operation Years (e.g., Fiscal Year)
# Note: 'year' field should be CharField or IntegerField, not a specific year number here.
DEFAULT_OPERATION_YEARS = [
    {'year': 'Operation Year One', 'comments': 'The initial fiscal year of operation.'},
    {'year': 'Current Year', 'comments': 'Represents the current active operating year.'},
]

# 'operation_year_name' will be used to link to the DEFAULT_OPERATION_YEARS
DEFAULT_OPERATION_YEAR_TERMS = [
    {'operation_year_name': 'Operation Year One', 'name': 'Term One', 'comments': 'First term of Operation Year One'},
    {'operation_year_name': 'Operation Year One', 'name': 'Term Two', 'comments': 'Second term of Operation Year One'},
    {'operation_year_name': 'Operation Year One', 'name': 'Term Three', 'comments': 'Third term of Operation Year One'},
    {'operation_year_name': 'Operation Year One', 'name': 'Term Four', 'comments': 'Fourth term of Operation Year One'},
    {'operation_year_name': 'Current Year', 'name': 'Q1', 'comments': 'Quarter 1 of the Current Year'},
    {'operation_year_name': 'Current Year', 'name': 'Q2', 'comments': 'Quarter 2 of the Current Year'},
    {'operation_year_name': 'Current Year', 'name': 'Q3', 'comments': 'Quarter 3 of the Current Year'},
    {'operation_year_name': 'Current Year', 'name': 'Q4', 'comments': 'Quarter 4 of the Current Year'},
]

# Define default Codes (generic codes for various purposes)
DEFAULT_CODES = [
    {'code': '0001', 'name': 'Standard Code 0001', 'description': 'General purpose code 1'},
    {'code': '0002', 'name': 'Standard Code 0002', 'description': 'General purpose code 2'},
    {'code': '0003', 'name': 'Item Type - Physical', 'description': 'Code for physical inventory items'},
    {'code': '0004', 'name': 'Item Type - Service', 'description': 'Code for service items'},
    {'code': '0005', 'name': 'Customer Category - Retail', 'description': 'Code for retail customer category'},
]

# Define default Categories (generic categories for various lists/items)
DEFAULT_CATEGORIES = [
    {'name': 'General Category 1', 'description': 'First general category', 'code': 'GEN1'},
    {'name': 'General Category 2', 'description': 'Second general category', 'code': 'GEN2'},
    {'name': 'Product Category - Electronics', 'description': 'Category for electronics products', 'code': 'PRODELEC'},
    {'name': 'Service Category - Consulting', 'description': 'Category for consulting services', 'code': 'SERCONS'},
]

# Define default GL Account Categories (Assets, Liabilities, etc.)
DEFAULT_GL_ACCOUNT_CATEGORIES = [
    {'description': 'Assets', 'type': 'ASSET'},
    {'description': 'Liabilities', 'type': 'LIABILITY'},
    {'description': 'Equity', 'type': 'EQUITY'},
    {'description': 'Revenue', 'type': 'REVENUE'},
    {'description': 'Expenses', 'type': 'EXPENSE'},
]

# Define default Chart of Accounts (Ledger Accounts)
# 'category_name' refers to the 'description' field in DEFAULT_GL_ACCOUNT_CATEGORIES
DEFAULT_CHART_OF_ACCOUNTS = [
    # Assets (Codes typically starting with 1xxxx)
    {'code': '10000', 'description': 'Cash', 'comments': 'Main operating cash account', 'category_name': 'Assets'},
    {'code': '10100', 'description': 'Petty Cash', 'comments': 'Small cash on hand for minor expenses', 'category_name': 'Assets'},
    {'code': '10200', 'description': 'Bank Account - Main', 'comments': 'Primary bank checking account', 'category_name': 'Assets'},
    {'code': '10300', 'description': 'Accounts Receivable', 'comments': 'Money owed to the company by customers', 'category_name': 'Assets'},
    {'code': '10400', 'description': 'Inventory / Stock', 'comments': 'Goods available for sale', 'category_name': 'Assets'},
    {'code': '10500', 'description': 'Prepaid Expenses', 'comments': 'Expenses paid in advance (e.g., rent, insurance)', 'category_name': 'Assets'},
    {'code': '11000', 'description': 'Fixed Assets - Equipment', 'comments': 'Long-term assets like machinery and computers', 'category_name': 'Assets'},
    {'code': '11100', 'description': 'Fixed Assets - Furniture & Fixtures', 'comments': 'Office furniture and installed fixtures', 'category_name': 'Assets'},
    {'code': '11200', 'description': 'Fixed Assets - Land', 'comments': 'Company-owned land', 'category_name': 'Assets'},
    {'code': '11300', 'description': 'Fixed Assets - Buildings', 'comments': 'Company-owned buildings/properties', 'category_name': 'Assets'},
    {'code': '11400', 'description': 'Fixed Assets - Vehicles', 'comments': 'Company vehicles for operations', 'category_name': 'Assets'},
    {'code': '19000', 'description': 'Accumulated Depreciation - Equipment', 'comments': 'Contra-asset account for equipment depreciation', 'category_name': 'Assets'},
    {'code': '19100', 'description': 'Accumulated Depreciation - Furniture', 'comments': 'Contra-asset account for furniture depreciation', 'category_name': 'Assets'},
    {'code': '19200', 'description': 'Accumulated Depreciation - Buildings', 'comments': 'Contra-asset account for building depreciation', 'category_name': 'Assets'},
    {'code': '19300', 'description': 'Accumulated Depreciation - Vehicles', 'comments': 'Contra-asset account for vehicle depreciation', 'category_name': 'Assets'},

    # Liabilities (Codes typically starting with 2xxxx)
    {'code': '20000', 'description': 'Accounts Payable', 'comments': 'Money owed by the company to suppliers', 'category_name': 'Liabilities'},
    {'code': '20100', 'description': 'Salaries Payable', 'comments': 'Salaries owed to employees', 'category_name': 'Liabilities'},
    {'code': '20200', 'description': 'Sales Tax Payable', 'comments': 'Sales tax collected but not yet remitted to authorities', 'category_name': 'Liabilities'},
    {'code': '20300', 'description': 'Unearned Revenue', 'comments': 'Payments received for goods/services not yet delivered', 'category_name': 'Liabilities'},
    {'code': '21000', 'description': 'Short-term Loans Payable', 'comments': 'Loans due within one year', 'category_name': 'Liabilities'},
    {'code': '21100', 'description': 'Long-term Loans Payable', 'comments': 'Loans due beyond one year', 'category_name': 'Liabilities'},
    {'code': '21200', 'description': 'Mortgage Payable', 'comments': 'Outstanding mortgage debt on company property', 'category_name': 'Liabilities'},

    # Equity (Codes typically starting with 3xxxx)
    {'code': '30000', 'description': 'Owner\'s Equity / Capital', 'comments': 'Initial investment by the owner(s)', 'category_name': 'Equity'},
    {'code': '30100', 'description': 'Owner\'s Drawings', 'comments': 'Personal withdrawals made by the owner(s)', 'category_name': 'Equity'},
    {'code': '30200', 'description': 'Retained Earnings', 'comments': 'Accumulated net income less dividends', 'category_name': 'Equity'},
    {'code': '30300', 'description': 'Common Stock / Share Capital', 'comments': 'Capital raised from issuing common shares', 'category_name': 'Equity'},
    {'code': '30400', 'description': 'Preferred Stock', 'comments': 'Capital raised from issuing preferred shares', 'category_name': 'Equity'},

    # Revenue (Codes typically starting with 4xxxx)
    {'code': '40000', 'description': 'Sales Revenue (Goods)', 'comments': 'Income from the sale of products', 'category_name': 'Revenue'},
    {'code': '40100', 'description': 'Service Revenue', 'comments': 'Income from services provided', 'category_name': 'Revenue'},
    {'code': '40200', 'description': 'Interest Income', 'comments': 'Income earned from interest on investments or loans', 'category_name': 'Revenue'},
    {'code': '40300', 'description': 'Rental Income', 'comments': 'Income earned from renting out property', 'category_name': 'Revenue'},
    {'code': '40400', 'description': 'Sales Returns & Allowances', 'comments': 'Contra-revenue for returned goods/allowances', 'category_name': 'Revenue'},

    # Expenses (Codes typically starting with 5xxxx)
    {'code': '50000', 'description': 'Cost of Goods Sold (COGS)', 'comments': 'Direct costs attributable to the production of goods sold', 'category_name': 'Expenses'},
    {'code': '50100', 'description': 'Salaries & Wages Expense', 'comments': 'Employee compensation expense', 'category_name': 'Expenses'},
    {'code': '50200', 'description': 'Rent Expense', 'comments': 'Cost of renting office or operational space', 'category_name': 'Expenses'},
    {'code': '50300', 'description': 'Utilities Expense', 'comments': 'Costs for electricity, water, gas, internet', 'category_name': 'Expenses'},
    {'code': '50400', 'description': 'Office Supplies Expense', 'comments': 'Cost of office supplies consumed', 'category_name': 'Expenses'},
    {'code': '50500', 'description': 'Marketing & Advertising Expense', 'comments': 'Costs related to promoting the business', 'category_name': 'Expenses'},
    {'code': '50600', 'description': 'Travel Expense', 'comments': 'Costs for business travel', 'category_name': 'Expenses'},
    {'code': '50700', 'description': 'Bank Service Charges', 'comments': 'Fees charged by financial institutions', 'category_name': 'Expenses'},
    {'code': '50800', 'description': 'Depreciation Expense', 'comments': 'Non-cash expense for asset wear and tear', 'category_name': 'Expenses'},
    {'code': '50900', 'description': 'Repairs & Maintenance Expense', 'comments': 'Costs for repairing and maintaining assets', 'category_name': 'Expenses'},
    {'code': '51000', 'description': 'Insurance Expense', 'comments': 'Cost of insurance premiums', 'category_name': 'Expenses'},
    {'code': '51100', 'description': 'Professional Fees Expense', 'comments': 'Legal, accounting, consulting fees', 'category_name': 'Expenses'},
    {'code': '51200', 'description': 'Telephone Expense', 'comments': 'Cost of communication services', 'category_name': 'Expenses'},
    {'code': '51300', 'description': 'Delivery & Freight Expense', 'comments': 'Costs related to shipping and delivery', 'category_name': 'Expenses'},
    {'code': '51400', 'description': 'Miscellaneous Expense', 'comments': 'Small, infrequent operating expenses', 'category_name': 'Expenses'},
]