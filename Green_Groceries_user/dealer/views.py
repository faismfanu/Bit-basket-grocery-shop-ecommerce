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
                    return redirect('dealer_dashboard')
            else:
                messages.error(request, 'Invalid username and password')
                return redirect('dealerlogin')

        else:
            messages.error(request, 'Invalid username and password')
            return redirect('dealerlogin')
    else:
       return render(request,'dealer/login.html')

        

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
       
     
        print(order)
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
        return redirect(dealer_products)
    else:
        return render(request,'dealer/login.html') 





def dealerlogout(request):
    auth.logout(request)
    return redirect('dealerlogin')