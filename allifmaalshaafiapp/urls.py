from django.urls import path
from . import views
app_name='allifmaalshaafiapp'
urlpatterns = [
    
path('Healthcare/Home/<str:allifusr>/<str:allifslug>/', views.shaafiHome, name="shaafiHome"),
path('Healthcare/Dashboard/<str:allifusr>/<str:allifslug>/', views.shaafiDashboard, name="shaafiDashboard"),

]  