from .models import CommonCompanyDetailsModel
def allifmaalcommonappglobalVariables(request):
        user_var = 0
        glblslug= "allifmaalfsjdfljengineeringjdjrwosdflimitedjfljj"

        if request.user.is_authenticated:
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
                }
                
        return {
            'user_var':user_var,
            'glblslug':glblslug,
            }
    
