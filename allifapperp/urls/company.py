# allifapperp/urls/company.py

from django.urls import path, include

# This URL configuration is for company-specific subdomains.
# The `company_slug` parameter will be passed from the hosts.py file.
urlpatterns = [
    # All common URLs are available under the 'allifmaalcommonapp' namespace.
    path('', include('allifmaalcommonapp.urls', namespace='allifmaalcommonapp')),
    
    # You can add other company-specific URLs here.
    # Example: path('dashboard/', views.company_dashboard, name='company_dashboard'),
    path('users/', include('allifmaalusersapp.urls', namespace='allifmaalusersapp')),
    path('users/', include('allifmaalshaafiapp.urls', namespace='allifmaalshaafiapp')),
    path('users/', include('allifmaaladminapp.urls', namespace='allifmaaladminapp')),
     path('users/', include('allifmaalsalesapp.urls', namespace='allifmaalsalesapp')),
]
