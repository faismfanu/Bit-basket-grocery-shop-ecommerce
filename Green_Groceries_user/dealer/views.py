from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from ad.models import *
from datetime import date
import datetime
from .models import *
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
        today = date.today()
        order = Order.objects.filter(dealer=dealer, date_ordered=today ,complete=True)
       
     
        print('lol ',order)
        context = {'order':order,'today':today}
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
    print('haiiiii')
    # id = request.POST.get('order_id')
    # status = request.POST.get('order_status')
    # print(id)
    # print(status)
   

    # order = Order.objects.get(id = id)
    # print('koooooi',order)
    # # order.orderitem_status = status
    # # order.save()
    return redirect('dealer_orders')


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
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        return render(request, 'dealer/dashboard_sample.html',{'dealer':dealer})
    else:
        return render(request,'dealer/login_sample.html')   
   


def order_sample(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        print('fadsf',dealer)
        today = date.today()
        order = Order.objects.filter(dealer=dealer, date_ordered=today ,complete=True)
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
   

def offers(request):

    return render(request,"dealer/offer.html")


def add_offer(request):
    if request.user.is_authenticated:
        user = request.user.id
        dealer = Dealers.objects.get(user_id=user)
        products = Product.objects.filter(dealer=dealer,offer_price=0)
        print("asf",products)
        print(products)
        # offers = offer()
        if request.method == "POST":
            offer_image = request.FILES['offer_image']
            offer_name= request.POST.get('offer_name')
            discount_amount = request.POST.get('offer_amount')
            product = request.POST.get('offer_product')
            product_obj=Product.objects.get(id=product)
            dealer = dealer
            offers = offer.objects.create(offer_image=offer_image,offer_name=offer_name,discount_amount=discount_amount,product=product_obj,dealer=dealer)
            offers.save()
            price = product_obj.newprice
            product_obj.offer_price = price
            discount_amounts = int(discount_amount)
            offer_price =  int(price)*(discount_amounts/100)
            product_obj.newprice = offer_price
            product_obj.save()
            return redirect('offers')
        else:
            return render(request,"dealer/add_offer.html",{'products':products})       


    else:
        return render(request,'dealer/login.html') 
   
  