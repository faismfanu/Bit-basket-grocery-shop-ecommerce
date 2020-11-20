from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User,auth
from ad.models import *
from dealer.models import *
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime
import razorpay
from . import Checksum
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from . import Checksum
from django.conf import settings

import json
from django.contrib import messages


# Create your views here.



def index(request):
    dealer = Dealers.objects.all()
    print(dealer)
    if request.user.is_authenticated :
        login_user = request.user
        login_name = request.user.username
        login_email = request.user.email
        user, created = Customer.objects.get_or_create(user = login_user, name = login_name, email = login_email)
        customer=request.user.customer
        # print(customer)
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
        item_count = items.count()
     
       
        # cartItems = order.get_cart_itemsdealer_dashboard
        
    
    else:
        customer = 0
        items = []  
        order = {'get_cart_items':0,'shipping':False}  
        item_count = 0
        cartItems = order['get_cart_items']
    context = {'dealer':dealer,'items':items,'order':order,'item_count':item_count}

    return render(request,'index.html',context)



def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            if user.is_staff == 0:
                auth.login(request,user)
                if user.is_staff == 0:
                    return redirect(index)
            else:
                dicti={'error':"inavlid credention"}
                return render(request,'login.html',dicti)     
        else:
            dicti={'error':"inavlid credention"}
            return render(request,'login.html',dicti)     
    return render(request, 'login.html')




def signup(request):
    
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        dic={"lastname":lastname, "email":email, "username":username}

        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Mobile number already taken')
            return render(request, 'signup.html',dic)

        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email is Taken')
            return render(request, 'signup.html',dic)
    
        else:
            user = User.objects.create_user(last_name=lastname,username=username,email=email,password=password)
            user.save()
            messages.info(request,'User Created') 
            return redirect('login')
        
    else:
        return render(request, 'signup.html')
    return render(request,"signup.html")
    

       

def user_products(request,id):
    catogery = catogeries.objects.all()
    dealer = Dealers.objects.get(id=id)
    product = Product.objects.filter(dealer=id)
    product_images = Product_images.objects.filter(product_id=product)
    if request.user.is_authenticated :
        customer = request.user.customer
        dealer = Dealers.objects.get(id=id)
        print("hai",dealer)
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer,  complete=False)
        items = order.orderitem_set.all()
        item_count = items.count()
        print(item_count)
        # cartItems = order.get_cart_items
        print(items)
       
    else:
        items = []  
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}  
        # cartItems = order['get_cart_items']
        item_count = 0
    context = {'items':items,'order':order,'product':product,'dealer':dealer, 'product_images':product_images,'item_count':item_count,'catogery':catogery}
    return render(request,'user_products.html',context)  



def product_catogery(request,id,cat_id):
    catogery = catogeries.objects.all()
    cat = catogeries.objects.get(id=cat_id)
    catname = cat.cat_name
    print('catogery',catname)
    product = Product.objects.filter(dealer=id ,product_category=catname)
    print('value',product)
    dealer = Dealers.objects.get(id=id)
    product_images = Product_images.objects.filter(product_id=product)
    if request.user.is_authenticated and request.user.is_staff == 0:
        customer = request.user.customer
        dealer = Dealers.objects.get(id=id)
        dele = dealer.id
        print("hai",dealer)
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer,  complete=False)
        items = order.orderitem_set.all()
        item_count = items.count()
        print(item_count)
        # cartItems = order.get_cart_items
        print(items)
       
    else:
        items = []  
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}  
        # cartItems = order['get_cart_items']
        item_count = 0
    context = {'items':items,'order':order,'product':product,'dealer':dealer, 'product_images':product_images,'item_count':item_count,'catname':catname}
    return render(request,'product_catogery.html',context)     


def product_view(request,id):
    product = Product()
    try:
        product = Product.objects.get(id=id)
        product_images = Product_images.objects.filter(product_id=product)
    except:
        pass
    if request.user.is_authenticated and request.user.is_staff == 0:
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        item_count = items.count()
        # cartItems = order.get_cart_items
        print(items)
    else:
        items = []  
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        item_count = 0
        # cartItems = order['get_cart_items']
    context = {'items':items,'order':order,'product':product,'product_images':product_images,'item_count':item_count}    
    return render(request, 'product_view.html',context)




def updateItem(request):
    data = json.loads(request.body)
    product_Id = data['productId']
    action = data['action']
    print('Product_ID: ',product_Id)
    print('Action: ',action)

    customer = request.user.customer
    product = Product.objects.get(id=product_Id)
    dealer = product.dealer
    print("like",dealer)
    order, created = Order.objects.get_or_create(customer=customer,  complete=False)
    items=order.orderitem_set.all()
    item_count = items.count()
    if order.dealer == dealer:
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action =='remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()    

        if orderItem.quantity <= 0:
            orderItem.delete()
            
    elif order.dealer != dealer:
        messages.error(request,'previous Item will be deleted')  
        del_item = order.orderitem_set.all()
        del_item.delete()
        order.dealer = dealer

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        order.save()

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action =='remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()    
        
     
        if orderItem.quantity <= 0:
            orderItem.delete()
        

    else:
        order.dealer = dealer   

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        order.save()

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action =='remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()    

        if orderItem.quantity <= 0:
            orderItem.delete()
        
    return JsonResponse(item_count, safe=False)


def checkout(request):
    if request.user.is_authenticated:
        
        customer = request.user.customer
        print('fais',customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        item_count = items.count()
        cartItems = order.get_cart_items
        print(items)
        client  = razorpay.Client(auth=("rzp_test_BIydmFasQhZv1U", "vu8l6padL6tNMOQlwCYm1Q4z"))
        if request.user.is_authenticated:
            total = int(order.get_cart_total*100)
        else:
            total = int(order['get_cart_total']*100)
        
        order_amount = total
        order_currency = 'USD'
        if order_amount == 0:
            return redirect('checkout')
        else:
            response = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture = 0) )

            print(response)
            order_id = response['id']
            # context = {'items': items, 'order':order, 'cartItems':cartItems, 'order_id':order_id,'c':countries}
            # return render(request, 'checkout.html', context)

    else:
        items = []  
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}  
        cartItems = order['get_cart_items']
        item_count = 0
    context = {'items':items,'order':order,'item_count':item_count,'cartItems':cartItems,'order_id':order_id}   
    return render(request,"checkout.html", context)    


def cod(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = data['form']['total']
        order.transaction_id = transaction_id

        if float(total) == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAdress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                pincode=data['shipping']['pincode'],
                payment_cod=data['shipping']['payment_cod'],
            )        
 

    return JsonResponse('COD Order complete', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        # dealer = 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id 

        if total == order.get_cart_total:
            order.complete = True
            order.product_total = total
            
        order.save()

        if order.shipping == True:
            ShippingAdress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                country=data['shipping']['country'],
                pincode=data['shipping']['pincode'],

            )    

    else:
        print('User not logged in..')     
    print('Data:',request.body)
    return JsonResponse('payment complete!', safe=False)



def order_completed(request):
    return render(request, "order_completed.html")




# ----------------------------------------------------------------------------------------#

def dashboard(request):
    dealer = Dealers.objects.all()
    print(dealer)
    if request.user.is_authenticated :
        login_user = request.user
        login_name = request.user.username
        login_email = request.user.email
        user, created = Customer.objects.get_or_create(user = login_user, name = login_name, email = login_email)
        customer=request.user.customer
        # print(customer)
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        order_count = Order.objects.filter(customer=customer,complete=True)
        oc = order_count.count()
        cartItems=order.get_cart_items
        item_count = items.count()
        
       
        # cartItems = order.get_cart_itemsdealer_dashboard
        
    
    else:
        customer = 0
        items = []  
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}  
        item_count = 0
        # cartItems = order['get_cart_items']
    context = {'dealer':dealer,'items':items,'order':order,'item_count':item_count,'oc':oc}
    return render(request, "dashboard.html", context)


def dashboard_orders(request):
    # dealer = Dealers.objects.all()
    # print('faf',dealer)
    if request.user.is_authenticated:
        login_user = request.user
        login_name = request.user.username
        login_email = request.user.email
        user, created = Customer.objects.get_or_create(user = login_user, name = login_name, email = login_email)
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        order_count = Order.objects.filter(customer=customer,complete=True).order_by('-id')
        oc = order_count.count()
        cartItems=order.get_cart_items
        item_count = items.count() 

    else:
        customer = 0
        items = []  
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}  
        item_count = 0
        # cartItems = order['get_cart_items']
    context = {'order_count':order_count,'items':items,'order':order,'item_count':item_count,'oc':oc}
    return render(request, "dashboard_orders.html", context)    

# ----------------------------------------------------------------------------------------#


def logoutview(request):
    logout(request)
    return redirect('/')





def payment(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    item_count = items.count()
    cartItems = order.get_cart_items
    order_id = Checksum.__id_generator__()
    bill_amount = str(order.get_cart_total)
    data_dict = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
        'MOBILE_NO': '7405505665',
        'EMAIL': 'dhaval.savalia6@gmail.com',
        'CUST_ID': '123123',
        'ORDER_ID':order_id,
        'TXN_AMOUNT': bill_amount,
    } # This data should ideally come from database
    data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
    context = {
        'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
        'comany_name': settings.PAYTM_COMPANY_NAME,
        'data_dict': data_dict
    }
    return render(request, 'payment.html', context)


@csrf_exempt
def response(request):
    resp = VerifyPaytmResponse(request)
    if resp['verified']:
        # save success details to db; details in resp['paytm']
        return redirect('order_completed')
    else:
        # check what happened; details in resp['paytm']
        return HttpResponse("<center><h1>Transaction Failed</h1><center>", status=400)


def VerifyPaytmResponse(response):
    response_dict = {}
    if response.method == "POST":
        data_dict = {}
        for key in response.POST:
            data_dict[key] = response.POST[key]
        MID = data_dict['MID']
        ORDERID = data_dict['ORDERID']
        verify = Checksum.verify_checksum(data_dict, settings.PAYTM_MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            STATUS_URL = settings.PAYTM_TRANSACTION_STATUS_URL
            headers = {
                'Content-Type': 'application/json',
            }
            data = '{"MID":"%s","ORDERID":"%s"}'%(MID, ORDERID)
            check_resp = requests.post(STATUS_URL, data=data, headers=headers).json()
            if check_resp['STATUS']=='TXN_SUCCESS':
                response_dict['verified'] = True
                response_dict['paytm'] = check_resp
                return (response_dict)
            else:
                response_dict['verified'] = False
                response_dict['paytm'] = check_resp
                return (response_dict)
        else:
            response_dict['verified'] = False
            return (response_dict)
    response_dict['verified'] = False
    return response_dict        