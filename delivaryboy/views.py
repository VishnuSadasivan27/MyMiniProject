from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from home.models import MyProduct
from customer.models import OrderItem
from django.shortcuts import redirect, render
from home.views import Registration
from customer.models import Order,Cus_address
# Create your views here.
class Deliboyprofile(View):
    def get(self,request):
        l_id=request.session.get('id')
        print(l_id)
        return render(request,'delivaryboy/deliboyprofile.html')

class Viewmyjob(View):
    def get(self,request):
        l_id = request.session.get('first_name')
        print(l_id)
        if l_id=="joyel":
            orders=Cus_address.objects.filter(pincode="686513")
            return render(request, 'delivaryboy/myjob.html',{'orders':orders})
        else:
            return render(request, 'delivaryboy/myjob.html')
