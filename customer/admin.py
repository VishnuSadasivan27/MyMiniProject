from django.contrib import admin
from .models import OrderItem
from .models import Order
# Register your models here.

admin.site.register(OrderItem)
admin.site.register(Order)