from django.urls import path
from . import views
app_name='allifmaalhotelsapp'
urlpatterns = [
    
path('Hotels/Home/<str:allifusr>/<str:allifslug>/', views.hotelsHome, name="hotelsHome"),
path('Hotels/Dashboard/<str:allifusr>/<str:allifslug>/', views.hospitalityDashboard, name="hospitalityDashboard"),


]  