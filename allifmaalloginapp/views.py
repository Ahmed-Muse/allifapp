from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout#for login and logout- and authentication

#@permission_required("allifmaalloginapp:allifmaalUserLogin")
def AllifmaalnewUserRegistration(request):
    try:
        title="New User Registration"
        if request.user.is_authenticated:
            return redirect("allifmaalcommonapp:CommonDecisionPoint")
        else:
            form=AllifmaalCreateUserForm()
            if request.method=='POST':
                form=AllifmaalCreateUserForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.save()
            
                    newUser=AllifmaalUsersModel.objects.filter(email=obj).first()
                    if newUser!=None:
                        secret_key=newUser.customuserslug
                        context={"title":title,"form":form,"secret_key":secret_key,}
                        return render(request,"allifmaalloginapp/users/allifuserkey.html",context)
                    
                    else:
                        messages.info(request,f'User does not exist')
                        return redirect('allifmaalusersapp:newUserRegistration')
                    
                else:
                    messages.info(request,f'Sorry email is likely taken, or passwords not match')
        context={
            "form":form,
            "title":title,
        }
        return render(request,"allifmaalloginapp/users/registration.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalloginapp/error/error.html',error_context)
    
def allifmaalUserLogin(request):
    try:
        title="Allifmaal User Login Page"
        if request.user.is_authenticated:
            return redirect("allifmaalcommonapp:CommonDecisionPoint")
        
        else:
            form=AllifmaalUserLoginForm()
            if request.method=='POST':
                username=request.POST.get('username')
                password=request.POST.get('password')
                user=authenticate(request,username=username,password=password)
                if user is not None:#if there is an authenticated user
                    login(request, user)
                    return redirect("allifmaalcommonapp:CommonDecisionPoint")
                else:
                    messages.info(request,'Dear '+username + ', Your username or password is incorrect ! ')
                    form=AllifmaalUserLoginForm(request)
        context={"form":form,
            "title":title,
            }
        return render(request,"allifmaalloginapp/users/login.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalloginapp/error/error.html',error_context)

def allifmaaluserLogout(request):
    try:
        if request.user.is_authenticated:
            logout(request)#logs user out
            messages.success(request,"Successfully logged out ")
            return redirect('allifmaalloginapp:allifmaalUserLogin')
        else:
            return redirect('allifmaalloginapp:allifmaalUserLogin')
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalloginapp/error/error.html',error_context)


def AllifmaalEditUserDetails(request,allifslug):
    try:
        if request.user.is_authenticated:
            user=AllifmaalUsersModel.objects.filter(customuserslug=allifslug).first()
            title="Update User Details"
            form=AllifmaalUpdateCustomUserForm(instance=user)
            if request.method=='POST':
                form=AllifmaalUpdateCustomUserForm(request.POST or None, instance=user)
                if form.is_valid():
                    form.save()
                    return redirect('allifmaalcommonapp:CommonDecisionPoint')
            context={"title":title,"form":form,}
            return render(request,"allifmaalloginapp/users/update_user.html",context)
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalloginapp/error/error.html',error_context)
   
def allifmaalChangeYourPassword(request):
    try:
        title="Change Your User Password"
        if request.user.is_authenticated:
            logged_user=request.user
            if request.method=='POST':
                pass1=request.POST.get('password1')
                pass2=request.POST.get('password2')
                if pass2==pass1:
                    user=AllifmaalUsersModel.objects.filter(email=logged_user).first()
                    user.set_password(str(pass1))
                    user.save()
                    logout(request)
                    return redirect('allifmaalloginapp:allifmaalUserLogin')
                else:
                    messages.info(request,'Sorry the two passwords are not the same')
                    return redirect('allifmaalloginapp:allifmaalChangeYourPassword')
                    
            context={"title":title,"logged_user":logged_user,}
            return render(request,"allifmaalloginapp/users/change_password.html",context)
        else:
            return redirect('allifmaalloginapp:allifmaalUserLogin')
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalloginapp/error/error.html',error_context)

def allifmaalChangeUsersPassword(request,allifslug):
    try:
        selecteduser=AllifmaalUsersModel.objects.filter(customuserslug=allifslug).first()
        title="Change User Password"
        if request.user.is_authenticated:
            if request.method=='POST':
                pass1=request.POST.get('password1')
                pass2=request.POST.get('password2')
                if pass2==pass1:
                    user=AllifmaalUsersModel.objects.filter(email=selecteduser).first()
                    user.set_password(str(pass1))
                    user.save()
                    return redirect('allifmaalcommonapp:CommonDecisionPoint')
                else:
                    messages.info(request,'Sorry the two passwords are not the same')
                    return redirect('allifmaalloginapp:allifmaalChangeUsersPassword',allifslug=selecteduser.customuserslug)
                    
            context={"title":title,"selecteduser":selecteduser,}
            return render(request,"allifmaalloginapp/users/changeuserpassbyadmin.html",context)
        else:
            return redirect('allifmaalloginapp:allifmaalUserLogin')
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalloginapp/error/error.html',error_context)

def AllifmaalChangeUserToSupperuser(request,allifslug):
    try:
        if request.user.is_authenticated:
            user=AllifmaalUsersModel.objects.filter(customuserslug=allifslug).first()
            if user.is_staff==True and user.is_superuser==True:
                user.is_staff=False
                user.is_superuser=False
                user.is_active=True
            else:
                user.is_staff=True
                user.is_superuser=True
                user.is_active=True
            user.save()
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
        else:
            return redirect('allifmaalcommonapp:CommonDecisionPoint')
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalloginapp/error/error.html',error_context)

def allifmaalDeleteUser(request,allifslug):
    try:
        if request.user.is_authenticated:
            AllifmaalUsersModel.objects.filter(customuserslug=allifslug).first().delete()
            return redirect('aallifmaalcommonapp:CommonDecisionPoint')
        else:
            return redirect('allifmaalloginapp:allifmaalUserLogin')
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalloginapp/error/error.html',error_context)

def allifmaalForgotPassword(request):#this requires the user to remember their email and secret key
    try:
        title="Forgot Your Password?"
        if request.method=='POST':
            accessemail=request.POST.get('email')
            secretkey=request.POST.get('secretkey')
            pass1=request.POST.get('password1')
            pass2=request.POST.get('password2')
            usremail=AllifmaalUsersModel.objects.filter(email=accessemail,customuserslug=secretkey).first()
            if usremail is not None:
                if pass2==pass1:
                    usremail.set_password(str(pass1))
                    usremail.save()
                    messages.success(request, 'Your password was successfully changed!')
                    return redirect('allifmaalloginapp:allifmaalForgotPassword')
                else:
                    messages.info(request,'Sorry the two passwords are not the same')
                    return redirect('allifmaalloginapp:allifmaalForgotPassword')
                
            else:
                messages.info(request,'Your email or secret key is incorrect!')
                return redirect('allifmaalloginapp:allifmaalForgotPassword')
            
        return render(request,"allifmaalloginapp/users/forgotpassword.html",{"title":title,})
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalloginapp/error/error.html',error_context)