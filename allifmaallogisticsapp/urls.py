from django.urls import path
from . import views

app_name='allifmaallogisticsapp'
urlpatterns = [
path('Logistics/Home/<str:allifusr>/<str:allifslug>/', views.logisticsHome, name="logisticsHome"),
path('Logistics/Dashboard/<str:allifusr>/<str:allifslug>/', views.logisticsDashboard, name="logisticsDashboard"),

]  



