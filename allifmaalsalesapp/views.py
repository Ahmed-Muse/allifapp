from django.shortcuts import render,HttpResponse,redirect
from allifmaalusersapp.models import User
from allifmaalcommonapp.forms import CommonAddTasksForm
from allifmaalcommonapp.models import CommonTasksModel,CommonCompanyDetailsModel,CommonEmployeesModel
from allifmaalcommonapp.allifutils import common_shared_data
from allifmaalcommonapp.decorators import subscriber_company_status,logged_in_user_must_have_profile
# Create your views here.

#@logged_in_user_must_have_profile
#@subscriber_company_status
def salesHome(request,*allifargs,**allifkwargs):
    title="Home : Sales & Distribution"
    try:
        user_is_supper=request.user.is_superuser
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_profile") is not None:
            context={"title":title,"user_is_supper":user_is_supper,}
            return render(request,"allifmaalsalesapp/home/home.html",context)
        else:
            return redirect('allifmaalcommonapp:commonAddStaffProfile',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

def salesDashboard(request,*allifargs,**allifkwargs):
    try:
        title="Dashboard : Distribution"
        
        user_var=request.user
        form=CommonAddTasksForm(request.POST or None)
        tasks=CommonTasksModel.objects.all()
        user_role=user_var.allifmaal_admin
        user_is_supper=request.user.is_superuser
        
        context={
            "title":title,
            "user_var":user_var,
            "form":form,
            "tasks":tasks,
            "user_is_supper":user_is_supper,
        }
        return render(request,"allifmaalsalesapp/dashboard/dashboard.html",context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)