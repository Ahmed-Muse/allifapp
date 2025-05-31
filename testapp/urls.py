from django.urls import path
from . import views
# apps/inventory/urls.py

from django.urls import path
from . import views
app_name='testapp'
urlpatterns = [
    path('testing/home/first/', views.testinapp, name="testinapp"),
    path('transfers/', views.transfer_order_list, name='transfer_order_list'),
    path('transfers/create/', views.transfer_order_create, name='transfer_order_create'),
    path('transfers/<int:pk>/', views.transfer_order_detail, name='transfer_order_detail'),
    path('transfers/<int:pk>/approve/', views.transfer_order_approve, name='transfer_order_approve'),
    
    path('transfers/<int:to_pk>/create-gin/', views.create_gin, name='create_gin'),
    path('gins/<int:pk>/', views.gin_detail, name='gin_detail'),

    path('transfers/<int:to_pk>/create-grn/', views.create_grn, name='create_grn'),
    path('grns/<int:pk>/', views.grn_detail, name='grn_detail'),
]

