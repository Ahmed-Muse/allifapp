from django.shortcuts import render
from allifmaalcommonapp.models import CommonExpensesModel,CommonSpacesModel,CommonSpaceUnitsModel

# Create your views here.
def realestateHome(request,*allifargs,**allifkwargs):
    try:
        title="Home : Real Estates"
        expenses=CommonExpensesModel.objects.all()   
        user_var=request.user
       
        user_role=user_var.allifmaal_admin
        user_is_supper=request.user.is_superuser
        user_is_supper=request.user.is_superuser
        user_company=request.user.company
        spaces=CommonSpacesModel.objects.all().count()
        space_units=CommonSpaceUnitsModel.objects.all().count()
        
       
        context={
            "title":title,
            "user_var":user_var,
            "user_is_supper":user_is_supper,
            "user_role":user_role,
            "expenses":expenses,
            "user_company":user_company,
            "spaces":spaces,
            "space_units":space_units,
           
        }
        return render(request,"allifmaalrealestateapp/home/home.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

def realestateDashboard(request,*allifargs,**allifkwargs):
    try:
        title="Dashboard : Hospitality"
        user_var=request.user
        user_role=user_var.allifmaal_admin
        user_is_supper=request.user.is_superuser
        context={
            "title":title,
            "user_var":user_var,
            "user_is_supper":user_is_supper,
        }
        return render(request,"allifmaalrealestateapp/dashboard/dashboard.html",context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

