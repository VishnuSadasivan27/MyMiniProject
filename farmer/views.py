from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View
from home.models import MyProduct
from django.shortcuts import redirect, render

# Create your views here.
class Addproduct(View):
    def get(self,request):
        return render(request,'farmer/product_add.html')


class ProductAdd(View):
    def post(self, request):
        Product_name = request.POST.get("pname")
        price = request.POST.get("pprice")
        quantity = request.POST.get("quantity")
        image = request.FILES.get("pimage")
        adddate = request.POST.get("adddate")
        expirydate = request.POST.get("expiry")
        print(Product_name, price, quantity, image, adddate, expirydate)
        r = MyProduct(Product_name=Product_name , price=price, quantity=quantity, image=image, adddate=adddate,expirydate=expirydate)

        r.save()
        return render(request, 'farmer/product_add.html')

class Farmerprofile(View):
    def get(self,request):
        l_id=request.session.get('id')
        print(l_id)
        return render(request,'farmer/farmerprofile.html')


