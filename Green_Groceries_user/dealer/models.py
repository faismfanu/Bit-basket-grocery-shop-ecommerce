from django.db import models
from ad.models import *
from django.db.models import Max
from django.contrib.auth.models import User 
# Create your models here.



class Product(models.Model):
    id=models.AutoField(primary_key=True)
    dealer = models.ForeignKey(Dealers, on_delete = models.CASCADE, null = True, blank = True)
    product_category = models.CharField(max_length = 300)
    name = models.CharField(max_length = 300)
    newprice = models.FloatField(null=True)
    offer_price = models.FloatField(null=True)
    offer_percentage = models.IntegerField(null=True)
    product_type = models.CharField(max_length = 300, null= True)
    product_image =  models.FileField(max_length=2555,null=True,blank=True,upload_to='product/images')
    stock = models.IntegerField()
    digital = models.BooleanField(default=False , blank=True)
    description = models.TextField(max_length=1000, verbose_name ='description')


    def __str__(self):
        return self.name

class Product_images(models.Model):
    id=models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.FileField(max_length=2555,upload_to='product/images')

    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200,null = True)
    email = models.CharField(max_length= 200, null = True)
    profile_image = models.ImageField(max_length=10000, null = True,blank = True,upload_to='profile_photos')
    reff_code = models.CharField(max_length=100, null= True)
    refferd_user = models.CharField(max_length=150, null= True)
 
    def _str_(self):
        return self.id





class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank= True, null=True)
    dealer = models.ForeignKey(Dealers, on_delete=models.SET_NULL,blank= True, null=True)
    date_ordered = models.DateField(auto_now=True)
    complete = models.BooleanField(default=False,blank=False)
    transaction_id = models.CharField(max_length = 200, null = True )
    product_total = models.FloatField(default=0, null = True )
    order_status = models.CharField(default = 'Pending',max_length = 200, null = True )

    def _str_(self):
        return str(self.id)

    def __unicode__(self):
        return self.id

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping    

    @property
    def get_cart_total(self):
        orderitems =  self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total   

    @property
    def get_cart_items(self):
        orderitems =  self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total       


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank = True, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank = True, null = True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        if self.id is None: 
            return None
        total = self.product.newprice * self.quantity
        return total


class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank= True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank = True, null = True)
    address = models.CharField(max_length = 200,null = True)
    city = models.CharField(max_length = 200,null = True)
    state = models.CharField(max_length = 200,null = True)
    pincode = models.CharField(max_length = 200,null = True)
    country = models.CharField(max_length = 200,null = True)
    date_added = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=300, null=True)
    payment_cod = models.CharField(max_length=300, null=True)


    def _str_(self):
        return self.address



class offer(models.Model):
    offer_image = models.FileField(max_length=2555,null=True,blank=True,upload_to='offer')
    offer_name = models.CharField(max_length= 220, null=True)
    offer_type = models.CharField(max_length= 220, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    dealer = models.ForeignKey(Dealers,on_delete=models.CASCADE,null=True)
    catogery = models.ForeignKey(catogeries,on_delete=models.CASCADE,null=True)
    discount_amount = models.FloatField(null=True)
    offer_start = models.DateField(auto_now_add=True, null=True)
    offer_expiry = models.DateField(null=True)
    






