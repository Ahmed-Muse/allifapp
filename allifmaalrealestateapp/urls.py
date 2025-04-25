from django.urls import path
from . import views
app_name='allifmaalrealestateapp'
urlpatterns = [
    
path('Real/Estates/Home/<str:allifusr>/<str:allifslug>/', views.realestateHome, name="realestateHome"),
path('Real/Estates/Dashboard/<str:allifusr>/<str:allifslug>/', views.realestateDashboard, name="realestateDashboard"),

]  