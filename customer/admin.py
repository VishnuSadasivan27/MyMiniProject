from django.contrib import admin
from .models import OrderItem
from .models import Order,Cus_address
# Register your models here.

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Cus_address)