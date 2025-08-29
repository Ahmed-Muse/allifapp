from django.shortcuts import render
from allifmaalcommonapp.models import CommonInvoicesModel,CommonChartofAccountsModel,CommonQuotesModel,CommonStocksModel,CommonSuppliersModel,CommonCustomerPaymentsModel, CommonAssetsModel, CommonCustomersModel, CommonExpensesModel,CommonSpacesModel,CommonSpaceUnitsModel,CommonTransactionsModel
from allifmaalcommonapp.allifutils import common_shared_data
from django.db.models import Count,Min,Max,Avg,Sum,Q
from allifmaalusersapp.models import User
# Create your views here.
def realestateHome(request,*allifargs,**allifkwargs):
    try:
        title="Home : Real Estates"
        allif_data=common_shared_data(request)
        
        value_card_one=CommonSpacesModel.objects.all().count()
        value_card_two=CommonSpaceUnitsModel.objects.all().count()
        value_card_three=CommonSpaceUnitsModel.objects.filter(current_status='Occupied').count()
        value_card_four=CommonSpaceUnitsModel.objects.filter(current_status='Available').count()
        value_card_five=CommonCustomersModel.objects.all().filter(status='active').count()
        full_table_values=CommonSpaceUnitsModel.objects.filter(current_status='Available').order_by('-name','-date')[:10]
        half_table_one_values=CommonSpaceUnitsModel.objects.filter(current_status='Maintenance').order_by('-name','-date')[:10]
        half_table_two_values=CommonSpaceUnitsModel.objects.filter(current_status='Construction').order_by('-name','-date')[:10]
        
        chart_one_values=CommonAssetsModel.objects.all().order_by('-value','-date')[:10]
        chart_two_values=CommonExpensesModel.objects.all().order_by('-amount','-date')[:10]
        chart_three_values=CommonInvoicesModel.objects.filter(posting_inv_status='posted').order_by('-total','-date')[:10]
        chart_four_values=CommonCustomerPaymentsModel.objects.all().order_by('-amount','-date')[:10]
        chart_five_values=CommonCustomersModel.objects.filter(balance__gte=1).order_by('-balance','-date')[:10]
        chart_six_values=CommonSuppliersModel.objects.filter(balance__gte=1).order_by('-balance','-date')[:10]
        
        chart_one_total=CommonAssetsModel.objects.all().order_by('-value').aggregate(Sum('value'))['value__sum']
        chart_two_total=CommonExpensesModel.objects.all().order_by('-amount').aggregate(Sum('amount'))['amount__sum']
        chart_three_total=CommonInvoicesModel.objects.all().order_by('-total').aggregate(Sum('total'))['total__sum']
        chart_four_total=CommonCustomerPaymentsModel.objects.all().order_by('-amount').aggregate(Sum('amount'))['amount__sum']
        chart_five_total=CommonCustomersModel.objects.all().order_by('-balance').aggregate(Sum('balance'))['balance__sum']
        chart_six_total=CommonSuppliersModel.objects.all().order_by('-balance').aggregate(Sum('balance'))['balance__sum']
       
        
        
        small_table_one_values=User.objects.filter(company=request.user.company,performance_counter__gte=0).order_by('-performance_counter')[:10]
        small_table_two_values=CommonCustomersModel.objects.all().order_by('-turnover')[:10]
        small_table_three_values=CommonSuppliersModel.objects.all().order_by('-turnover')[:10]
        
        small_table_four_values=CommonStocksModel.objects.all().order_by('-ratings')[:10]
        small_table_five_values=CommonStocksModel.objects.filter(quantity=0,ratings__gte=0).order_by('-ratings')[:10]
        small_table_six_values=CommonQuotesModel.objects.filter(prospect='Likely').order_by('-total')[:10]
        
        total_small_table_one=User.objects.filter(company=request.user.company,performance_counter__gte=2).count()
        total_small_table_two=CommonCustomersModel.objects.all().order_by('-turnover').aggregate(Sum('turnover'))['turnover__sum']
        total_small_table_three=CommonSuppliersModel.objects.all().order_by('-turnover').aggregate(Sum('turnover'))['turnover__sum']
        total_small_table_four=CommonStocksModel.objects.all().order_by('-ratings').aggregate(Sum('ratings'))['ratings__sum']
        total_small_table_five=CommonStocksModel.objects.filter(quantity=0,ratings__gte=0).order_by('-ratings').aggregate(Sum('ratings'))['ratings__sum']
        total_small_table_six=CommonQuotesModel.objects.filter(prospect='Likely').order_by('-total').aggregate(Sum('total'))['total__sum']
        
        
        
        user_var=request.user
       
        user_role=user_var.allifmaal_admin
        user_is_supper=request.user.is_superuser
        user_is_supper=request.user.is_superuser
        user_company=request.user.company
        spaces=CommonSpacesModel.objects.all().count()
        space_units=CommonSpaceUnitsModel.objects.all().count()
        
       
        context={
            "title":title,
            "value_card_one":value_card_one,
            "value_card_two":value_card_two,
            "value_card_three":value_card_three,
            "value_card_four":value_card_four,
            "value_card_five":value_card_five,
            "full_table_values":full_table_values,
            "half_table_one_values":half_table_one_values,
            "half_table_two_values":half_table_two_values,
            "chart_one_values":chart_one_values,
            "chart_two_values":chart_two_values,
            "chart_three_values":chart_three_values,
            "chart_four_values":chart_four_values,
            "chart_five_values":chart_five_values,
            "chart_six_values":chart_six_values,
            "chart_one_total":chart_one_total,
            "chart_two_total":chart_two_total,
            "chart_three_total":chart_three_total,
            "chart_four_total":chart_four_total,
            "chart_five_total":chart_five_total,
            "chart_six_total":chart_six_total,
            "small_table_one_values":small_table_one_values,
            "small_table_two_values":small_table_two_values,
            "small_table_three_values":small_table_three_values,
            "small_table_four_values":small_table_four_values,
            "small_table_five_values":small_table_five_values,
            "small_table_six_values":small_table_six_values,
            "total_small_table_one":total_small_table_one,
            "total_small_table_two":total_small_table_two,
            "total_small_table_three":total_small_table_three,
            "total_small_table_four":total_small_table_four,
            "total_small_table_five":total_small_table_five,
            "total_small_table_six":total_small_table_six,
            
           
            
            
            
            
            
            "user_var":user_var,
            "user_is_supper":user_is_supper,
            "user_role":user_role,
            
            "user_company":user_company,
            "spaces":spaces,
            "space_units":space_units,
           
           
        }
        return render(request,"allifmaalrealestateapp/home/home.html",context)
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

def realestateDashboard(request,*allifargs,**allifkwargs):
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
        return render(request,"allifmaalrealestateapp/dashboard/dashboard.html",context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

