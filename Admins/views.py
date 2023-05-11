from django.http.response import HttpResponse,HttpResponseBadRequest
from django.views import View
import stripe
from django.core.mail import EmailMultiAlternatives
from Agrikart.settings import EMAIL_HOST_USER
from django.conf import settings
from django.core.files.storage import default_storage
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.core import serializers
from home.decorators import user_login_required
from home.models import Registration,Catagory,Address,MyProduct
from delivaryboy.models import DelivaryBoyLeave,DelivaryAssign
from django.contrib import messages
from django.db.models import Q
from customer.models import Order
# Create your views here.
@method_decorator(user_login_required, name='dispatch')
class Farmer_approve(View):
    def get(self,request):
        # val=Address.objects.all().values('first_name','last_name')
        values = Address.objects.filter(user_id__role='Farmer',user_id__status="inactive").all()
        # values=Address.objects.all()
        print(values)
        return render(request,'admin/Farmer_approve.html',{'values':values})
@method_decorator(user_login_required, name='dispatch')
class Addcatagory(View):
    def get(self,request):

        return render(request,'admin/catagory.html')

@method_decorator(user_login_required, name='dispatch')
class Paymentforfarmerview(View):
    def get(self,request):
        values = Address.objects.filter(user_id__role="Farmer", user_id__status='active').all()
        payment= DelivaryAssign.objects.filter(cart_id__product_id__farmer_id__role="Farmer",status='delivered',payforfarmer='pending').all()
        print(payment.count())
        return render(request, 'admin/payforfarmer.html', {'values': values,'payment':payment})


@method_decorator(user_login_required, name='dispatch')
# class Showmypaymentdata(View):
#     def post(self,request):
#         id=request.POST.get('ids')
#         print("my id is",id)
#         # values = list(Address.objects.filter(user_id__role="Farmer", user_id__status='active').all())
#         values = list(Address.objects.filter(user_id__role="Farmer", user_id__status='active').all())
#         payment= DelivaryAssign.objects.filter(cart_id__product_id__farmer_id=id, cart_id__product_id__farmer_id__role="Farmer",status='delivered', payforfarmer='pending').all()
#         pay=DelivaryAssign.objects.filter(cart_id__product_id__farmer_id=id,cart_id__product_id__farmer_id__role="Farmer", status='delivered',payforfarmer='pending').all()
#         # payment = list(DelivaryAssign.objects.filter(cart_id__product_id__farmer_id=id,cart_id__product_id__farmer_id__role="Farmer", status='delivered',payforfarmer='pending').all())
#
#         data = render_to_string('admin/payforfarmer.html', {'values':values,'payment': payment})
#         data = {'values': serializers.serialize('json', values), 'payment': serializers.serialize('json', payment)}
#         return JsonResponse(data)
#         # data = {'values': serializers.serialize('json', values), 'payment': serializers.serialize('json', payment)}
#         # return JsonResponse(data)
#         # return render(request, 'admin/payforfarmer.html', {'values': values,'payment':payment})

class Showmypaymentdata(View):
    def get(self,request,id):

        print("my id is",id)
        # values = list(Address.objects.filter(user_id__role="Farmer", user_id__status='active').all())
        values = list(Address.objects.filter(user_id__role="Farmer", user_id__status='active').all())
        # payment= DelivaryAssign.objects.filter(cart_id__product_id__farmer_id=id, cart_id__product_id__farmer_id__role="Farmer",status='delivered', payforfarmer='pending').all()
        payment=DelivaryAssign.objects.filter(cart_id__product_id__farmer_id=id,cart_id__product_id__farmer_id__role="Farmer", status='delivered',payforfarmer='pending')
        # payment = list(DelivaryAssign.objects.filter(cart_id__product_id__farmer_id=id,cart_id__product_id__farmer_id__role="Farmer", status='delivered',payforfarmer='pending').all())
        print(payment.count())
        total=0
        for i in payment:
            total=total+i.cart.total
        # data = render_to_string('admin/payforfarmer.html', {'values':values,'payment': payment})
        # data = {'values': serializers.serialize('json', values), 'payment': serializers.serialize('json', payment)}
        # return JsonResponse(data)
        # data = {'values': serializers.serialize('json', values), 'payment': serializers.serialize('json', payment)}
        # return JsonResponse(data)
        return render(request, 'admin/showpaymentdata.html', {'values': values,'payment':payment,'total':total,'id':id})


@method_decorator(user_login_required, name='dispatch')
class Deliboyapprove(View):
    def get(self,request):
        values = Address.objects.filter(user_id__role='Delivery_Boy', user_id__status="inactive").all()
        # values=Address.objects.all()
        print(values)
        return render(request,'admin/delivaryboyapprove.html',{'values':values})
@method_decorator(user_login_required, name='dispatch')
class Customerview(View):
    def get(self,request):
        customers = Registration.objects.filter(role="Customer",status='active').values()
        return render(request,'admin/customerview.html',{'customers':customers})

@method_decorator(user_login_required, name='dispatch')
class Deletedcustomer(View):
    def get(self,request):
        customers = Registration.objects.filter(role="Customer",status='inactive').values()
        return render(request,'admin/deletedcustomer.html',{'customers':customers})
@method_decorator(user_login_required, name='dispatch')
class Farmerview(View):
    def get(self,request):
        values = Address.objects.filter(user_id__role="Farmer",user_id__status='active').all()
        return render(request,'admin/farmerview.html',{'values':values})
@method_decorator(user_login_required, name='dispatch')
class Delivaryboyview(View):
    def get(self,request):
        values = Address.objects.filter(user_id__role="Delivery_Boy",user_id__status='active').all()
        return render(request,'admin/delivaryboyview.html',{'values':values})
@method_decorator(user_login_required, name='dispatch')
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

@method_decorator(user_login_required, name='dispatch')
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

@method_decorator(user_login_required, name='dispatch')
class Deactivate(View):
    def get(self,request,id):
        dele=Registration.objects.get(id=id)
        dele.status="inactive"
        print(dele.status)
        dele.save()
        customers = Registration.objects.filter(role='Customer',status="active").values()
        return HttpResponse("<script>alert('Dectivated ');window.location='/Admins/Customerview';</script>")

        return render(request, 'admin/customerview.html', {'customers': customers})

@method_decorator(user_login_required, name='dispatch')
class Activatecustomer(View):
    def get(self, request, id):
        dele = Registration.objects.get(id=id)
        dele.status = "active"
        print(dele.status)
        dele.save()
        customers = Registration.objects.filter(status="inactive",role='Customer').values()
        return HttpResponse("<script>alert('Activated ');window.location='/Admins/Deletecustomer';</script>")
        return render(request,'admin/deletedcustomer.html',{'customers':customers})
@method_decorator(user_login_required, name='dispatch')
class Farmerdeactivate(View):
    def get(self,request,id):
        dele = Registration.objects.get(id=id)
        dele.status = "inactive"
        print(dele.status)
        dele.save()
        values= Address.objects.filter(user_id__status="active",user_id__role='Farmer').all()
        return HttpResponse("<script>alert('Deactivated ');window.location='/Admins/Farmerview';</script>")
        return render(request,'admin/farmerview.html',{'values':values})
@method_decorator(user_login_required, name='dispatch')
class Deliboydeactivate(View):
    def get(self,request,id):
        dele = Registration.objects.get(id=id)
        dele.status = "inactive"
        print(dele.status)
        dele.save()
        values= Address.objects.filter(user_id__status="active",user_id__role='Delivery_Boy').all()
        return render(request,'admin/farmerview.html',{'values':values})

@user_login_required
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

@user_login_required
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

@user_login_required
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

@user_login_required
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
@user_login_required
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
@user_login_required
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
@method_decorator(user_login_required, name='dispatch')
class Adminprofile(View):
    def get(self,request):
        return render(request,'admin/adminprofile.html')

@method_decorator(user_login_required, name='dispatch')
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

@method_decorator(user_login_required, name='dispatch')
class Viewcatagory(View):
    def get(self,request):
        catas=Catagory.objects.all()
        return render(request,'admin/catagoryview.html',{'catas':catas})

@method_decorator(user_login_required, name='dispatch')
class RemoveCatagory(View):
    def post(self, request):
        id = request.POST.get('ids')
        print("remove item id",id)
        cata_id= Catagory.objects.filter(id=id)

        cata_id.delete()
        data={'data':"succees"}
        return JsonResponse(data)

@method_decorator(user_login_required, name='dispatch')
class CatagoryEdit(View):
    def get(self, request,id):
        catagory=Catagory.objects.get(id=id)
        print(catagory.catagory_image)
        return render(request,'admin/catagoryedit.html',{'catagory':catagory})

@method_decorator(user_login_required, name='dispatch')
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


@method_decorator(user_login_required, name='dispatch')
class Allproductview(View):
    def get(self, request):
        product=MyProduct.objects.all()
        return render(request,'admin/allproductview.html',{'product':product})


@method_decorator(user_login_required, name='dispatch')
class Removetheproduct(View):
    def post(self, request):
        id = request.POST.get('ids')
        print("remove item id", id)
        pro_id = MyProduct.objects.filter(id=id)

        pro_id.delete()
        data = {'data': "succees"}
        return JsonResponse(data)
@method_decorator(user_login_required, name='dispatch')
class DelivaryLeaveview(View):
    def get(self,request):
        # val=Address.objects.all().values('first_name','last_name')
        leaves = DelivaryBoyLeave.objects.all()
        # values=Address.objects.all()
        return render(request,'admin/delivaryleaveapplication.html',{'leaves':leaves})

class Approveleave(View):
    def post(self, request):
        id = request.POST.get('ids')
        print("Approveid",id)
        cata_id= DelivaryBoyLeave.objects.get(id=id)

        cata_id.state="Approved"
        cata_id.save()
        data={'data':"succees"}
        return JsonResponse(data)

class DelivaryLeaveview(View):
    def get(self, request):
        # val=Address.objects.all().values('first_name','last_name')
        leaves = DelivaryBoyLeave.objects.filter(state="Cancelled")
        # values=Address.objects.all()
        return render(request, 'admin/delivaryleaveapplication.html', {'leaves': leaves})



class DelivaryCancelledLeave(View):
    def get(self, request):
        # val=Address.objects.all().values('first_name','last_name')
        leaves = DelivaryBoyLeave.objects.filter(state="Cancelled")
        # values=Address.objects.all()
        return render(request, 'admin/delivaryboyleavecancel.html', {'leaves': leaves})

class Deletedelivaryboyleave(View):
    def post(self, request):
        id = request.POST.get('ids')
        print("remove item id",id)
        cata_id=DelivaryBoyLeave.objects.filter(id=id)
        cata_id.delete()
        data={'data':"succees"}
        return JsonResponse(data)

def farmerpayment(request,id):
    print(id)
    payment = DelivaryAssign.objects.filter(cart_id__product_id__farmer_id=id, cart_id__product_id__farmer_id__role="Farmer", status='delivered',payforfarmer='pending')
    # payment = list(DelivaryAssign.objects.filter(cart_id__product_id__farmer_id=id,cart_id__product_id__farmer_id__role="Farmer", status='delivered',payforfarmer='pending').all())
    total = 0
    for i in payment:
        total = total + i.cart.total
    total=int(total*100)
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'unit_amount': total,
                'product_data': {
                    'name': 'Your Cart'
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('farmerthanks', args=[id])) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('Paymentforfarmerview')),
    )

    context = {
        'session_id': session.id,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'total': total
    }
    return render(request, 'admin/userpayment.html', context)


