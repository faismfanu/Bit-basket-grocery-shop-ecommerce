from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Dealers
from dealer.models import *
from .import views
import json
from django.db.models import DateTimeField
from django.db.models.functions import Trunc
import base64
from PIL import Image
from PIL import Image
from base64 import decodestring
import binascii
from django.core.files import File
from django.http import JsonResponse 
from django.core.files.base import ContentFile
# Create your views here.




def adminlogin(request):
    if request.session.has_key('username'):
        return redirect(adminpanel)  
    elif request.method == 'POST':
        user = request.POST['username']
        password = request.POST['password']
        if user=='admin' and password=='admin':
            request.session['username'] = user
            print("asdfsadf")
            return redirect(adminpanel) 
        else:
            messages.info(request,'invalid credentials')
            return redirect(adminlogin)
    else:
        return render(request, 'admin/login.html')



def adminpanel(request):
    if request.session.has_key('username'):
        dealer = Dealers.objects.all().count()
        users = User.objects.filter(is_staff=False).count()
        order = Order.objects.filter(complete=True).count()
        catog = catogeries.objects.all().count()
        context = {'dealer':dealer,'users':users,'order':order,'catog':catog}
        return render(request,"admin/adminpanel.html",context)
    else:
        return render(request, 'admin/login.html')

def adddealer(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            dealers = Dealers()
            user = request.user
            username = request.POST['username']
            password = request.POST['password'] 
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already taken')
                return render(request, 'admin/adddealer.html')
            else:
                user = User.objects.create_user(username=username,password=password,is_staff=1)
                dealers.user_id = user
                dealers.dealer_name= request.POST.get('dealer_name')
                dealers.dealer_phone= request.POST.get('dealer_number')
                dealers.dealer_address= request.POST.get('dealer_address')
                dealers.dealer_website= request.POST.get('website')
                dealers.shop_name = request.POST.get('shope_name')
                dealers.shop_number = request.POST.get('shope_number')
                dealers.shop_location = request.POST.get('location')
                dealers.shop_place = request.POST.get('shope_place')
                dealers.shop_opening_time = request.POST.get('opening_time')
                dealers.shop_closing_time = request.POST.get('closing_time')
                image_data =request.POST.get('image64data')
                print(image_data)
                try:
                    format, imgstr = image_data.split(';base64,')
                    ext = format.split('/')[-1]
                    data = ContentFile(base64.b64decode(imgstr),name= str(user.id)+'.' +ext)
                    print("ASFDSFDASFASF",data)
                    dealers.shop_image = data
                except:
                    pass    
                 
                user.save()
                dealers.save()
                messages.error(request,"New Doctor Added")
                return redirect('dealers')
        else:
            return render(request,"admin/adddealer.html")
    else:
        return render(request, 'admin/login.html')


def edit_dealer(request,id,user_id):
    if request.session.has_key('username'):
        dealers = Dealers.objects.get(id=id)
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            dealers.user_id = user
            dealers.dealer_name= request.POST.get('dealer_name')
            dealers.dealer_phone= request.POST.get('dealer_number')
            dealers.dealer_address= request.POST.get('dealer_address')
            dealers.dealer_website= request.POST.get('website')
            dealers.shop_name = request.POST.get('shope_name')
            dealers.shop_number = request.POST.get('shope_number')
            dealers.shop_location = request.POST.get('location')
            dealers.shop_place = request.POST.get('shope_place')
            dealers.shop_opening_time = request.POST.get('opening_time')
            dealers.shop_closing_time = request.POST.get('closing_time')
            image_data =request.POST.get('image64data')
            if image_data == "":
                dealer = Dealers.objects.get(id=id)
                dealers.shop_image = dealer.shop_image
                
            else:
                try:
                    format, imgstr = image_data.split(';base64,')
                    ext = format.split('/')[-1]
                    data = ContentFile(base64.b64decode(imgstr),name= str(user.id)+'.' +ext)
                    print("ASFDSFDASFASF",data)
                    dealers.shop_image = data
                except:
                    pass
                
            dealers.save()
            messages.error(request,"Dealer Updated")
            return redirect('dealers')
        return render(request,"admin/edit_dealer.html",{'dealers':dealers})
    else:
        return render(request, 'admin/login.html')


def delete_dealer(request,id,user_id):
    if request.session.has_key('username'):
        user = User.objects.get(id=user_id)
        print(user)
        dealers = Dealers.objects.get(id=id)
        print(dealers)
        user.delete()
        dealers.delete()
        return redirect("dealers")
    else:
        return render(request, 'admin/login.html')



def addorder(request):
    if request.session.has_key('username'):
        order = Order.objects.filter(complete=True)
        dealers =Dealers.objects.all()
        # order = dealers.orderItem_set.all()
        # print(order)
        return render(request, 'admin/admin_orders.html',{'order':order,'dealers':dealers})
    else:
        return render(request, 'admin/login.html')


def order_view(request,id):
    if request.session.has_key('username'):
        order = Order.objects.get(id=id)
        try:
            shipping = ShippingAdress.objects.get(order=id)
        except:
            shipping = 0    
        items = OrderItem.objects.filter(order=id)
        return render(request, 'admin/admin_order_view.html',{'order':order,'shipping':shipping,'items':items})
    else:
        return render(request, 'admin/login.html')



def dealers(request):
    if request.session.has_key('username'):
        dealers = Dealers.objects.all()
        print(dealers)
        return render(request,"admin/dealers.html",{"dealers":dealers})
    else:
        return render(request, 'admin/login.html')


def block_dealer(request,id,user_id):
    if request.session.has_key('username'):
        dealers = Dealers.objects.get(id=id)
        user = User.objects.get(id=user_id)
        user.is_active = 0
        user.save()
        return redirect('dealers')
    else:
        return render(request, 'admin/login.html')


def unblock_dealer(request,id,user_id):
    if request.session.has_key('username'):
        dealers = Dealers.objects.get(id=id)
        user = User.objects.get(id=user_id)
        user.is_active = 1
        user.save()
        return redirect('dealers')
    else:
        return render(request, 'admin/login.html')

def base(request):
    return render(request,"admin/base.html")



def admin_catogeries(request):
    if request.session.has_key('username'):
        catogery = catogeries.objects.all()
        return render(request, "admin/admin_catogeries.html", {'catogery':catogery})
    else:
        return render(request, 'admin/login.html')



def add_catogeries(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            catogery = catogeries()
            catogery.cat_name= request.POST.get('catogery_name')
            image_data =request.POST.get('image64data')
            print(image_data)
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
            catogery.image = data

        
            
            catogery.save()
            return redirect('admin_catogeries')
        else:
            return render(request, "admin/add_catogeries.html")   
    else:
        return render(request, 'admin/login.html')


def edit_catogeries(request,id):
    if request.session.has_key('username'):
        catogery = catogeries.objects.get(id=id)
        if request.method == 'POST':
            catogery.cat_name= request.POST.get('catogery_name')
            image_data =request.POST.get('image64data')
            if image_data == "":
                cats = catogeries.objects.get(id=id)
                catogery.image = cats.image

            else:   
                print(image_data)
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
                catogery.image = data
            catogery.save()
            return redirect('admin_catogeries')
       
        else:
            return render(request, "admin/edit_catogery.html",{'catogery':catogery})
    else:
        return render(request, 'admin/login.html')

    


  
def delete_catogery(request,id):
    catogery = catogeries.objects.filter(id=id)
    catogery.delete()
    return redirect('admin_catogeries') 


def reffrel_offer(request):
    if request.session.has_key('username'):
        reffral = reffreal_offer.objects.all()
        return render(request,'admin/reffreal_offer.html',{'reffral':reffral})

    else:
        return render(request, 'admin/login.html')
    
def edit_reffrel_offer(request,id):
    if request.session.has_key('username'):
        reff = reffreal_offer.objects.get(id=id)
        if request.method == 'POST':
            reff.reff_name = request.POST.get('offer_name')
            reff.refferd_person_discount = request.POST.get('person_discount')
            reff.order_maximum = request.POST.get('minimum_price')  
            reff_offer_type = request.POST.get('offer_type')
            print(reff_offer_type)
            if reff_offer_type == "price":
                reff.reff_price = request.POST.get('offer_price')
                reff.reff_offer_type = reff_offer_type
            elif reff_offer_type == "percentage":
                reff.reff_discount = request.POST.get('offer_discount') 
                reff.reff_offer_type = reff_offer_type
            reff.save()           
            return redirect('reffrel_offer')
        else:
            return render(request, "admin/edit_reffral_offer.html",{"reff":reff})
    else:
        return render(request, 'admin/login.html')



def add_reffral(request,id):
    if request.session.has_key('username'):
        return render(request, "admin/edit_reffral_offer.html")
        # reff = reffreal_offer.objects.get(id=id)
        # if request.method == 'POST':
        #     reff.reff_name = request.POST.get('offer_name')
        #     reff.refferd_person_discount = request.POST.get('person_discount')
        #     reff.order_maximum = request.POST.get('minimum_price')  
        #     reff_offer_type = request.POST.get('offer_type')
        #     print(reff_offer_type)
        #     if reff_offer_type == "price":
        #         reff.reff_price = request.POST.get('offer_price')
        #         reff.reff_offer_type = reff_offer_type
        #     elif reff_offer_type == "percentage":
        #         reff.reff_discount = request.POST.get('offer_discount') 
        #         reff.reff_offer_type = reff_offer_type
        #     reff.save()           
        #     return redirect('reffrel_offer')
        # else:
        #     return render(request, "admin/edit_reffral_offer.html",{"reff":reff})
    else:
        return render(request, 'admin/login.html')
    

        
def adminlogout(request):
    if request.session.has_key('username'):
        request.session.delete()
        return redirect('adminlogin')
    else:
        return render(request, 'admin/login.html')


def user_control(request):
    if request.session.has_key('username'):
        user = User.objects.filter(is_staff=False,is_superuser=False,first_name='')
        return render(request, "admin/user_control.html",{'user':user})
        
    else:
        return render(request, 'admin/login.html')

def edit_user(request,id):
    if request.session.has_key('username'):
        user = User.objects.get(id=id)
        if request.method == 'POST':
            user.username = request.POST.get('name')
            user.email = request.POST.get('email')
            user.last_name = request.POST.get('mobile')
            user.save()
            return redirect('user_control')
        return render(request, "admin/edit_user.html",{'user':user})
        
    else:
        return render(request, 'admin/login.html')     


def block_user(request,id):
    if request.session.has_key('username'):
        user = User.objects.get(id=id)
        print(user)
        user.is_active = 0
        user.save()
        return redirect('user_control')    
    else:
        return render(request, 'admin/login.html')  

def unblock_user(request,id):
    if request.session.has_key('username'):
        user = User.objects.get(id=id)
        print(user)
        user.is_active = 1
        user.save()
        return redirect('user_control')    
    else:
        return render(request, 'admin/login.html')  



def delete_user(request,id):
    if request.session.has_key('username'):
        user = User.objects.get(id=id)
        cust = Customer.objects.get(user_id=id)
        cust.delete()
        user.delete()
        return redirect('user_control')    
    else:
        return render(request, 'admin/login.html')   


    