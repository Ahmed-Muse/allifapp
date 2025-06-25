# your_app_name/configs/navigation_links.py

# Define general links accessible to all sectors
allifmaal_general_links = [
    {'name': 'commonHome', 'url_name': 'allifmaalcommonapp:commonHome'},
    {'name': 'commonTransactions', 'url_name': 'allifmaalcommonapp:commonTransactions'},
    # Add more general links here
    {'name': 'commonCodes', 'url_name': 'allifmaalcommonapp:commonCodes'},
   
]

# Define sector-specific links
# Each list holds dictionaries for links specific to that sector
# Use the exact string representation of your company sector (e.g., 'Healthcare', 'Education')

allifmaal_sector_specific_links= {
    'Healthcare': [
        {'name': 'ShaafiHome', 'url_name': 'allifmaalshaafiapp:shaafiHome'}, # Example URL name
        {'name': 'triageData', 'url_name': 'allifmaalshaafiapp:triageData'},
      
    ],
    'Education': [
        {'name': 'Exams', 'url_name': 'allifmaalilmapp:examinations'},
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