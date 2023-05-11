from django.db import models
from home.models import Registration,MyProduct,Address
from customer.models import Cus_address,OrderItem,Order

# Create your models here.


class DelivaryAssign(models.Model):
    boy  = models.ForeignKey(Registration, on_delete=models.SET_NULL,null=True,blank =True)
    farmer = models.ForeignKey(Address, on_delete=models.SET_NULL,null=True,blank =True)
    cart = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    status= models.CharField(max_length=200, default="pending")
    payforfarmer = models.CharField(max_length=200, default="pending")
    payfordelivaryboy = models.CharField(max_length=200, default="pending")
    assigned_date= models.DateTimeField(auto_now_add=True)
    delivarycode= models.CharField(max_length=200)
    placeddate= models.CharField(max_length=200)

class DelivaryBoyLeave(models.Model):
    boy = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.CharField(max_length=100,null=True)
    state= models.CharField(max_length=200,default="pending")
    pincode = models.CharField(max_length=200)
    assigned_date = models.DateTimeField(auto_now_add=True)
    required_date = models.DateTimeField()
