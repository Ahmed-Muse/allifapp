
from django.shortcuts import render
def ilmHome(request,*allifargs,**allifkwargs):
    try:
        title="Home : Education"
        
        user_var=request.user
      
        user_role=user_var.allifmaal_admin
        user_is_supper=request.user.is_superuser
       
        context={
            "title":title,
            "user_var":user_var,
            
        }
        return render(request,"allifmaalilmapp/home/home.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
def ilmDashboard(request,*allifargs,**allifkwargs):
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
        return render(request,"allifmaalilmapp/dashboard/dashboard.html",context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    