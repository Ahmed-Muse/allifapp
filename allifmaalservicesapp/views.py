from django.shortcuts import render


# Create your views here.
def servicesHome(request,*allifargs,**allifkwargs):
    try:
        title="Home : Services"
        
        user_var=request.user
        user_role=user_var.allifmaal_admin
        user_is_supper=request.user.is_superuser
       
        context={
            "title":title,
            "user_var":user_var,
        }
        return render(request,"allifmaalservicesapp/home/home.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

def servicesDashboard(request,*allifargs,**allifkwargs):
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
        return render(request,"allifmaalservicesapp/dashboard/dashboard.html",context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)