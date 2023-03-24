from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View
from home.models import MyProduct
from django.shortcuts import redirect, render
from home.models import Registration

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
        return HttpResponse("<script>alert('Product Added');window.location='/farmer/Addproduct';</script>")
        return render(request, 'farmer/product_add.html')




class Farmerprofile(View):
    def get(self,request):
        l_id=request.session.get('id')
        print(l_id)
        return render(request,'farmer/farmerprofile.html')


class FarmerChangepassword(View):
    def post(self, request):
        id = request.session.get('id')
        user = Registration.objects.filter(id=id)
        old_pass = request.POST.get("cpassword")
        new_pass1 = request.POST.get("newpassword")
        new_pass2= request.POST.get("renewpassword")
        print(old_pass,new_pass1,new_pass2);
        current_password = Registration.objects.filter(id=id).values('password').get()['password']
        if(old_pass==current_password):
             user.update(password=new_pass1)
             return HttpResponse("<script>alert('Succesfully updated');window.location='Farmerprofile';</script>")
        else:
            return HttpResponse("<script>alert('current password is wrong');window.location='Farmerprofile';</script>")
