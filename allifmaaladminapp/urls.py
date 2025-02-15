from django.urls import path
from . import views
app_name='allifmaaladminapp'
urlpatterns = [
    
path('Home/<str:allifusr>/<str:allifslug>/', views.adminappHome, name="adminappHome"),
path('Registered/System/Users/Subscribers/<str:allifusr>/<str:allifslug>/', views.adminappUsers, name="adminappUsers"),
path('User/Details/Admin/App/<str:pk>/<str:allifusr>/<str:allifslug>/', views.adminappUserDetails, name="adminappUserDetails"),

path('Customer/Contacts/Forms/Data/<str:allifusr>/<str:allifslug>/', views.adminCustomerContacts, name="adminCustomerContacts"),
path('Customer/Contact/Details/<str:pk>/<str:allifusr>/<str:allifslug>/', views.adminCustomerContactDetails, name="adminCustomerContactDetails"),
path('Delete/Customer/Contact/Information/<str:pk>/<str:allifusr>/<str:allifslug>/', views.adminDeleteCustomerContact, name="adminDeleteCustomerContact"),




]   
