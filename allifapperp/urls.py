from django.contrib import admin
from django.urls import path, include
import django

#start of images 
from django.conf import settings#for uploading files
from django.conf.urls.static import static
#end of images

urlpatterns = [
    path('admin/', admin.site.urls),# uncomment after migrations
    #path('website/', include('website.urls')),#this line does all the routing for the views
    #path('', include('website.urls')),#this line does all the routing for the views
    #path('loginpage', include('login.urls')),#point to login


    #since login is doing all the authentication, we need the two lines below
    #path('login/', include('django.contrib.auth.urls')),#this ensures and allows that we use the already built in authentication system
    #path('login/', include('login.urls')),#point to login

 
    path('Allifmaal/Application/For/Users/And/Accounts/Management/', include('allifmaalusersapp.urls')),
    
   
    path('Allifmaal/ERP/System/Admin/App/', include('allifmaaladminapp.urls')),


    path('', include('allifmaalcommonapp.urls')),
    path('Allifmaal/ERP/System/Hotels/App/', include('allifmaalhotelsapp.urls')),
    path('Allifmaal/ERP/System/Education/App/', include('allifmaalilmapp.urls')),
    path('Allifmaal/ERP/System/Logistics/App/', include('allifmaallogisticsapp.urls')),
    path('Allifmaal/ERP/System/Real/Estate/App/', include('allifmaalrealestateapp.urls')),
    path('Allifmaal/ERP/System/Distribution/Sales/App/', include('allifmaalsalesapp.urls')),
    path('Allifmaal/ERP/System/Healthcare/App/', include('allifmaalshaafiapp.urls')),
    path('Allifmaal/ERP/System/Services/App/', include('allifmaalservicesapp.urls')),
    path('Allifmaal/ERP/System/Onlines/App/', include('allifmaalonlineapp.urls')),

]

if settings.DEBUG:#if debug which is in development stage only, then add the path below
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#this will enable 