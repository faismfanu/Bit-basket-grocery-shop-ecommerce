from django.db import models
from django.db.models import Model 
from django.contrib.auth.models import User 
import datetime
import os 
from django.core.exceptions import ObjectDoesNotExist
from uuid import uuid4
# Create your models here.


class User_profile(models.Model):
    firstname = models.CharField(max_length = 300)
