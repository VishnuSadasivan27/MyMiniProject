from django.db import models
from enum import unique
from django.db import models
from home.models import Registration,MyProduct

import uuid
import datetime

# Create your models here.
class OrderItem(models.Model):
    product = models.ForeignKey(MyProduct, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Order(models.Model):
    customer = models.ForeignKey(Registration, on_delete=models.SET_NULL,null=True,blank =True)
    myorder = models.ForeignKey(OrderItem, on_delete=models.SET_NULL,null=True,blank =True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)
    delivarycharge = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)

