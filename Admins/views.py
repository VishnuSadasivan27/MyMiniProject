from django.http.response import HttpResponse,HttpResponseBadRequest
from django.views import View
from django.http import JsonResponse
from django.shortcuts import redirect, render
from home.models import Registration,Catagory,Address
from django.contrib import messages
from django.db.models import Q
from customer.models import Order
# Create your views here.

class Farmer_approve(View):
    def get(self,request):
        # val=Address.objects.all().values('first_name','last_name')
        values = Address.objects.filter(user_id__role='Farmer',user_id__status="inactive").all()
        # values=Address.objects.all()
        print(values)
        return render(request,'admin/Farmer_approve.html',{'values':values})

class Addcatagory(View):
    def get(self,request):

        return render(request,'admin/catagory.html')
class Deliboyapprove(View):
    def get(self,request):
        values = Address.objects.filter(user_id__role='Delivery_Boy', user_id__status="inactive").all()
        # values=Address.objects.all()
        print(values)
        return render(request,'admin/delivaryboyapprove.html',{'values':values})
class Customerview(View):
    def get(self,request):
        customers = Registration.objects.filter(role="Customer",status='active').values()
        return render(request,'admin/customerview.html',{'customers':customers})

class Deletedcustomer(View):
    def get(self,request):
        customers = Registration.objects.filter(role="Customer",status='inactive').values()
        return render(request,'admin/deletedcustomer.html',{'customers':customers})
class Farmerview(View):
    def get(self,request):
        values = Address.objects.filter(user_id__role="Farmer",user_id__status='active').all()
        return render(request,'admin/farmerview.html',{'values':values})
class Delivaryboyview(View):
    def get(self,request):
        values = Address.objects.filter(user_id__role="Delivery_Boy",user_id__status='active').all()
        return render(request,'admin/delivaryboyview.html',{'values':values})
class Deliactivate(View):
   print("entereddddddddddddd")
   def post(self, request):
        pincode = request.POST.get("pincode")
        id = request.POST.get("ids")
        print(pincode)
        print(id)
        dele=Registration.objects.get(id=id)
        boys=Address.objects.get(user_id=id)
        boys.pin=pincode
        boys.save()
        dele.status="active"
        print(dele.status)
        dele.save()
        data={'pincode':pincode}
        return JsonResponse(data)

class Activate(View):
    def get(self,request,id):
        dele=Registration.objects.get(id=id)
        dele.status="active"
        print(dele.status)
        dele.save()
        print(dele.first_name)
        values = Address.objects.filter(user_id__role='Farmer',user_id__status="inactive").all()
        return render(request, 'admin/Farmer_approve.html',{'values': values})

        return HttpResponse("<script>alert('Activated ');window.location='/AdminsFarmer_approval';</script>")

class Deactivate(View):
    def get(self,request,id):
        dele=Registration.objects.get(id=id)
        dele.status="inactive"
        print(dele.status)
        dele.save()
        customers = Registration.objects.filter(role='Customer',status="active").values()
        return HttpResponse("<script>alert('Dectivated ');window.location='/Admins/Customerview';</script>")

        return render(request, 'admin/customerview.html', {'customers': customers})

class Activatecustomer(View):
    def get(self, request, id):
        dele = Registration.objects.get(id=id)
        dele.status = "active"
        print(dele.status)
        dele.save()
        customers = Registration.objects.filter(status="inactive",role='Customer').values()
        return HttpResponse("<script>alert('Activated ');window.location='/Admins/Deletecustomer';</script>")
        return render(request,'admin/deletedcustomer.html',{'customers':customers})
class Farmerdeactivate(View):
    def get(self,request,id):
        dele = Registration.objects.get(id=id)
        dele.status = "inactive"
        print(dele.status)
        dele.save()
        values= Address.objects.filter(user_id__status="active",user_id__role='Farmer').all()
        return HttpResponse("<script>alert('Deactivated ');window.location='/Admins/Farmerview';</script>")
        return render(request,'admin/farmerview.html',{'values':values})
class Deliboydeactivate(View):
    def get(self,request,id):
        dele = Registration.objects.get(id=id)
        dele.status = "inactive"
        print(dele.status)
        dele.save()
        values= Address.objects.filter(user_id__status="active",user_id__role='Delivery_Boy').all()
        return render(request,'admin/farmerview.html',{'values':values})

def customersearchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(first_name=query) | Q(last_name=query))
            customers = Registration.objects.filter(multiple_q,role='Customer',status='active')
            return render(request, 'admin/customerview.html', {'customers':customers})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
            return render(request, 'admin/customerview.html', {})

def customerdsearchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(first_name=query) | Q(last_name=query))
            customers = Registration.objects.filter(multiple_q,role='Customer',status='inactive')
            return render(request, 'admin/deletedcustomer.html', {'customers':customers})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
            return render(request, 'admin/deletedcustomer.html', {})

def farmersearchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(first_name=query) | Q(last_name=query))
            farmers = Registration.objects.filter(multiple_q,role='Farmer',status='active')
            return render(request, 'admin/farmerview.html', {'farmers':farmers})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
            return render(request, 'admin/farmerview.html', {})

def farmerdsearchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(first_name=query) | Q(last_name=query))
            values = Registration.objects.filter(multiple_q,role='Farmer',status='inactive')
            return render(request, 'admin/Farmer_approve.html', {'values':values})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
            return render(request, 'admin/Farmer_approve.html', {})
def Deliboydsearchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(first_name=query) | Q(last_name=query))
            values = Registration.objects.filter(multiple_q,role='Delivery_Boy',status='inactive')
            return render(request, 'admin/delivaryboyapprove.html', {'values':values})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
            return render(request, 'admin/delivaryboyapprove.html', {})
def Deliboysearchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(first_name=query) | Q(last_name=query))
            boys = Registration.objects.filter(multiple_q,role='Delivery_Boy',status='active')
            return render(request, 'admin/delivaryboyview.html', {'boys':boys})
        else:
            messages.info(request, 'No delivary boy with that name!!!')
            print("No information to show")
            return render(request, 'admin/delivaryboyview.html', {})
class Adminprofile(View):
    def get(self,request):
        return render(request,'admin/adminprofile.html')

class Uploadcatagory(View):
    def post(self,request):
        if request.method == 'POST':
            catagoryname=request.POST.get('cataname')
            description=request.POST.get('discription')
            cataimage=request.FILES.get('cataimage')
            if not Catagory.objects.filter(catagory_name=catagoryname).exists():
                cata=Catagory(catagory_name=catagoryname,catagory_image=cataimage,discription=description)
                cata.save()
                return HttpResponse("<script>alert('Product is Added');window.location='/adminhome/';</script>")
            else:
                return HttpResponse("<script>alert('catagory is already exists');window.location='/Admins/Addcatagory';</script>")

                return redirect('')

class Viewcatagory(View):
    def get(self,request):
        catas=Catagory.objects.all()
        return render(request,'admin/catagoryview.html',{'catas':catas})

class RemoveCatagory(View):
    def post(self, request):
        id = request.POST.get('ids')
        print("remove item id",id)
        cata_id= Catagory.objects.filter(id=id)

        cata_id.delete()
        data={'data':"succees"}
        return JsonResponse(data)

class CatagoryEdit(View):
    def get(self, request,id):
        catagory=Catagory.objects.get(id=id)
        print(catagory.catagory_image)
        return render(request,'admin/catagoryedit.html',{'catagory':catagory})

class CatagoryEditSubmit(View):
    def post(self, request,id):
        print(id)
        catagory=Catagory.objects.get(id=id)
        catagories=Catagory.objects.all()
        print("enthadaaa")
        if request.method == 'POST':
            catagoryname = request.POST.get('cataname')
            description = request.POST.get('discription')
            cataimage = request.FILES.get('cataimage')

            if catagory.catagory_name==catagoryname:
                catagory.discription=description
                print(catagory.discription)
                if cataimage==None:
                    catagory.catagory_image=catagory.catagory_image
                    catagory.save()
                    print("haiii")
                    return HttpResponse("<script>alert('Catagory Updated');window.location='/Admins/Viewcatagory'; event.preventDefault();</script>")
                else:
                    catagory.catagory_image=cataimage
                    catagory.save()
                    print("polii")
                    return HttpResponse("<script>alert('Catagory Updated1');window.location='/Admins/Viewcatagory'; event.preventDefault();</script>")
            else:
                for cata in catagories:
                    print(cata.catagory_name)
                    if cata.catagory_name==catagoryname:
                        print("podaaaaa")
                        return HttpResponse("<script>alert('Catagory exist');window.location='/Admins/CatagoryEdit/{0}''; event.preventDefault();</script>".format(id))
                        break

                else:
                    catagory.catagory_name=catagoryname
                    catagory.discription = description
                    if cataimage == None:
                        catagory.catagory_image = catagory.catagory_image
                        print("endaaa")
                        catagory.save()
                        return HttpResponse("<script>alert('Catagory Updated3');window.location='/Admins/Viewcatagory'; event.preventDefault();</script>")
                    else:
                        catagory.catagory_image = cataimage
                        catagory.save()
                        return HttpResponse("<script>alert('Catagory Updated4');window.location='/Admins/Viewcatagory'; event.preventDefault();</script>")

            return HttpResponseBadRequest("Invalid Request")




