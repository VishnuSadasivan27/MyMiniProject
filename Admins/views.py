from django.http.response import HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from home.models import Registration
from django.contrib import messages
from django.db.models import Q
from customer.models import Order
# Create your views here.

class Farmer_approve(View):
    def get(self,request):
        values = Registration.objects.filter(role='Farmer',status="inactive").values()
        return render(request,'admin/Farmer_approve.html',{'values':values})
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
        farmers = Registration.objects.filter(role="Farmer",status='active').values()
        return render(request,'admin/farmerview.html',{'farmers':farmers})

class Activate(View):
    def get(self,request,id):
        dele=Registration.objects.get(id=id)
        dele.status="active"
        print(dele.status)
        dele.save()
        values = Registration.objects.filter(role='Farmer',status="inactive").values()
        return render(request, 'admin/Farmer_approve.html',{'values': values})

        return HttpResponse("<script>alert('Activated ');window.location='/AdminsFarmer_approval';</script>")

class Deactivate(View):
    def get(self,request,id):
        dele=Registration.objects.get(id=id)
        dele.status="inactive"
        print(dele.status)
        dele.save()
        customers = Registration.objects.filter(role='Customer',status="active").values()
        return render(request, 'admin/customerview.html', {'customers': customers})

        return HttpResponse("<script>alert('Activated ');window.location='/AdminsFarmer_approval';</script>")
class Activatecustomer(View):
    def get(self, request, id):
        dele = Registration.objects.get(id=id)
        dele.status = "active"
        print(dele.status)
        dele.save()
        customers = Registration.objects.filter(status="inactive",role='Customer').values()
        return render(request,'admin/deletedcustomer.html',{'customers':customers})
class Farmerdeactivate(View):
    def get(self,request,id):
        dele = Registration.objects.get(id=id)
        dele.status = "inactive"
        print(dele.status)
        dele.save()
        farmers= Registration.objects.filter(status="active", role='Farmer').values()
        return render(request,'admin/farmerview.html',{'farmers':farmers})

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


class Adminprofile(View):
    def get(self,request):
        return render(request,'admin/adminprofile.html')



