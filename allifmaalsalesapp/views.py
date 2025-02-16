from django.shortcuts import render
from allifmaalusersapp.models import User
from allifmaalcommonapp.forms import CommonAddTasksForm
from allifmaalcommonapp.models import CommonTasksModel

# Create your views here.
def salesHome(request,*allifargs,**allifkwargs):
    try:
        title="Home"
        
        user_var=request.user
        form=CommonAddTasksForm(request.POST or None)
        tasks=CommonTasksModel.objects.all()
        user_role=user_var.allifmaal_admin
        user_is_supper=request.user.is_superuser
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
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)