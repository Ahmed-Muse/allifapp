from django.urls import path
from . import views
app_name='allifmaalservicesapp'
urlpatterns = [
    
path('Services/Home/<str:allifusr>/<str:allifslug>/', views.servicesHome, name="servicesHome"),
path('Services/Dashboard/<str:allifusr>/<str:allifslug>/', views.servicesDashboard, name="servicesDashboard"),

]  