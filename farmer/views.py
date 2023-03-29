from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View
from home.models import MyProduct
from django.shortcuts import redirect, render
from home.models import Registration,Catagory
import subprocess

def Predictproduct(request):
    # run your machine learning script using subprocess
    subprocess.run(['python', 'farmer/Machine_learning_knn.py'])
    return render(request, 'home/farmerhome.html')

class Addproduct(View):
    def get(self,request):
        mycat=Catagory.objects.all()

        return render(request,'farmer/product_add.html',{'mycat':mycat})


class ProductAdd(View):
    def post(self, request):
        Product_name = request.POST.get("product_name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        image = request.FILES.get("primage")
        expirydate = request.POST.get("expiry")
        catagory= request.POST.get("catagory")
        print(Product_name, price, quantity, image, catagory, expirydate)
        data=Catagory.objects.filter(catagory_name=catagory).values('id').get()['id']
        cataid=Catagory.objects.get(id=data)
        print(cataid)
        id=request.session.get('id')
        user = Registration.objects.get(id=id)
        r = MyProduct(Product_name=Product_name , price=price, quantity=quantity, image=image,expirydate=expirydate,catagory=cataid,farmer=user)
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
