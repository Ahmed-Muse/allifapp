from .models import CommonCompanyDetailsModel,CommonSectorsModel
from .sessions import Allifsessions

def allifmaalcommonappglobalVariables(request):
        user_var=0
        
        allifapp_logged_user_category=''
        cmpnysctr="Healthcare"
        glbl_place_holder="This module is not yet configured"
        user_var='kljfldsjkdjfslkewj'
        glblslug= "allifmaalfsjdfljengineeringjdjrwosdflimitedjfljj"
        main_sbscrbr_entity="Menu"
        open_link="Actions"
        user = getattr(request, 'user', None)  # Get 'user' if it exists, otherwise None
        is_authenticated = user is not None and user.is_authenticated
        
        if is_authenticated:
            allifapp_logged_user_category=request.user.user_category
       
            main_sbscrbr_entity=CommonCompanyDetailsModel.all_objects.filter(company=request.user.company).first()
            if main_sbscrbr_entity is not None:
                compslg=main_sbscrbr_entity.slgfld
            user_var=request.user.customurlslug
            
            if main_sbscrbr_entity!=None:
                glblslug=main_sbscrbr_entity.slgfld
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
                    'user_var':user_var,
                'glblslug':glblslug,
                "main_sbscrbr_entity":main_sbscrbr_entity,
                "open_link":open_link,
                "glbl_place_holder":glbl_place_holder,
                "cmpnysctr":cmpnysctr,
                "allifapp_logged_user_category":allifapp_logged_user_category,
                }
        else:
            
            return {
                'user_var':user_var,
                'glblslug':glblslug,
                "main_sbscrbr_entity":main_sbscrbr_entity,
                "open_link":open_link,
                "glbl_place_holder":glbl_place_holder,
                "cmpnysctr":cmpnysctr,
                "allifapp_logged_user_category":allifapp_logged_user_category,
                }
        

# create context process so that user sessions can be available on all pages
def allifUserSessions(request):
     
     # return the default data from the user session
    
     return {'usersessn':Allifsessions(request)}