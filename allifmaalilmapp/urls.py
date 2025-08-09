from django.urls import path
from . import views
app_name='allifmaalilmapp'
urlpatterns = [
path('Education/Home/<str:allifusr>/<str:allifslug>/', views.ilmHome, name="ilmHome"),
path('Education/Dashboard/<str:allifusr>/<str:allifslug>/', views.ilmDashboard, name="ilmDashboard"),

]  