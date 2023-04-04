from django.db import models
from home.models import Registration,MyProduct,Address
from customer.models import Cus_address,OrderItem,Order

# Create your models here.


class DelivaryAssign(models.Model):
    boy  = models.ForeignKey(Registration, on_delete=models.SET_NULL,null=True,blank =True)
    farmer = models.ForeignKey(Address, on_delete=models.SET_NULL,null=True,blank =True)
    cart = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    status= models.BooleanField(default=False)
    assigned_date= models.DateTimeField(auto_now_add=True)
