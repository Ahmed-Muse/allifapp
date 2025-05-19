from .models import CommonCompanyDetailsModel
from .sessions import Allifsessions

def allifmaalcommonappglobalVariables(request):
        user_var=0
        glbl_place_holder="This module is not yet configured"
        glblslug= "allifmaalfsjdfljengineeringjdjrwosdflimitedjfljj"
        main_sbscrbr_entity="Menu"
        open_link="Actions"
        user = getattr(request, 'user', None)  # Get 'user' if it exists, otherwise None
        is_authenticated = user is not None and user.is_authenticated
        
        if is_authenticated:
            user_var=request.user.customurlslug
            compslg=request.user.usercompany
            main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
            
            if main_sbscrbr_entity!=None:
                glblslug=main_sbscrbr_entity.companyslug
                sctr=str(main_sbscrbr_entity.sector)
               
                return {
                'user_var':user_var,
                'glblslug':glblslug,
                "sctr":sctr,
                "main_sbscrbr_entity":main_sbscrbr_entity,
                "open_link":open_link,
                "glbl_place_holder":glbl_place_holder,
                }
                
        return {
            'user_var':user_var,
            'glblslug':glblslug,
            "main_sbscrbr_entity":main_sbscrbr_entity,
            "open_link":open_link,
            "glbl_place_holder":glbl_place_holder,
            }
    
# create context process so that user sessions can be available on all pages
def allifUserSessions(request):
     
     # return the default data from the user session
    
     return {'usersessn':Allifsessions(request)}