import json
from .models import *
def cookieCart(request):
    try:
        cart=json.loads(request.COOKIES['cart'])#this will turn back to python dictionary
    except:
        cart={}
    print('Cart:',cart)
    items=[]
    newOrder={'get_cart_total':0, 'get_cart_items':0,'shipping':False}#this is to avoid error for unauthenticated user, when you log out
    cartItems= newOrder['get_cart_items']
    for i in cart:
        try:
            cartItems+=cart[i]['quantity']
            product=OnlineProductsModel.objects.get(id=i)
            total=(product.price * cart[i]['quantity'])
            newOrder['get_cart_total']+=total
            newOrder['get_cart_items']+=cart[i]['quantity']
            item={
                'product':{
                'id':product.id,
                'name':product.name,
                'price':product.price,
                'imageURL':product.imageURL,
                 },
                'quantity':cart[i]['quantity'],
                'get_total':total
                }
            items.append(item)
            if product.digital==False:
                newOrder['shipping']=True
        except:
            pass

    return {'cartItems':cartItems,'newOrder':newOrder,'items':items}

def cartData(request):
    if request.user.is_authenticated:
        mycustomer=request.user.onlinecustomersmodel
        #either create or find the order... below is two functions combined...to understand better, check docs of _or_create django
        newOrder, created=OnlineOrdersModel.objects.get_or_create(customerName=mycustomer, status=False)
        
        #then get the items attached to that order
        items=newOrder.onlineordereditemsmodel_set.all()
        cartItems=newOrder.get_cart_items
    else:
        cookieData=cookieCart(request)
        cartItems=cookieData['cartItems']
        newOrder=cookieData['newOrder']
        items=cookieData['items']
        ''' items=[]
        
        order={'get_cart_total':0, 'get_cart_items':0,'shipping':False}#this is to avoid error for unauthenticated user, when you log out
        cartItems=order['get_cart_items'] '''
    return {'cartItems':cartItems,'newOrder':newOrder,'items':items}

def guestOrder(request,data):
    print("user not logged in")
        
    print('COOKIES:',request.COOKIES)
    name=data['form']['name']
    email=data['form']['email']
    cookieData=cookieCart(request)
    items=cookieData['items']#this 'items' is from the cookieCart
    mycustomer, created=OnlineCustomersModel.objects.get_or_create(
    email=email,
    )
    mycustomer.name=name
    mycustomer.save()
    newOrder=OnlineOrdersModel.objects.create(
    customerName=mycustomer, 
    status=False,
    )
    for item in items:
        product=OnlineProductsModel.objects.get(id=item['product']['id'])
        orderItem=OnlineOrderedItemsModel.objects.create(
        product=product,
        order=newOrder,
        quantity=item['quantity']
        )

    return mycustomer,newOrder