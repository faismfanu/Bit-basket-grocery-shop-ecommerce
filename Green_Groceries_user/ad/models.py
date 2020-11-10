from django.db import models
from django.db.models import Model 
from django.contrib.auth.models import User 
import datetime
import os 
from django.core.exceptions import ObjectDoesNotExist
from uuid import uuid4
# Create your models here.

class Dealers(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    dealer_name = models.CharField(null = True, max_length=225)
    dealer_phone = models.CharField(null = True, max_length=225)
    dealer_address = models.CharField(null = True, max_length=225)
    dealer_website = models.CharField(null = True, max_length=225)
    shop_image = models.ImageField(max_length=10000, null = True,blank = True)
    shop_name = models.CharField(null = True, max_length=225)
    shop_number = models.CharField(null = True, max_length=225)
    shop_location = models.CharField(null = True, max_length=225)
    shop_place = models.CharField(null = True, max_length=225)
    shop_opening_time = models.TimeField(null = True, max_length=225)
    shop_closing_time = models.TimeField(null = True, max_length=225)


    
