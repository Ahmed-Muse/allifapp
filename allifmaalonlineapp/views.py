from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import datetime

from django.contrib import messages#for flash messages
from .models import OnlineProductsModel,OnlineOrdersModel
from .forms import *
from .utils import cookieCart,cartData,guestOrder

def allifOnlineHome(request):
    context={
        
    }
    return render(request,'allifmaalonlineapp/home/home.html',context)
# Create your views here.
def onlineStore(request):
    title="Online store"
    onlineProducts=OnlineProductsModel.objects.all()
    data=cartData(request)
    cartItems=data['cartItems']
    
   # if request.user.is_authenticated:
      #  try:
           # mycustomer=request.user.onlinecustomersmodel#this is the db
        #either create or find the order... below is two functions combined...to understand better, check docs of _or_create django
           # newOrder, createdOrder=OnlineOrdersModel.objects.get_or_create(customerName=mycustomer, status=False)
      
        #then get the items attached to that order
         #   items=newOrder.onlineordereditemsmodel_set.all()#this is querying child object with all lowercase values by setting the parent value
        #so here, this will get all the ordered items that has newOrder has the parent
        #    cartItems=newOrder.get_cart_items
      #  except:
         #   items=[]
        #do an empty dictionary
         #   newOrder={"get_cart_total":0,"get_cart_items":0}
           # return HttpResponse("The user does not have a customer, please create one")
        #cartItems=order.get_cart_items
   # else:#if the user is not logged in
      #  cookieData=cookieCart(request)
      #  cartItems=cookieData['cartItems']
        
        #items=[]
        #do an empty dictionary
        #newOrder={"get_cart_total":0,"get_cart_items":0,'shipping':False}#you can access the shipping method because it was passed to the template
        #cartItems=newOrder["get_cart_items"]

    mycontext={
        "onlineProducts":onlineProducts,
        "title":title,
        "cartItems":cartItems,
    }
    return render(request,'estore/onlinestore.html',mycontext)

def cart(request):
    title="cart"
    data=cartData(request)
    cartItems=data['cartItems']
    newOrder=data['newOrder']
    items=data['items']
    
   # if request.user.is_authenticated:
       # try:
            # I think the line below means get the customer who is connected to the user
           # mycustomer=request.user.onlinecustomersmodel#this is the database in lower case
        #either create or find the order... below is two functions combined...to understand better, check docs of _or_create django
            #newOrder, createdOrder=OnlineOrdersModel.objects.get_or_create(customerName=mycustomer, status=False)
      
        #then get the items attached to that order...the below line returns all the objects of the OlineOrderedItemsModel
           # items=newOrder.onlineordereditemsmodel_set.all()#this is querying child object with all lowercase values by setting the parent value
        #so here, this will get all the ordered items that has newOrder has the parent
           # cartItems=newOrder.get_cart_items
        #cartItems=order.get_cart_items
      #  except:
       #     items=[]
        #do an empty dictionary
         #   newOrder={"get_cart_total":0,"get_cart_items":0}
            # return HttpResponse("The user does not have a customer, please create one")
          #  cartItems=newOrder.get_cart_items

    #else:#if the user is not logged in
      #  cookieData=cookieCart(request)
      #  cartItems=cookieData['cartItems']
      #  newOrder=cookieData['newOrder']
       # items=cookieData['items']
        
    #return {'cartItems':cartItems,'order':order,'items':items}
    mycontext={
        "items":items,
        "newOrder":newOrder,
        "title":title,
        "cartItems":cartItems,

    }
    return render(request,'estore/cart.html',mycontext)

def checkout(request):
    title="Checkout"
    #if request.user.is_authenticated:
        #try:
            #mycustomer=request.user.onlinecustomersmodel#this is the db
        #either create or find the order... below is two functions combined...to understand better, check docs of _or_create django
            #newOrder, createdOrder=OnlineOrdersModel.objects.get_or_create(customerName=mycustomer, status=False)
      
        #then get the items attached to that order
            #items=newOrder.onlineordereditemsmodel_set.all()#this is querying child object with all lowercase values by setting the parent value
        #so here, this will get all the ordered items that has newOrder has the parent
        #cartItems=order.get_cart_items
           # cartItems=newOrder.get_cart_items
        #except:
           # items=[]
        #do an empty dictionary
           # newOrder={"get_cart_total":0,"get_cart_items":0}
           # return HttpResponse("The user does not have a customer, please create one")
           # cartItems=newOrder.get_cart_items
    #else:#if the user is not logged in
        
        #items=[]
        #do an empty dictionary
        # newOrder={"get_cart_total":0,"get_cart_items":0,'shipping':False}
        #cartItems=newOrder['get_cart_items']

    #cookieData=cookieCart(request)
    data=cartData(request)
    cartItems=data['cartItems']
    newOrder=data['newOrder']
    items=data['items']
        
    #return {'cartItems':cartItems,'order':order,'items':items}
    mycontext={
        "items":items,
        "newOrder":newOrder,
        "title":title,
        "cartItems":cartItems,
        
        }
   
    return render(request,'estore/checkout.html',mycontext)

def updateItem(request):
    #first, parse the sent data since it was sent as a  string value
    data=json.loads(request.body)#parse the data (body that was sent which is product id and action)
    #data=json.loads(request.data)#this also works when printing out data (product id and action)

    #then get the values of the sent data which are the product id and action
    productId=data['productId']#data here is the data that was sent from the js side
    action=data['action']#we can now access the data because its a dictionary once we parse it .
    print('Action:',action)
    print('ProductId:',productId)
    
    customer=request.user.onlinecustomersmodel#this gets the login customer...so query the customer and add to the ordered items
    product=OnlineProductsModel.objects.get(id=productId)#get the product we are passing/parsing in
    newOrder, created=OnlineOrdersModel.objects.get_or_create(customerName=customer, status=False)#get the order that is attached to the customer
    orderItem, created=OnlineOrderedItemsModel.objects.get_or_create(order=newOrder,product=product)

    if action=='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()  
    return JsonResponse("item has been added", safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)#parse the data
    if request.user.is_authenticated:
        try:
            mycustomer=request.user.onlinecustomersmodel#this is the db
            newOrder, created=OnlineOrdersModel.objects.get_or_create(customerName=mycustomer, status=False)
            """ total=float(data['form']['total'])#from the sent data, get the form value and get the user object within it and the total.
            newOrder.transaction_id=transaction_id
            if total ==newOrder.get_cart_total:#check if the total passed from front end is the same as the cart total
                newOrder.status=True
            newOrder.save() """
            """ if newOrder.shipping==True:
                OnlineCustomerShippingAddressModel.objects.create(
                customerName=mycustomer,
                order=newOrder,
                address=data['shipping']['address'],#From the sent data, grab the 'shipping' then 'address' in it.
               
                 ) """




        except:
            pass
    
    else:
        mycustomer,newOrder=guestOrder(request,data)

        """ print("user not logged in")
        
        print('COOKIES:',request.COOKIES)
        name=data['form']['name']
        email=data['form']['email']
        cookieData=cookieCart(request)
        items=cookieData['items']
        mycustomer, created=OnlineCustomersModel.objects.get_or_create(
        email=email,
        )
        mycustomer.name=name
        mycustomer.save()
        order=OnlineOrdersModel.objects.create(
        customerName=mycustomer, 
        status=False,
        )
        for item in items:
            product=OnlineProductsModel.objects.get(id=item['product']['id'])
            orderItem=OnlineOrderedItemsModel.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
            ) """

    total=float(data['form']['total'])#from the sent data, get the form value and get the user object within it and the total.
    newOrder.transaction_id=transaction_id
    if total ==newOrder.get_cart_total:#check if the total passed from front end is the same as the cart total
        newOrder.status=True
    newOrder.save()

    if newOrder.shipping==True:
        OnlineCustomerShippingAddressModel.objects.create(
        customerName=mycustomer,
        order=newOrder,
        address=data['shipping']['address'],#From the sent data, grab the 'shipping' then 'address' in it.
               
                 )
    return mycustomer, newOrder

    return JsonResponse('Payment has been made ...', safe=False)

################# start online parts for the front view #########################################
def addOnlineStock(request):
    title="Add online stock"
    form=AddOnlineStockForm(request.POST,request.FILES)
    items = OnlineProductsModel.objects.all()

    if request.method == 'POST':
        form=AddOnlineStockForm(request.POST, request.FILES)
        if form.is_valid():

            form.save()
            messages.success(request, 'Item added successfully')
        return redirect('ecommerceapp:online-store')
   
    context={
        "title": title,
        "form":form,
        "items":items,
        
        }
    return render(request,'estore/add_online_stock.html',context)


def deleteOnlineStock(request, pk):
    try:
        OnlineProductsModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('ecommerceapp:online-store')

    return redirect('ecommerceapp:online-store')  

def addOnlineCustomer(request):
    title="Add online customer"
    form=AddOnlineCustomerForm(request.POST or None)
    customers = OnlineCustomersModel.objects.all()
    if form.is_valid():
        form.save()
        messages.success(request, 'Customer added successfully')
        return redirect('ecommerceapp:online-store')
   
    context={
        "title": title,
        "form":form,
        "customers":customers,
        
        }
    return render(request,'estore/add_online_customer.html',context)


def deleteOnlineCustomer(request, pk):
    try:
        OnlineCustomersModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('ecommerceapp:online-store')

    return redirect('ecommerceapp:online-store') 

def createOnlineOrder(request):
    title="Create new order"
    form=AddOnlineOrdersForm(request.POST or None)
    orders = OnlineOrdersModel.objects.all()
    if form.is_valid():
        form.save()
        messages.success(request, 'Customer added successfully')
        return redirect('ecommerceapp:online-store')
   
    context={
        "title": title,
        "form":form,
        "orders":orders,
        
        }
    return render(request,'estore/create_online_order.html',context)


def deleteOnlineOrder(request, pk):
    try:
        OnlineOrdersModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('ecommerceapp:online-store')

    return redirect('ecommerceapp:online-store') 

def addOnlineItemsToOrder(request):
    title="Add online items to an order"
    form=AddOnlineItemsToOrderForm(request.POST or None)
    orderitems = OnlineOrderedItemsModel.objects.all()
    if form.is_valid():
        form.save()
        messages.success(request, 'Customer added successfully')
        return redirect('ecommerceapp:online-store')
   
    context={
        "title": title,
        "form":form,
        "orderitems":orderitems,
        
        }
    return render(request,'estore/order_online_items.html',context)

def deleteOnlineOrderedItem(request, pk):
    try:
        OnlineOrderedItemsModel.objects.get(id=pk).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('ecommerceapp:online-store')

    return redirect('ecommerceapp:online-store') 

def addOnlineCustomerShippingAddress(request):
    title="Allifmaal Online Stock"
    form=AddOnlineCustomerShippingAddressForm(request.POST or None)
    shipping_details = OnlineCustomerShippingAddressModel.objects.all()
    if form.is_valid():
        form.save()
        messages.success(request, 'Customer added successfully')
        return redirect('ecommerceapp:online-store')
   
    context={
        "title": title,
        "form":form,
        "shipping_details":shipping_details,
        
        }
    return render(request,'estore/online_customer_shippingaddress.html',context)

################### end ............. online part####################################################

