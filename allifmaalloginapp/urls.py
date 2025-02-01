from django.urls import path
from . import views
app_name='allifmaalloginapp'
k='utax27hx35qlksdrjsh65/jsf46h5hhjds/'
urlpatterns = [
path('Allifmaal/New/User/Registration/Create/Page/utax27hx35qlksdrjsh65/jsf46h5hhjds/', 
     views.AllifmaalnewUserRegistration, name="AllifmaalnewUserRegistration"),
path('Allifmaal/User/Login/Page/View/u27hx35qlksdrjsh65/jsf46h5hhjdskjflks89/', 
     views.allifmaalUserLogin, name="allifmaalUserLogin"),
path('Allifmaal/User/Logout/Page/sjkksf27hx35qlksdrjsh65/jsf46h5s/', 
     views.allifmaaluserLogout, name="allifmaaluserLogout"),
path('Allifmaal/Edit/User/Details/Page/<slug:allifslug>/Update/utax86jhkj35qlksdrjsh65/jsf46h5hhjds/', 
     views.AllifmaalEditUserDetails, name="AllifmaalEditUserDetails"),
path('Allifmaal/Change/Your/User/Password/Page/re543utax27hx35ql65/jsf46h5hhjds/', 
     views.allifmaalChangeYourPassword, name="allifmaalChangeYourPassword"),
path('Allifmaal/Edit/User/Password/Page/<slug:allifslug>/Update/yrrh7hx35qlksdrjsh6ew/jsf46h5hhjds/', 
     views.allifmaalChangeUsersPassword, name="allifmaalChangeUsersPassword"),
path('Allifmaal/Change/User/To/Super/User/Permissions/Page/<slug:allifslug>/Update/pyuhx35qlksdr67jsh65/jsf46hrts/', 
     views.AllifmaalChangeUserToSupperuser, name="AllifmaalChangeUserToSupperuser"),
path('Delete/User/Selected/<slug:allifslug>/Completely/For/Ever/76fds7hx35qlksdrjsh65/jsf46kjksfs/', 
     views.allifmaalDeleteUser, name="allifmaalDeleteUser"),
path('Allifmaal/Forgot/Pass/User/Self/Change/Password/New/Password/Page/u7h7hx35qlksdrjsdsf5/jsf46h5hdfss/', 
     views.allifmaalForgotPassword, name="allifmaalForgotPassword"),

]   
