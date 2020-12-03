from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from ad.models import *
from datetime import *
import requests
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files import File as DjangoFile
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files import File
from django.core.files.storage import FileSystemStorage

# Create your views here.



def dealerlogin(request):
    if request.user.is_authenticated:
        return redirect('dealer_dashboard')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff == 1:
                auth.login(request,user)
                if user.is_staff == 1:
                    return redirect('dashboard_sample')
            else:
                messages.error(request, 'Invalid username and password')
                return redirect('login_sample')

        else:
            messages.error(request, 'Invalid username and password')
            return redirect('login_sample')
    else:
       return render(request,'dealer/login_sample.html')

def login_sample(request):
    if request.user.is_authenticated:
        return redirect('dashboard_sample')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff == 1 and user.is_superuser == False:
                auth.login(request,user)
                if user.is_staff == 1:
                    return redirect('dashboard_sample')
            else:
                messages.error(request, 'Invalid username and password')
                return redirect('login_sample')

        else:
            messages.error(request, 'Invalid username and password')
            return redirect('login_sample')
    else:
        return render(request, 'dealer/login_sample.html')        




@login_required(login_url='/')
def dealer_dashboard(request):

    if request.user.is_authenticated:
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        print("hai",dealer)
        return render(request,'dealer/dealer_dashboard.html',{'dealer':dealer})
    else:
        return render(request,'dealer/login.html')    




def dealer_products(request):
    if request.user.is_authenticated:
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        product = Product.objects.filter(dealer=dealer)
        catogery = catogeries.objects.all()
        return render(request,"dealer/dealer_products.html" ,{'product':product,'catogery':catogery})
    else:
        return render(request,'dealer/login.html') 
    

def dealer_orders(request):
    if request.user.is_authenticated:
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        print(dealer)
        order = Order.objects.filter(dealer=dealer ,complete=True)
        print(order)
        context = {'order':order}
        return render(request, 'dealer/dealer_orders.html',context)
    else:
        return render(request,'dealer/login.html') 
    


def dealer_orderhistory(request):
    if request.user.is_authenticated:
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        print(dealer)
        today = date.today()
        order = Order.objects.filter(dealer=dealer ,complete=True)
        print(order)
       
        
        context = {'order':order,'today':today}
        return render(request, 'dealer/dealer_orderhistory.html',context)
    else:
        return render(request,'dealer/login.html') 
    


def update_order(request):
    id = request.POST.get('order_id')
    status = request.POST.get('order_status')
    print(id)
    print(status)
    order = Order.objects.get(id = id)
    print('koooooi',order)
    order.order_status = status
    order.save()
    return JsonResponse('hello',safe=False)


def add_products(request):
    if request.user.is_authenticated:
        products = Product()
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        if request.method == "POST":
            products.dealer = dealer
            products.name= request.POST.get('product_name')
            products.product_category= request.POST.get('product_catogery')
            products.newprice= request.POST.get('product_price')
            products.product_type = request.POST.get('product_type')
            products.stock = request.POST.get('product_stock')
            products.description = request.POST.get('product_discription')
            products.product_image = request.FILES['image1']
            images = request.FILES.getlist('file[]')
            products.save()


            for img in images:
                fs=FileSystemStorage()
                file_path=fs.save(img.name,img)
                pimage=Product_images(product_id=products,image=file_path)
                pimage.save()

            messages.success(request, "Project Senting  Successfully!")    


            return redirect(dealer_products)
        else:
            return render(request,"dealer/dealer_products.html")


    else:
        return render(request,'dealer/login.html') 

    
def delete_product(request,id):
    if request.user.is_authenticated:
        product = Product.objects.filter(id=id)

        product.delete()
        return redirect(product_sample)
    else:
        return render(request,'dealer/login.html') 





def dealerlogout(request):
    auth.logout(request)
    return redirect('login_sample')



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def dashboard_sample(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        today = datetime.date.today()
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        order = Order.objects.filter(dealer=dealer,complete=True)
        t_order = Order.objects.filter(dealer=dealer,complete=True,date_ordered=today)
        p_sum = 0
        t_sum = 0
        for orders in order:
            p_sum += orders.product_total
        for t_orders in t_order:
            t_sum += t_orders.product_total    
        order_count = Order.objects.filter(dealer=dealer,complete=True).count()
        today_orders = Order.objects.filter(dealer=dealer,complete=True,date_ordered=today).count()
        print(today_orders)

        
        year = datetime.date.today().year
        month = datetime.date.today().month
        today = date.today()
        print('today:',month)
        today_order = Order.objects.filter(dealer=dealer,date_ordered = today,complete=True)

        print('hi',today_order)

        chart_order = Order.objects.filter(dealer=dealer,date_ordered__year = year,date_ordered__month = month)

        chart_values = []
        
        for i in range(0,12):
            chart_order = Order.objects.filter(dealer=dealer,date_ordered__year = year,date_ordered__month = month-5+i,complete=True)
            order_total = 0
            for items in chart_order:
                try:
                    order_total += round(items.get_cart_total,2)
                except:
                    order_total += 0
            chart_values.append(round(order_total,2))        
        print(chart_values)

        orders = Order.objects.filter(dealer=dealer,complete=True)
        print('order',orders.count())
        total = 0
        for order in orders:
            try:
                order_total = order.get_cart_total
            except:
                order_total = 0
            total = total + order_total

        print('total',round(total,2))

        payment = []

        paypal = ShippingAdress.objects.filter(payment_status='paypal')
        razor = ShippingAdress.objects.filter(payment_status='razorpay')
        cashondelivery = ShippingAdress.objects.filter(payment_cod='cash')
        pay = paypal.count()
        raz = razor.count()
        cnt = cashondelivery.count()
        print('paypal:',pay,'RaZ:',raz,'cod:',cnt)
        payment.append(raz)
        payment.append(pay)
        payment.append(cnt)
        print('payment checking:',payment)
        context = {'payment':payment,'orders':orders,'today_order':today_order,'total':total,'chart_values':chart_values,'dealer':dealer,'order_count':order_count,'today_orders':today_orders,'p_sum':p_sum,'t_sum':t_sum}
        return render(request, 'dealer/dashboard_sample.html',context)
    else:
        return render(request,'dealer/login_sample.html')   
   


def order_sample(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        print('fadsf',dealer)
        today = date.today()
        order = Order.objects.filter(dealer=dealer ,complete=True)
        context = {'order':order,'dealer':dealer,'today':today}
        return render(request, 'dealer/order_sample.html',context)
    else:
        return render(request,'dealer/login_sample.html') 
    



def order_history_sample(request):
    if request.user.is_authenticated:
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        print(dealer)
        today = date.today()
        order = Order.objects.filter(dealer=dealer ,complete=True)
        print(order)
        context = {'order':order,'dealer':dealer,'today':today}
        return render(request,'dealer/order_history_sample.html',context)   
    else:
        return render(request,'dealer/login_sample.html') 


def product_sample(request):
    if request.user.is_authenticated:
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        product = Product.objects.filter(dealer=dealer)
        catogery = catogeries.objects.all()
        return render(request,"dealer/product_sample.html" ,{'product':product,'dealer':dealer,'catogery':catogery})
    else:
        return render(request,'dealer/login_sample.html') 
    

def add_product_sample(request):
    if request.user.is_authenticated:
        products = Product()
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        catogery = catogeries.objects.all()
        if request.method == "POST":
            products.dealer = dealer
            products.name= request.POST.get('product_name')
            products.product_category= request.POST.get('product_catogery')
            products.newprice= request.POST.get('product_price')
            products.product_type = request.POST.get('product_type')
            products.stock = request.POST.get('product_stock')
            products.description = request.POST.get('product_discription')
            products.product_image = request.FILES['add_image1']
            products.offer_price = 0
            images = request.FILES.getlist('file[]')
            products.save()


            for img in images:
                fs=FileSystemStorage()
                file_path=fs.save(img.name,img)
                pimage=Product_images(product_id=products,image=file_path)
                pimage.save()

            return redirect(product_sample)
        else:
              return render(request, 'dealer/add_product_sample.html',{'catogery':catogery})     


    else:
        return render(request,'dealer/login.html') 
   

def edit_product_sample(request,id):
    products = Product.objects.get(id=id)
    p_image = Product_images.objects.filter(product_id=id)
    print()
    if request.user.is_authenticated:
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        catogery = catogeries.objects.all()
        if request.method == "POST":
            products.dealer = dealer
            products.name= request.POST.get('product_name')
            products.product_category= request.POST.get('product_catogery')
            products.newprice= request.POST.get('product_price')
            products.product_type = request.POST.get('product_type')
            products.stock = request.POST.get('product_stock')
            products.description = request.POST.get('product_discription')
            if 'add_image1' not in request.POST:
                products.product_image = request.FILES['add_image1']
            else:
                product = Product.objects.get(id=id)
                products.product_image = product.product_image
          

            products.offer_price = 0
            images = request.FILES.getlist('file[]')
            products.save()

            for img in images:
                fs=FileSystemStorage()
                file_path=fs.save(img.name,img)
                pimage=Product_images(product_id=products,image=file_path)
                pimage.save()

            return redirect(product_sample)
        else:
            return render(request, 'dealer/edit_product.html',{'products':products,'dealer':dealer,'catogery':catogery,'p_image':p_image})



def offers(request):
    if request.user.is_authenticated:
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        offers = offer.objects.filter(dealer = dealer)
        today = datetime.date.today()
        print('lala',today)
        
        return render(request,"dealer/offer.html", {'offers':offers,'dealer':dealer})
    else:
        return render(request,'dealer/login.html')     


def add_offer(request):
    if request.user.is_authenticated:
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        catogery = catogeries.objects.all()
        products = Product.objects.filter(dealer=dealer,offer_price=0)
        if request.method == "POST":
            offer_image = request.FILES['offer_image']
            offer_name= request.POST.get('offer_name')
            discount_amount = request.POST.get('offer_amount')
            product = request.POST.get('offer_product')
            catogery = request.POST.get('offer_category')
            product_type = request.POST.get('offer_type')
            offer_date = request.POST.get('txtDate')
            if product_type == "single":
                product_obj=Product.objects.get(id=product)
            elif product_type == "catogery":    
                catogeris = catogeries.objects.get(id=catogery)
            dealer = dealer
            if product_type == "single":
                price = product_obj.newprice
                product_obj.offer_price = price
                discount_amounts = int(discount_amount)
                offer_price =  price-(int(price)*(discount_amounts/100))
                product_obj.newprice = offer_price
                product_obj.offer_percentage = discount_amount
                product_obj.save()
            elif product_type == "catogery":
                catogeris = catogeries.objects.get(id=catogery)
                product = Product.objects.filter(dealer=dealer,product_category=catogeris.cat_name)
                for products in product:
                    if products.offer_price == 0:
                        price = products.newprice
                        products.offer_price = price
                        discount_amounts = int(discount_amount)
                        offer_price =  price-(int(price)*(discount_amounts/100))
                        products.newprice = offer_price
                        products.offer_percentage = discount_amount
                        products.save()
                    else: 
                        price = products.offer_price
                        discount_amounts = int(discount_amount)
                        offer_price =  price-(int(price)*(discount_amounts/100))
                        products.newprice = offer_price
                        products.offer_percentage = discount_amount
                        products.save()
            elif product_type == "multiple" :
                product_obj=Product.objects.get(id=product)
                price = product_obj.newprice
                product_obj.offer_price = price
                discount_amounts = int(discount_amount)
                offer_price =  price-(int(price)*(discount_amounts/100))
                product_obj.newprice = offer_price
                product_obj.offer_percentage = discount_amount
                product_obj.save()
            if product_type == "single":
                offers = offer.objects.create(offer_image=offer_image,offer_name=offer_name,discount_amount=discount_amount,product=product_obj,dealer=dealer,offer_type=product_type,offer_expiry=offer_date)    
                offers.save()
            elif product_type == "catogery":
                offers = offer.objects.create(offer_image=offer_image,offer_name=offer_name,discount_amount=discount_amount,dealer=dealer,offer_type=product_type,catogery=catogeris,offer_expiry=offer_date)    
                offers.save()
            return redirect('offers')
        else:
            return render(request,"dealer/add_offer.html",{'products':products,'catogery':catogery})       
    else:
        return render(request,'dealer/login.html') 


def edit_offer(request,id):
    offers = offer.objects.get(id=id)
    # products = Product.objects.filter(dealer=dealer,offer_price=0)
    print('jaiho',offers)


    return render(request, "dealer/edit_offer.html", {'offers':offers})

   
def delete_offer(request,id):
    if request.user.is_authenticated:
        offers = offer.objects.get(id=id)
        product_id = offers.product.id
        product = Product.objects.get(id=product_id)
        normal_price = product.offer_price
        product.newprice = normal_price
        product.offer_price = 0
        product.offer_percentage =0
        product.save()
        offers.delete()
        return redirect('offers')
    else:
        return render(request,'dealer/login.html') 

    
def delete_offer_cat(request,id) :
    if request.user.is_authenticated:
        dealer = Dealers.objects.get(user_id=request.user.id)
        print("dealer",dealer)
        offers = offer.objects.get(id=id)
        catogery_id = offers.catogery.cat_name
        print('hoop',catogery_id)
        product = Product.objects.filter(dealer=dealer,product_category=catogery_id)
        print('product',product)
        for products in product:
            price = products.offer_price
            price1 = products.newprice
            products.newprice = price
            products.offer_price = 0
            products.offer_percentage = 0
            products.save()
        offers.delete()
        return redirect('offers')
    else:
        return render(request,'dealer/login.html') 


# %%
