from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Dealers
from dealer.models import *
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
        if user=='faismfanu' and password=='faism9922':
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
        return render(request,"admin/adminpanel.html")
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
            print(image_data)
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
    order = Order.objects.all()
    dealers =Dealers.objects.all()
    # order = dealers.orderItem_set.all()
    # print(order)
    return render(request, 'admin/admin_orders.html',{'order':order,'dealers':dealers})

       

def dealers(request):
    if request.session.has_key('username'):
        dealers = Dealers.objects.all()
        print(dealers)
        return render(request,"admin/dealers.html",{"dealers":dealers})
    else:
        return render(request, 'admin/login.html')

def base(request):
    return render(request,"admin/base.html")

        
        
def adminlogout(request):
    if request.session.has_key('username'):
        request.session.delete()
        return redirect('adminlogin')
    else:
        return render(request, 'admin/login.html')
    