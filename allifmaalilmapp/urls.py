from django.urls import path
from . import views
app_name='allifmaalilmapp'
urlpatterns = [
    
path('Education/Home/<str:allifusr>/<str:allifslug>/', views.ilmHome, name="ilmHome"),
path('Education/Dashboard/<str:allifusr>/<str:allifslug>/', views.ilmDashboard, name="ilmDashboard"),

path('Forms/<str:allifusr>/<str:allifslug>/', views.commonForms, name="commonForms"),
path('Add/New/Form/<str:allifusr>/<str:allifslug>/', views.commonAddForm, name="commonAddForm"),
path('Edit/Form/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditForm, name="commonEditForm"),
path('Delete/Form/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteForm, name="commonDeleteForm"),
path('View/Form/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonFormDetails, name="commonFormDetails"),
path('Search/Forms/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonFormSearch, name="commonFormSearch"),
path('Want/To/Delete/Form/Faculty/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteForm, name="commonWantToDeleteForm"),

################################3333 classes #########################################################
path('Classes/<str:allifusr>/<str:allifslug>/', views.commonClasses, name="commonClasses"),
path('Add/New/Class/<str:allifusr>/<str:allifslug>/', views.commonAddClass, name="commonAddClass"),
path('Edit/Class/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonEditClass, name="commonEditClass"),
path('Delete/Class/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonDeleteClass, name="commonDeleteClass"),
path('Search/Classes/<str:allifusr>/<str:allifslug>/Shareholders/', views.commonClassSearch, name="commonClassSearch"),
path('View/Class/<str:pk>/<str:allifusr>/<str:allifslug>/Details/', views.commonClassDetails, name="commonClassDetails"),
path('Want/To/Delete/This/Class/<str:pk>/<str:allifusr>/<str:allifslug>/', views.commonWantToDeleteClass, name="commonWantToDeleteClass"),


]  