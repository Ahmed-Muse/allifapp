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
path('Block/Unblock/Company/Entity/<str:pk>/<str:allifusr>/<str:allifslug>/', views.adminBlockUnblockEntity, name="adminBlockUnblockEntity"),



############################3 BELOW ARE FOR TESTING PURPOSES ###############################3
path('UI1/Home/<str:allifusr>/<str:allifslug>/', views.ui1, name="ui1"),
path('UI2/Home/<str:allifusr>/<str:allifslug>/', views.ui2, name="ui2"),
path('UI3/Home/<str:allifusr>/<str:allifslug>/', views.ui3, name="ui3"),
path('UI4/Home/<str:allifusr>/<str:allifslug>/', views.ui4, name="ui4"),
path('UI6/Home/<str:allifusr>/<str:allifslug>/', views.ui6, name="ui6"),
path('UI7/Home/<str:allifusr>/<str:allifslug>/', views.ui7, name="ui7"),
path('UI8/Home/<str:allifusr>/<str:allifslug>/', views.ui8, name="ui8"),
path('add/dynamic_form_view/', views.dynamic_form_view, name='dynamic_form_view'),

path('products/', views.product_list, name='product_list'),

]   
