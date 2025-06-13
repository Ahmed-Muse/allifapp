
from django.shortcuts import render,redirect
from allifmaalcommonapp.allifutils import common_shared_data
from allifmaalcommonapp.decorators import subscriber_company_status,logged_in_user_must_have_profile
from allifmaalcommonapp.decorators import *
from .models import *
from .forms import *
from django.db.models import Q
def ilmHome(request,*allifargs,**allifkwargs):
    title="Home : Healthcare"
    try:
        user_is_supper=request.user.is_superuser
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_profile") is not None:
            context={"title":title,"user_is_supper":user_is_supper,}
            return render(request,"allifmaalilmapp/home/home.html",context)
        else:
            return redirect('allifmaalcommonapp:commonAddStaffProfile',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
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



##################################### EDUCATIONS... ###################
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonForms(request,*allifargs,**allifkwargs):
    try:
        title="Forms And Faculties"
        allif_data=common_shared_data(request)
        allifqueryset=[]
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonFormsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonFormsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonFormsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonFormsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]

        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/education/forms/forms.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddForm(request,*allifargs,**allifkwargs):
    title="Forms, Faculties Registration"
    try:
        allif_data=common_shared_data(request)
        form=CommonFormsAddForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonFormsAddForm(allif_data.get("main_sbscrbr_entity"),request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonForms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonFormsAddForm(allif_data.get("main_sbscrbr_entity"))
       
        context={
            "form":form,"title":title,}
        return render(request,'allifmaalcommonapp/education/forms/add-form.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditForm(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Update Forms And Faculties Details"
        allifquery_update=CommonFormsModel.objects.filter(id=pk).first()
        form=CommonFormsAddForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=CommonFormsAddForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonForms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonFormsAddForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
         
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalcommonapp/education/forms/add-form.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def commonWantToDeleteForm(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonFormsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/education/forms/form-delete-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)       

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_has_departmental_delete
def commonDeleteForm(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonFormsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonForms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonFormDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Form/Faculty Details"
        allifquery=CommonFormsModel.objects.filter(id=pk).first()
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/education/forms/forms-details.html',context)
        
    
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonFormSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonFormsModel.objects.filter((Q(name__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]
        context={
        "title":title,
        "allifsearch":allifsearch,
        "searched_data":searched_data,
    }
        return render(request,'allifmaalcommonapp/education/forms/forms.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#######################################3 classes ###############################3
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonClasses(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Classes"
        allifqueryset=[]
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=CommonClassesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=CommonClassesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=CommonClassesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=CommonClassesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
       
     
        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalcommonapp/education/classes/classes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def commonAddClass(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Add New Class"
        form=CommonClassesAddForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=CommonClassesAddForm(allif_data.get("main_sbscrbr_entity"), request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.company=allif_data.get("main_sbscrbr_entity")
                obj.division=allif_data.get("logged_user_division")
                obj.branch=allif_data.get("logged_user_branch")
                obj.department=allif_data.get("logged_user_department")
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonClasses',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
        else:
            form=CommonClassesAddForm(allif_data.get("main_sbscrbr_entity"))

        context={"form":form,"title":title,}
        return render(request,'allifmaalcommonapp/education/classes/add-class.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def commonEditClass(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Class Details"
        allif_data=common_shared_data(request)
        allifquery_update=CommonClassesModel.objects.filter(id=pk).first()
        form=CommonClassesAddForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery_update)
        if request.method=='POST':
            form=CommonClassesAddForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=allifquery_update)
            if form.is_valid():
                obj=form.save(commit=False)
                obj.owner=allif_data.get("usernmeslg")
                obj.save()
                return redirect('allifmaalcommonapp:commonClasses',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
                 
            else:
                error_message=form.errors
                allifcontext={"error_message":error_message,"title":title,}
                return render(request,'allifmaalcommonapp/error/form-error.html',allifcontext)
               
        else:
            form=CommonClassesAddForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery_update)

        context={"title":title,"form":form,"allifquery_update":allifquery_update}
        return render(request,'allifmaalcommonapp/education/classes/add-class.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
@logged_in_user_has_departmental_delete
def commonDeleteClass(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        CommonClassesModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonClasses',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonClassDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Class Details"
        allifquery=CommonClassesModel.objects.filter(id=pk).first()
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalcommonapp/education/classes/class-details.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def commonClassSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=CommonClassesModel.objects.filter((Q(name__icontains=allifsearch)|Q(comments__icontains=allifsearch)|Q(form__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
          
        }
        return render(request,'allifmaalcommonapp/education/classes/classes.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_has_departmental_delete
def commonWantToDeleteClass(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=CommonClassesModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalcommonapp/education/classes/class-delete-confirm.html',context)

    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)       

