
from django.shortcuts import render
def logisticsHome(request,*allifargs,**allifkwargs):
    try:
        title="Home : Logistics"
        
        user_var=request.user
      
        user_role=user_var.allifmaal_admin
        user_is_supper=request.user.is_superuser
       
        context={
            "title":title,
            "user_var":user_var,
           
        }
        return render(request,"allifmaallogisticsapp/home/home.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

def logisticsDashboard(request,*allifargs,**allifkwargs):
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
        return render(request,"allifmaallogisticsapp/dashboard/dashboard.html",context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)