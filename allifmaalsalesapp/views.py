from django.shortcuts import render,HttpResponse,redirect
from allifmaalusersapp.models import User
from django.db.models import Count,Min,Max,Avg,Sum
from allifmaalcommonapp.forms import CommonAddTasksForm
from allifmaalcommonapp.models import CommonSupplierPaymentsModel,CommonCustomerPaymentsModel, CommonInvoicesModel, CommonAssetsModel,CommonExpensesModel,CommonQuotesModel,CommonCustomersModel,CommonSuppliersModel,CommonStocksModel
from allifmaalcommonapp.allifutils import common_shared_data
from allifmaalcommonapp.decorators import subscriber_company_status,logged_in_user_must_have_profile
# Create your views here.

#@logged_in_user_must_have_profile
#@subscriber_company_status
def salesHome(request,*allifargs,**allifkwargs):
    title="Home : Sales & Distribution Sector"
    try:
        allif_data=common_shared_data(request)
        if allif_data.get("logged_in_user_profile") is not None:
            user_is_supper=request.user.is_superuser
            limit_values=10

            allifqueryset_quotes=CommonQuotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),prospect='Likely',total__gte=2).order_by('-total')[:limit_values]
            quotes_total=allifqueryset_quotes.aggregate(Sum('total'))['total__sum']

            allifqueryset_customers=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),turnover__gte=2).order_by('-turnover')[:limit_values]
            customers_turnover=allifqueryset_customers.aggregate(Sum('turnover'))['turnover__sum']
            
            allifqueryset_suppliers=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),turnover__gte=2).order_by('-turnover')[:limit_values]
            suppliers_turnover=allifqueryset_suppliers.aggregate(Sum('turnover'))['turnover__sum']
            
            allifqueryset_debtors=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),balance__gte=2).order_by('-balance')[:limit_values]
            customers_balances=allifqueryset_debtors.aggregate(Sum('balance'))['balance__sum']
            
            allifqueryset_creditors=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),balance__gte=2).order_by('-balance')[:limit_values]
            suppliers_balances=allifqueryset_creditors.aggregate(Sum('balance'))['balance__sum']
            
            
            gold_items=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),total_units_sold__gte=2).order_by('-total_units_sold')[:limit_values]
            gold_items_value=gold_items.aggregate(Sum('unitPrice'))['unitPrice__sum']
            
            high_value_assets=CommonAssetsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),value__gte=2).order_by('-value')[:limit_values]
            assets_value=high_value_assets.aggregate(Sum('value'))['value__sum']
            
            high_value_expenses=CommonExpensesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),amount__gte=2).order_by('-amount')[:limit_values]
            expenses_value=high_value_expenses.aggregate(Sum('amount'))['amount__sum']

            high_value_invoices=CommonInvoicesModel.objects.filter(posting_inv_status='posted',company=allif_data.get("main_sbscrbr_entity"),invoice_status='Paid',total__gte=2).order_by('-total')[:limit_values]
            invoices_total=high_value_invoices.aggregate(Sum('total'))['total__sum']

            high_value_customer_payments=CommonCustomerPaymentsModel.objects.filter(status='posted',company=allif_data.get("main_sbscrbr_entity"),amount__gte=2).order_by('-amount')[:limit_values]
            customer_payments_total=high_value_customer_payments.aggregate(Sum('amount'))['amount__sum']
            
            high_value_supplier_payments=CommonSupplierPaymentsModel.objects.filter(status='posted',company=allif_data.get("main_sbscrbr_entity"),amount__gte=2).order_by('-amount')[:limit_values]
            supplier_payments_total=high_value_supplier_payments.aggregate(Sum('amount'))['amount__sum']

            high_peformancing_staff=User.objects.filter(company=request.user.company,peformance_counter__gte=2).order_by('-peformance_counter')[:limit_values]
            staff_rating=allif_data.get("usernmeslg")

            context={"title":title,"user_is_supper":user_is_supper,
            "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
            "allifqueryset_quotes":allifqueryset_quotes,
            "quotes_total":quotes_total,
            "allifqueryset_customers":allifqueryset_customers,
            "customers_turnover":customers_turnover,

            "allifqueryset_suppliers":allifqueryset_suppliers,
            "suppliers_turnover":suppliers_turnover,
            "allifqueryset_debtors":allifqueryset_debtors,
            "customers_balances":customers_balances,
            "allifqueryset_creditors":allifqueryset_creditors,
            "suppliers_balances":suppliers_balances,

            "gold_items":gold_items,
            "gold_items_value": gold_items_value,
            "high_value_assets":high_value_assets,
            "assets_value":assets_value,
            "high_value_expenses":high_value_expenses,
            "expenses_value":expenses_value,
            "high_value_invoices":high_value_invoices,
            "invoices_total":invoices_total,
            "high_value_customer_payments":high_value_customer_payments,
            "customer_payments_total":customer_payments_total,
            "high_value_supplier_payments":high_value_supplier_payments,
            "supplier_payments_total":supplier_payments_total,
            "high_peformancing_staff":high_peformancing_staff,
            "staff_rating":staff_rating,
            
            }
            return render(request,"allifmaalsalesapp/home/home.html",context)
        else:
            return redirect('allifmaalcommonapp:commonAddStaffProfile',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

def salesDashboard(request,*allifargs,**allifkwargs):
    try:
        allif_data=common_shared_data(request)
        title="Dashboard : Distribution Dashboard"
        limit_values=10

        allifqueryset_quotes=CommonQuotesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),prospect='Likely',total__gte=2).order_by('-total')[:limit_values]
        quotes_total=allifqueryset_quotes.aggregate(Sum('total'))['total__sum']

        allifqueryset_customers=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),turnover__gte=2).order_by('-turnover')[:limit_values]
        customers_turnover=allifqueryset_customers.aggregate(Sum('turnover'))['turnover__sum']
        
        allifqueryset_suppliers=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),turnover__gte=2).order_by('-turnover')[:limit_values]
        suppliers_turnover=allifqueryset_suppliers.aggregate(Sum('turnover'))['turnover__sum']
        
        allifqueryset_debtors=CommonCustomersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),balance__gte=2).order_by('-balance')[:limit_values]
        customers_balances=allifqueryset_debtors.aggregate(Sum('balance'))['balance__sum']
        
        allifqueryset_creditors=CommonSuppliersModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),balance__gte=2).order_by('-balance')[:limit_values]
        suppliers_balances=allifqueryset_creditors.aggregate(Sum('balance'))['balance__sum']
        
        
        gold_items=CommonStocksModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),total_units_sold__gte=2).order_by('-total_units_sold')[:limit_values]
        gold_items_value=gold_items.aggregate(Sum('unitPrice'))['unitPrice__sum']
        
        high_value_assets=CommonAssetsModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),value__gte=2).order_by('-value')[:limit_values]
        assets_value=high_value_assets.aggregate(Sum('value'))['value__sum']
        
        high_value_expenses=CommonExpensesModel.objects.filter(company=allif_data.get("main_sbscrbr_entity"),amount__gte=2).order_by('-amount')[:limit_values]
        expenses_value=high_value_expenses.aggregate(Sum('amount'))['amount__sum']

        high_value_invoices=CommonInvoicesModel.objects.filter(posting_inv_status='posted',company=allif_data.get("main_sbscrbr_entity"),invoice_status='Paid',total__gte=2).order_by('-total')[:limit_values]
        invoices_total=high_value_invoices.aggregate(Sum('total'))['total__sum']

        high_value_customer_payments=CommonCustomerPaymentsModel.objects.filter(status='posted',company=allif_data.get("main_sbscrbr_entity"),amount__gte=2).order_by('-amount')[:limit_values]
        customer_payments_total=high_value_customer_payments.aggregate(Sum('amount'))['amount__sum']
        
        high_value_supplier_payments=CommonSupplierPaymentsModel.objects.filter(status='posted',company=allif_data.get("main_sbscrbr_entity"),amount__gte=2).order_by('-amount')[:limit_values]
        supplier_payments_total=high_value_supplier_payments.aggregate(Sum('amount'))['amount__sum']

        high_peformancing_staff=User.objects.filter(usercompany=request.user.usercompany,peformance_counter__gte=2).order_by('-peformance_counter')[:limit_values]
        staff_rating=allif_data.get("usernmeslg").peformance_counter


        context={"title":title,
        "main_sbscrbr_entity":allif_data.get("main_sbscrbr_entity"),
        "allifqueryset_quotes":allifqueryset_quotes,
        "quotes_total":quotes_total,
        "allifqueryset_customers":allifqueryset_customers,
        "customers_turnover":customers_turnover,

        "allifqueryset_suppliers":allifqueryset_suppliers,
        "suppliers_turnover":suppliers_turnover,
        "allifqueryset_debtors":allifqueryset_debtors,
        "customers_balances":customers_balances,
        "allifqueryset_creditors":allifqueryset_creditors,
        "suppliers_balances":suppliers_balances,

        "gold_items":gold_items,
        "gold_items_value": gold_items_value,
        "high_value_assets":high_value_assets,
        "assets_value":assets_value,
        "high_value_expenses":high_value_expenses,
        "expenses_value":expenses_value,
        "high_value_invoices":high_value_invoices,
        "invoices_total":invoices_total,
        "high_value_customer_payments":high_value_customer_payments,
        "customer_payments_total":customer_payments_total,
        "high_value_supplier_payments":high_value_supplier_payments,
        "supplier_payments_total":supplier_payments_total,
        "high_peformancing_staff":high_peformancing_staff,
        "staff_rating":staff_rating,
        
        }
    
        return render(request,"allifmaalsalesapp/dashboard/dashboard.html",context)
        
    except Exception as ex:
        error_context={'error_message': ex,}
        return render(request,'allifmaalcommonapp/error/error.html',error_context)

