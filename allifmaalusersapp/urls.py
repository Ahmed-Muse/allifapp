from django.urls import path
from . import views
app_name='allifmaalusersapp'
urlpatterns = [
path('New/User/Registration/Create/Page/', views.newUserRegistration, name="newUserRegistration"),
path('User/Login/Page/', views.userLoginPage, name="userLoginPage"),
path('User/Logout/Page/', views.userLogoutPage, name="userLogoutPage"),
path('Edit/User/Details/Page/<slug:allifslug>/Update/', views.editUserDetailsByAdmin, name="editUserDetailsByAdmin"),
path('Change/Your/User/Password/Page/', views.changeYourUserPassword, name="changeYourUserPassword"),
path('User/Admin/Change/User/Password/New/Password/Page/<slug:allifslug>/', views.changeUserPasswordByAdmin, name="changeUserPasswordByAdmin"),
path('Change/User/To/Superuser/By/Admin/<slug:allifslug>/', views.changeUserToSupperuserByAdmin, name="changeUserToSupperuserByAdmin"),
path('Delete/User/Selected/By/Admin/Permntly/<slug:allifslug>/Completely/For/Ever/', views.DeleteUserByAdmin, name="DeleteUserByAdmin"),
path('User/Forgot/Own/Change/Password/New/Password/Page/', views.userForgotPassowrd, name="userForgotPassowrd"),

]   
