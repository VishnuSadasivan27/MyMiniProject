from django.http.response import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import django.contrib.sessions
from django.template import loader
from django.http import JsonResponse
from django.contrib.auth import authenticate
import json
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from customer.models import Order
from home.models import Registration,MyProduct,AdminLogin
# import js2py
from home.forms import MyForms
# CustomerForm,FarmerForm,DeliverForm

# from home.models import Users
# from django.contrib.auth.models import User
# Create your views here.
def updateItem(request):
    data = json.loads(request.data)
    ProductId = data['ProductId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', ProductId)
    customer = request.user.customer
    product = MyProduct.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

    return JsonResponse('Item was added',safe = False)
def searchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(Product_name=query) | Q(price=query))
            datas = MyProduct.objects.filter(multiple_q)
            return render(request, 'home/store.html', {'datas':datas})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
            return render(request, 'home/store.html', {})

def adminhome(request):
    return render(request,'home/adminhome.html')
def farmerhome(request):
    return render(request,'home/farmerhome.html')
def index(request):
    return render(request,'home/home.html')
def Login(request):
    return render(request,'home/Login.html')
def signup(request):
    return render(request,'home/signup.html')

def store(request):
    datas = MyProduct.objects.all()
    return render(request,'home/store.html',{'datas':datas})

# def cart(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#     else:
#         # Create empty cart for now for non-logged in user
#         items = []
#     context = {'items': items}
#     return render(request, 'store/cart.html', context)



#customer registration
class CustomerRegistration(View):
    def get(self, request,role):
       print("hai")
       return render(request, 'home/cus_reg.html',{'role':role})


class Submit(View):
    def post(self,request,role):
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone")
        password = request.POST.get("pass")
        if role == "Customer":
            status="active"
            print(first_name, last_name, email, phone_no, password, role, status)

            if not Registration.objects.filter(email=email).exists():
                print("Not exist")

                # val.user_id = Registration.objects.get()
                # val.first_name = first_name

                r = Registration(first_name=first_name, last_name=last_name, phone_no=phone_no, role=role, status=status,email=email,password=password)
                r.save()
                # val.password = password
                # val.email = email
                # val.user_id_id = r.id
                # print(val.email, val.password,val.user_id_id)
                # val.save()

                print(first_name, last_name, email, phone_no, password, role, status,email,password)
                return HttpResponse("<script>alert('Your Account has  created');window.location='/Login/';</script>")
                return render(request, 'home/home.html', {'role': role})
            else:
                return HttpResponse("<script>alert('Email Id already Exist');window.location='//';</script>")
        elif role == "Farmer":
            status = "inactive"
            print(first_name, last_name, email, phone_no, password, role, status)
            if not Registration.objects.filter(email=email).exists():
                print("Not exist")

                # val.user_id = Registration.objects.get(id)
                # val.first_name = first_name
                # val.password = password
                # val.email = email
                # val.save()
                r = Registration(first_name=first_name, last_name=last_name, phone_no=phone_no, role=role,status=status,email=email,password=password)
                r.save()
                return HttpResponse("<script>alert('Account has created pls Wait');window.location='/Login/';</script>")
                return render(request, 'home/home.html', {'role': role})
            else:
                return HttpResponse("<script>alert('Email Id already Exist');window.location='//';</script>")

                # error = "Email already exist"
                # return render(request,"home/error.html",{'error':error})
            # v = Validation(password = password,email= email)
            # v.save()

class LoginPage(View):
    def post(self,request):
        # request.session['email'] = 'null'
        print("hello")
        username = request.POST.get("your_name")
        password = request.POST.get("your_pass")
        if AdminLogin.objects.filter(email=username, password=password).exists():
            admin_login= AdminLogin.objects.filter(email=username,password=password)
            print(admin_login)
            for admin in admin_login:
                email=admin.email
                request.session['email']=admin.email
                request.session['password'] = admin.password
                print(email)
                customers = Registration.objects.filter(role="Customer", status='active').values()
                count=customers.count()
                print(count)
            # cond = Registration.objects.all()
            return HttpResponse("<script>alert('login  Successfull');window.location='/adminhome/';</script>")

        elif Registration.objects.filter(email=username,password=password,role='Customer',status='active').exists():
            customer_login = Registration.objects.filter(email=username, password=password)
            print(customer_login)
            for admin in customer_login:
                email = admin.email
                id=admin.first_name
                print(id)
                request.session['email'] = admin.email
                request.session['password'] = admin.password
                request.session['first_name'] = admin.first_name
                request.session['last_name'] = admin.last_name
                request.session['role'] = admin.role
                request.session['phone_no'] = admin.phone_no
                request.session['id'] = admin.id


                messages.warning(request,'Successfully Logged')
                return redirect('store')
        elif Registration.objects.filter(email=username, password=password, role='Farmer').exists():
           if Registration.objects.filter(email=username, password=password,status='active').exists():
               farmer_login = Registration.objects.filter(email=username, password=password)
               print(farmer_login)
               for admin in farmer_login:
                   email = admin.email
                   id = admin.first_name
                   print(id)
                   request.session['email'] = admin.email
                   request.session['password'] = admin.password
                   request.session['first_name'] = admin.first_name
                   request.session['last_name'] = admin.last_name
                   request.session['role'] = admin.role
                   request.session['phone_no'] = admin.phone_no
                   request.session['id'] = admin.id
                   messages.warning(request, 'Successfully Logged')
                   return redirect('farmerhome')
               # return HttpResponse("<script>alert('Successfull');window.location='/farmerhome/';</script>")
               # return render(request, "{% url 'store' %}")
               # print("login")
           else:
               return HttpResponse("<script>alert('Please wait for approval');window.location='/Login/';</script>")
        else:
            return HttpResponse("<script>alert('Unsuccessfull..Invalid credential');window.location='/Login/';</script>")
            error="Invalid Username or Password"
            return render(request,"home/error.html",{'error':error})

class Logout(View):
    def get(self,request):
        for sesskey in request.session.keys():
            del request.session[sesskey]
            logout(request)
            return redirect('Login')
# class MyProduct(View):
#     model = MyProduct
#     def get(self,request):
#         queryset = MyProduct.objects.all()
#         return render(request,"home/text.html",{'queryset':queryset})

# # email = "admin@gmail.com"
# password = "admin@123"
# r = AdminLogin(email=email,password=password)
# print(email,password)
# r.save()
# Product_name="Carrot"
# price= "100"
# quantity = "50"
# image = "E:\images\placeholder_2"
# adddate = "2022-04-23"
# expirydate ="2022-04-22"
#
# r = Product(Product_name=Product_name, price=price, quantity=quantity, image=image, adddate=adddate,expirydate=expirydate)
# r.save()

