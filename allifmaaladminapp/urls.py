from django.urls import path
from . import views
app_name='allifmaaladminapp'
urlpatterns = [
    
path('Home/<str:allifusr>/<str:allifslug>/', views.adminappHome, name="adminappHome"),
path('Registered/System/Users/Subscribers/<str:allifusr>/<str:allifslug>/', views.adminappUsers, name="adminappUsers"),
path('User/Details/Admin/App/<str:pk>/<str:allifusr>/<str:allifslug>/', views.adminappUserDetails, name="adminappUserDetails"),


]   
