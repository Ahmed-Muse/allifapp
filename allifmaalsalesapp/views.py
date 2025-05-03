from django.shortcuts import render,HttpResponse,redirect
from allifmaalusersapp.models import User
from allifmaalcommonapp.forms import CommonAddTasksForm
from allifmaalcommonapp.models import CommonTasksModel,CommonCompanyDetailsModel,CommonEmployeesModel

# Create your views here.
def salesHome(request,*allifargs,**allifkwargs):
    #try:
    title="Home : Distribution"
    user_var=request.user
    form=CommonAddTasksForm(request.POST or None)
    tasks=CommonTasksModel.objects.all()
    user_role=user_var.allifmaal_admin
    user_is_supper=request.user.is_superuser

    logged_in_user=request.user
    usrslg=request.user.customurlslug
    compslg=request.user.usercompany
    usernmeslg=User.objects.filter(customurlslug=usrslg).first()
    main_sbscrbr_entity=CommonCompanyDetailsModel.objects.filter(companyslug=compslg).first()
    logged_in_user_profile=CommonEmployeesModel.objects.filter(username=logged_in_user,company=main_sbscrbr_entity).first()
    logged_user_division=None
    logged_user_branch=None
    logged_user_department=None
    logged_user_profile_staffslg=None
    if logged_in_user_profile:
        logged_user_division=logged_in_user_profile.division
        logged_user_branch=logged_in_user_profile.branch
        logged_user_department=logged_in_user_profile.department
        logged_user_profile_staffslg=logged_in_user_profile.stffslug
        #return HttpResponse("mmmmm")
        context={
            "title":title,
            "user_var":user_var,
            "form":form,
            "tasks":tasks,
            "user_is_supper":user_is_supper,
        }
        return render(request,"allifmaalsalesapp/home/home.html",context)
    
        
    else:
        print("kkkkkkkkkkkkk")
        return redirect('allifmaalcommonapp:commonAddStaffProfile',allifusr=user_var,allifslug=compslg)
        #return HttpResponse("kkkkk")
        #pass

        context={
                "title":title,
                "user_var":user_var,
                "form":form,
                "tasks":tasks,
                "user_is_supper":user_is_supper,
            }
        return render(request,"allifmaalsalesapp/home/home.html",context)
    
    logged_in_user_has_universal_access=request.user.universal_access
    logged_in_user_has_divisional_access=request.user.divisional_access
    logged_in_user_has_branches_access=request.user.branches_access
    logged_in_user_has_departmental_access=request.user.departmental_access

    logged_in_user_has_universal_delete=request.user.universal_delete
    logged_in_user_has_divisional_delete=request.user.divisional_delete
    logged_in_user_has_branches_delete=request.user.branches_delete
    logged_in_user_has_departmental_delete=request.user.departmental_delete
    
    if logged_in_user_profile==None:
        
        return redirect('allifmaalcommonapp:commonAddStaffProfile',allifusr=user_var,allifslug=compslg)
                

        pass
    else:
        pass

    compslg=request.user.usercompany
    if user_is_supper==True:
        
        context={
            "title":title,
            "user_var":user_var,
            "form":form,
            "tasks":tasks,
            "user_is_supper":user_is_supper,
        }
        return render(request,"allifmaalsalesapp/home/home.html",context)
    else:

    
        context={
            "title":title,
            "user_var":user_var,
            "form":form,
            "tasks":tasks,
        }
        return render(request,"allifmaalsalesapp/home/home.html",context)
    #except Exception as ex:
        #error_context={'error_message': ex,}
        #return render(request,'allifmaalcommonapp/error/error.html',error_context)

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