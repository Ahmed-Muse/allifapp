from django.urls import path
from . import views
app_name='allifmaalonlineapp'
urlpatterns = [
    
        path('Online/Ecommerce/Home/', views.allifOnlineHome, name="allifOnlineHome"),
        path('online-store', views.onlineStore, name="online-store"),
        path('cart', views.cart, name="cart"),
        path('check-out', views.checkout, name="check-out"),
        path('add-online-stock', views.addOnlineStock, name="add-online-stock"),
        path('add-online-customer', views.addOnlineCustomer, name="add-online-customer"),
        path('create-online-order', views.createOnlineOrder, name="create-online-order"),
        path('add-online-items', views.addOnlineItemsToOrder, name="add-online-items"),
        

        path('add-online-shippingaddress', views.addOnlineCustomerShippingAddress, name="add-online-shippingaddress"),
        path('delete-online-stock/<str:pk>', views.deleteOnlineStock, name="delete-online-stock"),
        path('delete-online-customer/<str:pk>', views.deleteOnlineCustomer, name="delete-online-customer"),
        path('delete-online-order/<str:pk>', views.deleteOnlineOrder, name="delete-online-order"),
        path('delete-online-ordered-item/<str:pk>', views.deleteOnlineOrderedItem, name="delete-online-ordered-item"),
        path('update_items', views.updateItem, name="update_items"),
        path('process_order', views.processOrder, name="process_order"),

        #path('deleteInvProduct/<str:pk>/', views.deleteInvProduct, name="deleteInvProduct"),

]  