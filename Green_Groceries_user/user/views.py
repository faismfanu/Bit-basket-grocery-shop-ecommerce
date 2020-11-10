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


# Create your views here.



def index(request):
    dealer = Dealers.objects.all()
    print(dealer)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        item_count = items.count()
        # cartItems = order.get_cart_items
        
    
    else:
        items = []  
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}  
        item_count = 0
        # cartItems = order['get_cart_items']
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

        
        if User.objects.filter(last_name=lastname).exists():
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
    product = Product.objects.filter(dealer=id)
    product_images = Product_images.objects.filter(product_id=product)
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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
    context = {'items':items,'order':order,'product':product, 'product_images':product_images,'item_count':item_count}
    return render(request,'user_products.html',context)  


def product_view(request,id):
    product = Product()
    try:
        product = Product.objects.get(id=id)
        product_images = Product_images.objects.filter(product_id=product)
    except:
        pass
    if request.user.is_authenticated:
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
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()    

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
    
        print('fais',customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        item_count = items.count()
        cartItems = order.get_cart_items
        print(items)
    else:
        items = []  
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}  
        cartItems = order['get_cart_items']
        item_count = 0
    context = {'items':items,'order':order,'item_count':item_count,'cartItems':cartItems}   
    return render(request,"checkout.html", context)    



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



def logoutview(request):
    logout(request)
    return redirect('/')
