
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
def examinations(request,*allifargs,**allifkwargs):
    try:
        title="Forms And Faculties"
        allif_data=common_shared_data(request)
        allifqueryset=[]
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=ExaminationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=ExaminationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=ExaminationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=ExaminationsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]

        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalilmapp/exams/exams.html',context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def addExamDetails(request,pk,*allifargs,**allifkwargs):
    title="Forms, Faculties Registration"
    try:
        allif_data=common_shared_data(request)
        allifquery=CommonTransactionsModel.objects.filter(id=pk).first()
        form=AddExamDetailsForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=AddExamDetailsForm(allif_data.get("main_sbscrbr_entity"),request.POST)
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
            form=AddExamDetailsForm(allif_data.get("main_sbscrbr_entity"))
       
        context={
            "form":form,"title":title,
            "allifquery":allifquery,
            
            }
        return render(request,'allifmaalilmapp/exams/add_exam.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def editExamDetails(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Update Forms And Faculties Details"
        allifquery_update=ExaminationsModel.objects.filter(id=pk).first()
        form=AddExamDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
        if request.method=='POST':
            form=AddExamDetailsForm(allif_data.get("main_sbscrbr_entity"),request.POST or None, instance=allifquery_update)
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
            form=AddExamDetailsForm(allif_data.get("main_sbscrbr_entity"),instance=allifquery_update)
         
        context={"title":title,"form":form,"allifquery_update":allifquery_update,}
        return render(request,'allifmaalilmapp/exams/add_exam.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
def wantToDeleteExam(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=ExaminationsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalilmapp/exams/delete_exam_confirm.html',context)
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)       

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
@logged_in_user_has_departmental_delete
def deleteExam(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        ExaminationsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonForms',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def examDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Form/Faculty Details"
        allifquery=ExaminationsModel.objects.filter(id=pk).first()
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalilmapp/exams/exam_details.html',context)
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def examSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=ExaminationsModel.objects.filter((Q(name__icontains=allifsearch)|Q(comments__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
        else:
            searched_data=[]
        context={
        "title":title,
        "allifsearch":allifsearch,
        "searched_data":searched_data,}
        return render(request,'allifmaalilmapp/exams/exams.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

#######################################3 classes ###############################3
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def examResults(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Classes"
        allifqueryset=[]
        if allif_data.get("logged_in_user_has_universal_access")==True:
            allifqueryset=ExamResultsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"))
        elif allif_data.get("logged_in_user_has_divisional_access")==True:
            allifqueryset=ExamResultsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"))
        elif allif_data.get("logged_in_user_has_branches_access")==True:
            allifqueryset=ExamResultsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"))
        elif allif_data.get("logged_in_user_has_departmental_access")==True:
            allifqueryset=ExamResultsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
        else:
            allifqueryset=[]
       
     
        context={
            "title":title,
            "allifqueryset":allifqueryset,
        }
        return render(request,'allifmaalilmapp/exams/results/results.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
       
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_add
def addExamResult(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Add New Class"
        form=AddExamResultsForm(allif_data.get("main_sbscrbr_entity"))
        if request.method=='POST':
            form=AddExamResultsForm(allif_data.get("main_sbscrbr_entity"), request.POST)
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
            form=AddExamResultsForm(allif_data.get("main_sbscrbr_entity"))

        context={"form":form,"title":title,}
        return render(request,'allifmaalilmapp/exams/results/add_result.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_edit
def editExamResult(request,pk,*allifargs,**allifkwargs):
    try:
        title="Update Class Details"
        allif_data=common_shared_data(request)
        allifquery_update=ExamResultsModel.objects.filter(id=pk).first()
        form=AddExamResultsForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery_update)
        if request.method=='POST':
            form=AddExamResultsForm(allif_data.get("main_sbscrbr_entity"), request.POST, instance=allifquery_update)
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
            form=AddExamResultsForm(allif_data.get("main_sbscrbr_entity"), instance=allifquery_update)

        context={"title":title,"form":form,"allifquery_update":allifquery_update}
        return render(request,'allifmaalilmapp/exams/results/add_result.html',context)
     
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
      
@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_delete
@logged_in_user_has_departmental_delete
def deleteExamResult(request,pk,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        ExamResultsModel.objects.filter(id=pk).first().delete()
        return redirect('allifmaalcommonapp:commonClasses',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
      
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def examResultDetails(request,pk,*allifargs,**allifkwargs):
    try:
        title="Class Details"
        allifquery=ExamResultsModel.objects.filter(id=pk).first()
        context={
            "allifquery":allifquery,
            "title":title,
        }
        return render(request,'allifmaalilmapp/exams/results/result_details.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_can_view
def examResultSearch(request,*allifargs,**allifkwargs):
    try:
        title="Search Results"
        allif_data=common_shared_data(request)
        if request.method=='POST':
            allifsearch=request.POST.get('allifsearchcommonfieldname')
            searched_data=ExamResultsModel.objects.filter((Q(name__icontains=allifsearch)|Q(comments__icontains=allifsearch)|Q(form__name__icontains=allifsearch)) & Q(company=allif_data.get("main_sbscrbr_entity")))
           
            context={
           
            "title":title,
            "allifsearch":allifsearch,
            "searched_data":searched_data,
          
        }
        return render(request,'allifmaalilmapp/exams/results/results.html',context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

@logged_in_user_must_have_profile
@subscriber_company_status
@logged_in_user_has_departmental_delete
def wantToDeleteExamResult(request,pk,*allifargs,**allifkwargs):
    try:
        allifquery=ExamResultsModel.objects.filter(id=pk).first()
        title="Are you sure to delete?"
        context={
        "allifquery":allifquery,
        "title":title,
        }
        return render(request,'allifmaalilmapp/exams/results/delete_result_confirm.html',context)
       
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)       

