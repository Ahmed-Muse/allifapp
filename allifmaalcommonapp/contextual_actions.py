# myerpapp/configs/contextual_actions.py

SECTOR_CONTEXTUAL_ACTIONS = {
    'Healthcare': [
        {'name': 'AddTriageData', 'url_name': 'allifmaalshaafiapp:AddTriageData', 'requires_pk': True},
        {'name': 'commonAddTransactionDetails', 'url_name': 'allifmaalcommonapp:commonAddTransactionDetails', 'requires_pk': True},
        {'name': 'commonSpaceBookings', 'url_name': 'allifmaalcommonapp:commonSpaceBookings', 'requires_pk': True},
        
        
    ],
    'Education': [
         {'name': 'AddExam', 'url_name': 'allifmaalilmapp:AddExam', 'requires_pk': True},
    ],
    'Real Estate': [
    ],
    # You can also add a 'Default' key here if you want actions that appear
    # when no specific sector matches, or for a 'General' sector.
} # <--- REMOVE THE TRAILING COMMA HERE!