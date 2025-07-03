from .models import CommonCompanyDetailsModel,CommonSectorsModel
from .sessions import Allifsessions

def allifmaalcommonappglobalVariables(request):
        user_var=0
        
        allifapp_logged_user_category=''
        cmpnysctr="Healthcare"
        glbl_place_holder="This module is not yet configured"
        glblslug= "allifmaalfsjdfljengineeringjdjrwosdflimitedjfljj"
        main_sbscrbr_entity="Menu"
        open_link="Actions"
        user = getattr(request, 'user', None)  # Get 'user' if it exists, otherwise None
        is_authenticated = user is not None and user.is_authenticated
        
        if is_authenticated:
            allifapp_logged_user_category=request.user.user_category
            user_var=request.user.customurlslug
           
            compslg=request.user.usercompany
            main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
            
            if main_sbscrbr_entity!=None:
                glblslug=main_sbscrbr_entity.companyslug
                cmpnysctr=str(main_sbscrbr_entity.sector)
                
                return {
                'user_var':user_var,
                'glblslug':glblslug,
                "cmpnysctr":cmpnysctr,
                "main_sbscrbr_entity":main_sbscrbr_entity,
                "open_link":open_link,
                "glbl_place_holder":glbl_place_holder,
                "allifapp_logged_user_category":allifapp_logged_user_category,
                }
            else:
                return {
                    "cmpnysctr":cmpnysctr,
                }
        return {
            'user_var':user_var,
            'glblslug':glblslug,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            "open_link":open_link,
            "glbl_place_holder":glbl_place_holder,
            "cmpnysctr":cmpnysctr,
            "allifapp_logged_user_category":allifapp_logged_user_category,
            }

"""
def allifmaalcommonappglobalVariables(request):
    # Initialize all variables with their absolute default/fallback values
    # These will be used if no specific logic overrides them.
    user_var = 0 # Consider making this None or "" for unauthenticated users
    cmpnysctr = "General" # Initial default sector (as a string)
    glbl_place_holder = "This module is not yet configured"
    glblslug = "default-company-slug" # More descriptive default
    main_sbscrbr_entity = None # Should be a model instance, not "Menu" string
    open_link = "Actions" # This seems like a constant, could be handled differently

    user = getattr(request, 'user', None)
    is_authenticated = user is not None and user.is_authenticated

    if is_authenticated:
        user_var = request.user.customurlslug

        # Assuming request.user.usercompany directly gives the companyslug string
        # If it's a ForeignKey to CommonCompanyDetailsModel, adjust accordingly
        compslg = request.user.usercompany 

        # Attempt to get the main company entity
        # Use .first() as it might not exist if compslg is bad/missing
        current_company_entity = CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()

        if current_company_entity:
            glblslug = current_company_entity.companyslug
            
            # Convert sector to string if it's a model instance
            if isinstance(current_company_entity.sector, CommonSectorsModel):
                cmpnysctr = str(current_company_entity.sector)
            elif isinstance(current_company_entity.sector, str):
                cmpnysctr = current_company_entity.sector
            else:
                cmpnysctr = "General" # Fallback if sector type is unexpected

            main_sbscrbr_entity = current_company_entity # Assign the model instance

        else:
            # If authenticated but no company found, set appropriate defaults
            if request.user.is_superuser:
                cmpnysctr = "Admin"
                glblslug = "admin-slug"
            else:
                cmpnysctr = "General"
                glblslug = "no-company-slug"
            main_sbscrbr_entity = None # No entity found

    # Consolidated return statement
    return {
        'user_var': user_var,
        'glblslug': glblslug,
        "cmpnysctr": cmpnysctr, # <--- ALWAYS INCLUDED HERE
        "main_sbscrbr_entity": main_sbscrbr_entity,
        "open_link": open_link,
        "glbl_place_holder": glbl_place_holder,
    }
"""
# create context process so that user sessions can be available on all pages
def allifUserSessions(request):
     
     # return the default data from the user session
    
     return {'usersessn':Allifsessions(request)}