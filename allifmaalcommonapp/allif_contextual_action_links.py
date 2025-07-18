# myerpapp/configs/contextual_actions.py

allif_sector_contextual_action_require_pk_links= {
    'Healthcare': [
    {'name': 'AddTriageData', 'url_name': 'allifmaalshaafiapp:AddTriageData', 'requires_pk': True},
    {'name': 'addDoctorAssessment', 'url_name': 'allifmaalshaafiapp:addDoctorAssessment', 'requires_pk': True},
    {'name': 'common_currency_pdf', 'url_name': 'allifmaalcommonapp:common_currency_pdf', 'requires_pk': True},
    {'name': 'commonWantToDeleteCurrency', 'url_name': 'allifmaalcommonapp:commonWantToDeleteCurrency', 'requires_pk': True},
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