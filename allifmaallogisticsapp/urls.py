from django.urls import path
from . import views

app_name='allifmaallogisticsapp'
urlpatterns = [
path('Logistics/Home/<str:allifusr>/<str:allifslug>/', views.logisticsHome, name="logisticsHome"),
path('Logistics/Dashboard/<str:allifusr>/<str:allifslug>/', views.logisticsDashboard, name="logisticsDashboard"),

path('Logistics/Flights/<str:allifusr>/<str:allifslug>/', views.flights, name="flights"),
path('Logistics/NewFlight/<str:allifusr>/<str:allifslug>/', views.newFlight, name="newFlight"),
path('Logistics/Add/Edit/Flight/Details/<int:pk>/<str:allifusr>/<str:allifslug>/', views.addFlightDetails, name="addFlightDetails"),
path('Logistics/Flight/To/PDF/<int:pk>/<str:allifusr>/<str:allifslug>/', views.flightpdf, name="flightpdf"),
path('Logistics/Want/To/Delete/This/Flight/<int:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteFlight, name="wantToDeleteFlight"),
path('Logistics/Delete/This/Flight/<int:pk>/<str:allifusr>/<str:allifslug>/', views.deleteFlight, name="deleteFlight"),
path('Logistics/Search/Flights/<str:allifusr>/<str:allifslug>/', views.flightSearch, name="flightSearch"),
path('Logistics/Advance/Search/Flights/<str:allifusr>/<str:allifslug>/', views.flightAdvanceSearch, name="flightAdvanceSearch"),

path('Logistics/Flights/Tickets/<str:allifusr>/<str:allifslug>/', views.flightTickets, name="flightTickets"),
path('Logistics/Add/Flight/Tickets/<int:pk>/<str:allifusr>/<str:allifslug>/', views.addFlightTickets, name="addFlightTickets"),
path('Logistics/Want/To/Delete/This/Flight/Ticket/<int:pk>/<str:allifusr>/<str:allifslug>/', views.wantToDeleteFlightTicket, name="wantToDeleteFlightTicket"),
path('Logistics/Delete/This/Flight/Ticket/<int:pk>/<str:allifusr>/<str:allifslug>/', views.deleteFlightTicket, name="deleteFlightTicket"),
path('Logistics/Edit/This/Flight/Ticket/<int:pk>/<str:allifusr>/<str:allifslug>/', views.editFlightTicket, name="editFlightTicket"),
path('Logistics/Flight/Ticket/Details/<int:pk>/<str:allifusr>/<str:allifslug>/', views.flightTicketDetails, name="flightTicketDetails"),
path('Logistics/Search/Flight/Tickets/<str:allifusr>/<str:allifslug>/', views.flightTicketSearch, name="flightTicketSearch"),
path('Logistics/Advance/Search/Flight/Tickets/<str:allifusr>/<str:allifslug>/', views.flightTicketAdvanceSearch, name="flightTicketAdvanceSearch"),

]  



