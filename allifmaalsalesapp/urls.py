from django.urls import path
from . import views
app_name='allifmaalsalesapp'
urlpatterns = [
    
path('Sales/Home/<str:allifusr>/<str:allifslug>/', views.salesHome, name="salesHome"),

]  