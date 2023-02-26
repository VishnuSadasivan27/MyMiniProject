from django.contrib import admin
from .models import Registration
from .models import MyProduct
from .models import Address
from .models import Review
from .models import AdminLogin

 # Register your models here.
admin.site.register(Registration)
admin.site.register(MyProduct)
admin.site.register(AdminLogin)

admin.site.register(Address)
admin.site.register(Review)