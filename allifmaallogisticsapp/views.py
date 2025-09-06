# realestateapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from allifmaalcommonapp.allifutils import common_shared_data
from allifmaalcommonapp.decorators import allif_base_view_wrapper,logged_in_user_can_delete
from .forms import *
from .models import *
from allifmaalcommonapp.models import CommonDocsFormatModel
from allifmaalcommonapp.utils import allif_common_detail_view,allif_filtered_and_sorted_queryset, allif_common_form_edit_and_save, allif_delete_confirm, allif_delete_hanlder, allif_search_handler, allif_advance_search_handler, allif_document_pdf_handler, allif_common_form_submission_and_save
from django.db.models import Q
from uuid import uuid4 
from django.utils import timezone
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

def logisticsHome(request,*allifargs,**allifkwargs):
    
    title="Home : Logistics "
    try:
        user_is_supper=request.user.is_superuser
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_profile") is not None:
            context={"title":title,"user_is_supper":user_is_supper,}
            return render(request,"allifmaallogisticsapp/home/home.html",context)
        else:
            return redirect('allifmaalcommonapp:commonAddStaffProfile',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)
    
   
def logisticsDashboard(request,*allifargs,**allifkwargs):
    try:
        title="Dashboard : Hospitality"
        user_var=request.user
        user_role=user_var.allifmaal_admin
        user_is_supper=request.user.is_superuser
        context={
            "title":title,
            "user_var":user_var,
            "user_is_supper":user_is_supper,
        }
        return render(request,"allifmaallogisticsapp/dashboard/dashboard.html",context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)




######################### FLIGHTS #########################
@allif_base_view_wrapper
def flights(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Flights"
    formats=CommonDocsFormatModel.all_objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,FlightsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaallogisticsapp/flights/flights.html',context)

@allif_base_view_wrapper
def newFlight(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    
    ###### start... UID generation ##################
    allifquery=FlightsModel.all_objects.filter(company=request.user.company)
    unque=str(uuid4()).split('-')[2]
    nmbr=int(allifquery.count())+int(1)
    currntyear=timezone.now().date().today().year
    allifuid=str(nmbr)+"/"+str(unque)
    ###### End... UID generation ##################

    if allifquery:
        sqnmbr='FLT'+"/"+str(allifuid)
    else:
        sqnmbr= 'FLT/1'+"/"+str(uuid4()).split('-')[2]

    newQuoteNumber=CommonTransitModel.all_objects.create(number=sqnmbr,company=request.user.company,owner=request.user,division=allif_data.get("logged_user_division"),branch=allif_data.get("logged_user_branch"),department=allif_data.get("logged_user_department"))
    newQuoteNumber.save()
    return redirect('allifmaallogisticsapp:flights',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))

@allif_base_view_wrapper
def wantToDeleteFlight(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,FlightsModel,"Delete this item",'allifmaallogisticsapp/flights/delete-flight-confirm.html')

@allif_base_view_wrapper
def deleteFlight(request,pk,*allifargs,**allifkwargs):
    return allif_delete_hanlder(request,model_name='FlightsModel',
    pk=pk,success_redirect_url_name='flights',app_namespace='allifmaallogisticsapp',)
   
@allif_base_view_wrapper
def flightSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='FlightsModel',search_fields_key='FlightsModel',
    template_path='allifmaallogisticsapp/flights/flights.html',search_input_name='allifsearchcommonfieldname',)

@allif_base_view_wrapper
def flightAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='FlightsModel',advanced_search_config_key='FlightsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaallogisticsapp/flights/flights.html',
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html',)
 
@allif_base_view_wrapper
def addFlightDetails(request, pk, *allifargs, **allifkwargs):
    allifquery=get_object_or_404(FlightsModel, id=pk)
    return allif_common_form_edit_and_save(request,pk,AddFlightDetailsForm,"Flight Details",
    'addFlightDetails','allifmaallogisticsapp/flights/add_flight_details.html',
    redirect_with_pk=True,redirect_pk_value=pk,)


@allif_base_view_wrapper
def flightpdf(request, pk, *allifargs, **allifkwargs):
    return allif_document_pdf_handler(request,pk=pk,document_config_key='FlightsModel',)

##########################3 TICKETS #########################
@allif_base_view_wrapper
def flightTickets(request,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    title="Tickets"
    formats=CommonDocsFormatModel.all_objects.all()
    allifqueryset =allif_filtered_and_sorted_queryset(request,FlightsModel,allif_data,explicit_scope='all')
    context={"title":title,"allifqueryset":allifqueryset,"sort_options": allifqueryset.sort_options,"formats":formats,}
    return render(request,'allifmaallogisticsapp/flights/tickets/tickets.html',context)
@allif_base_view_wrapper
def addFlightTickets(request,pk,*allifargs,**allifkwargs):
    allif_data=common_shared_data(request)
    allifquery=get_object_or_404(FlightsModel, id=pk)
    allifqueryset=TicketsModel.all_objects.filter(flight=allifquery)
   
    def transaction_item_pre_save(obj, request, allif_data):
        obj.flight=allifquery
    my_extra_context={"allifquery":allifquery,"allifqueryset": allifqueryset}
    return allif_common_form_submission_and_save(request,form_class=AddFlightTicketDetailsForm,
        title_text="Add Transit Items",
        success_redirect_url_name='addFlightTickets', # This URL expects a PK
        template_path='allifmaallogisticsapp/flights/tickets/add_tickets.html',
        pre_save_callback=transaction_item_pre_save,redirect_with_pk=True,redirect_pk_value=pk,
        extra_context=my_extra_context,)

@allif_base_view_wrapper
def wantToDeleteFlightTicket(request,pk,*allifargs,**allifkwargs):
    return allif_delete_confirm(request,pk,TicketsModel,"Delete this item",'allifmaallogisticsapp/flights/delete-flight-confirm.html')

@allif_base_view_wrapper
def deleteFlightTicket(request,pk,*allifargs,**allifkwargs):
    query=get_object_or_404(TicketsModel, id=pk)
    allifquery=query.flight.id
    return allif_delete_hanlder(request,model_name='TicketsModel',
    pk=pk,success_redirect_url_name='addFlightTickets',redirect_with_pk=True,redirect_pk_value=allifquery)

@allif_base_view_wrapper
def editFlightTicket(request, pk, *allifargs, **allifkwargs):
    query=get_object_or_404(TicketsModel, id=pk) 
    allifquery=query.shipment.id
    return allif_common_form_edit_and_save(request,pk,AddFlightTicketDetailsForm,"Edit Item",
    'addFlightTickets','allifmaallogisticsapp/flights/tickets/add_tickets.html',
    redirect_with_pk=True,redirect_pk_value=allifquery,)
   
@allif_base_view_wrapper
def flightTicketDetails(request, pk, *allifargs, **allifkwargs):
    return allif_common_detail_view(request,model_class=TicketsModel,pk=pk,
        template_name='allifmaallogisticsapp/flights/tickets/ticket_details.html', # Create this template
        title_map={'default': 'Item Shipment Details'},)


@allif_base_view_wrapper
def flightTicketSearch(request,*allifargs,**allifkwargs):
    return allif_search_handler(request,model_name='TicketsModel',search_fields_key='TicketsModel',
    template_path='allifmaallogisticsapp/flights/tickets/tickets.html',search_input_name='allifsearchcommonfieldname',)

@allif_base_view_wrapper
def flightTicketAdvanceSearch(request,*allifargs,**allifkwargs):
    return allif_advance_search_handler(request,model_name='TicketsModel',advanced_search_config_key='TicketsModel', # Key for ADVANCED_SEARCH_CONFIGS in utils.py
        template_html_path='allifmaallogisticsapp/flights/tickets/tickets.html',
        template_pdf_path='allifmaalcommonapp/ui/pdf/items-pdf.html',)
 
    