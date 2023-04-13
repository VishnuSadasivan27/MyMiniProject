from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.utils.decorators import method_decorator
import django.contrib.sessions
from datetime import datetime
from django.template import loader
from .decorators import user_login_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate
import json
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from customer.models import Order, Cus_address
from home.models import Registration, MyProduct, AdminLogin, Address,Catagory
from customer.models import OrderItem


# import js2py
# from home.forms import MyForms
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

    return JsonResponse('Item was added', safe=False)


def searchbar(request):
    if request.method == 'GET':
        query = request.GET.get('text')
        if query:
            multiple_q = Q(Q(Product_name__istartswith=query) | Q(price__istartswith=query))
            datas = MyProduct.objects.filter(multiple_q)
            print(datas)
            return render(request, 'home/store.html', {'datas': datas})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
            return render(request, 'home/store.html', {})


def searchbar_id(request):
    print("Entering... searchbar id")
    if request.method == 'GET':
        query = request.GET.get('search_id')
        print(query)
        if query:
            datas = MyProduct.objects.filter(id=query)
            return render(request, 'home/store.html', {'datas': datas})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
            return render(request, 'home/store.html', {})


def searchbar1(request):
    if request.method == 'GET':
        query = request.GET.get('text')
        if query:
            multiple_q = Q(Q(Product_name__istartswith=query) | Q(price__istartswith=query))
            datas = MyProduct.objects.filter(multiple_q)
            result_list = []
            for prod in datas:
                    result_list.append([prod.id, prod.Product_name, prod.quantity, prod.price,
                                    prod.expirydate, prod.adddate, prod.imageURL])
            return JsonResponse({'datas': result_list, 'X-Frame-Options': 'DENY'}, status=200)
        else:
            return "No search result!!!"


def adminhome(request):
    return render(request, 'home/adminhome.html')


def farmerhome(request):
    person = request.session['id']
    user = Registration.objects.get(id=person)
    totalproduct=MyProduct.objects.filter(farmer_id=user).count()
    print(user.image)
    return render(request, 'home/farmerhome.html', {'user': user,'totalproduct':totalproduct})


def delivaryhome(request):
    person = request.session['id']
    user = Registration.objects.get(id=person)
    print(user.image)
    return render(request, 'delivaryboy/delivaryhome.html',{'user':user})


def index(request):
    return render(request, 'home/home.html')


def Login(request):
    return render(request, 'home/Login.html')

@user_login_required
def signup(request):
    return render(request, 'home/signup.html')


@user_login_required
def store(request,id):
    datas = MyProduct.objects.filter(catagory_id=id,state='active')
    print("ggggggggggggggggggggggggggggggggggggg",datas)
    person = request.session['id']
    user = Registration.objects.get(id=person)
    today = datetime.now().date()
    expired_products = MyProduct.objects.filter(expirydate__lte=today)
    for expiry in expired_products:
        expiry.state='inactive'
        expiry.save()
    print(user.image)
    return render(request, 'home/store.html', {'datas': datas, 'user': user})


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
@method_decorator(user_login_required, name='dispatch')
class Catagorydisplay(View):
    def get(self, request):
        catagory=Catagory.objects.all()
        id = request.session['id']
        user = Registration.objects.get(id=id)
        print(user.image)
        return render(request, 'customer/catagorypage.html', {'catagory':catagory,'user':user})

# customer registration
class CustomerRegistration(View):
    def get(self, request, role):
        print("hai")
        return render(request, 'home/cus_reg.html', {'role': role})


class Submit(View):
    def post(self, request, role):
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone")
        password = request.POST.get("pass")
        if role == "Customer":
            status = "active"
            print(first_name, last_name, email, phone_no, password, role, status)

            if not Registration.objects.filter(email=email).exists():
                print("Not exist")

                # val.user_id = Registration.objects.get()
                # val.first_name = first_name

                r = Registration(first_name=first_name, last_name=last_name, phone_no=phone_no, role=role,
                                 status=status, email=email, password=password)
                r.save()
                # val.password = password
                # val.email = email
                # val.user_id_id = r.id
                # print(val.email, val.password,val.user_id_id)
                # val.save()

                print(first_name, last_name, email, phone_no, password, role, status, email, password)
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
                r = Registration(first_name=first_name, last_name=last_name, phone_no=phone_no, role=role,
                                 status=status, email=email, password=password)
                r.save()
                return HttpResponse("<script>alert('Account has created pls Wait');window.location='/Login/';</script>")
                return render(request, 'home/home.html', {'role': role})
            else:
                return HttpResponse("<script>alert('Email Id already Exist');window.location='//';</script>")
        elif role == "Delivery_Boy":
            status = "inactive"
            print(first_name, last_name, email, phone_no, password, role, status)
            if not Registration.objects.filter(email=email).exists():
                print("Not exist")

                # val.user_id = Registration.objects.get(id)
                # val.first_name = first_name
                # val.password = password
                # val.email = email
                # val.save()
                r = Registration(first_name=first_name, last_name=last_name, phone_no=phone_no, role=role,
                                 status=status, email=email, password=password)
                r.save()
                return HttpResponse(
                    "<script>alert('Account has created pls Wait');window.location='/Login/';</script>")
                return render(request, 'home/home.html', {'role': role})
            else:
                return HttpResponse("<script>alert('Email Id already Exist');window.location='//';</script>")

                # error = "Email already exist"
                # return render(request,"home/error.html",{'error':error})
            # v = Validation(password = password,email= email)
            # v.save()


class LoginPage(View):
    def post(self, request):
        # request.session['email'] = 'null'
        print("hello")
        username = request.POST.get("your_name")
        password = request.POST.get("your_pass")
        if AdminLogin.objects.filter(email=username, password=password).exists():
            admin_login = AdminLogin.objects.filter(email=username, password=password)
            print(admin_login)
            for admin in admin_login:
                email = admin.email
                request.session['email'] = admin.email
                request.session['password'] = admin.password
                request.session['id'] = admin.id
                print(email)
                customers = Registration.objects.filter(role="Customer", status='active').values()
                count = customers.count()
                print(count)
            # cond = Registration.objects.all()
            return HttpResponse("<script>alert('login  Successfull');window.location='/adminhome/';</script>")

        elif Registration.objects.filter(email=username, password=password, role='Customer', status='active').exists():
            customer_login = Registration.objects.filter(email=username, password=password)
            print(customer_login)
            for admin in customer_login:
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
                return redirect('Catagorydisplay')
        elif Registration.objects.filter(email=username, password=password, role='Farmer').exists():
            if Registration.objects.filter(email=username, password=password).exists():
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
        elif Registration.objects.filter(email=username, password=password, role='Delivery_Boy').exists():
            if Registration.objects.filter(email=username, password=password).exists():
                deli_login = Registration.objects.filter(email=username, password=password)
                print(deli_login)
                for admin in deli_login:
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
                    return redirect('delivaryhome')
                # return HttpResponse("<script>alert('Successfull');window.location='/farmerhome/';</script>")
                # return render(request, "{% url 'store' %}")
                # print("login")
            else:
                return HttpResponse("<script>alert('Please wait for approval');window.location='/Login/';</script>")
        else:
            return HttpResponse("<script>alert('Unsuccessfull..Invalid credential');window.location='/Login/';</script>")
            error = "Invalid Username or Password"
            return render(request, "home/error.html", {'error': error})


class Logout(View):
    def get(self, request):
        for sesskey in request.session.keys():
            del request.session[sesskey]
            logout(request)
            return redirect('Login')


@method_decorator(user_login_required, name='dispatch')
class Orderaddress(View):
    def post(self, request):
        cus_id = request.session.get('id')

        # user= Cus_address.objects.filter(customer_id=cus_id)
        address = request.POST.get("address")
        district = request.POST.get("district")
        panchayat = request.POST.get("panchayat")
        city = request.POST.get("city")
        landmark = request.POST.get("landmark")
        pincode = request.POST.get("pincode")
        phone = request.POST.get("phone")

        r = Cus_address(customer_id=cus_id, address=address, district=district, panchayat=panchayat, city=city,
                        pincode=pincode, landmark=landmark, phone=phone)
        r.save()
        if not Address.objects.filter(user_id=cus_id).exists():
            print(cus_id, address, panchayat, city, pincode, phone)
            add = Address(address=address, panchayat=panchayat, district=district, city=city, pin=pincode,
                          landmark=landmark, user_id=cus_id)
            add.save()
            return redirect('payment')
        else:
            user = Address.objects.get(user_id=cus_id)
            user.address = address
            user.panchayat = panchayat
            user.city = city
            user.pin = pincode
            user.landmark = landmark
            user.save()
            return redirect('payment')


@method_decorator(user_login_required, name='dispatch')
class Changepassword(View):
    def post(self, request):
        id = request.session.get('id')
        user = Registration.objects.filter(id=id)
        old_pass = request.POST.get("cpassword")
        new_pass1 = request.POST.get("newpassword")
        new_pass2 = request.POST.get("renewpassword")
        print(old_pass, new_pass1, new_pass2);
        current_password = Registration.objects.filter(id=id).values('password').get()['password']
        if (new_pass1 == new_pass2):
            if (old_pass == current_password):
                user.update(password=new_pass1)
                return HttpResponse(
                    "<script>alert('Succesfully updated');window.location='customercustomerprofile';</script>")
            else:
                return HttpResponse(
                    "<script>alert('current password is wrong');window.location='customercustomerprofile';</script>")
        else:
            return HttpResponse("<script>alert('Re-entered Password is wrong');window.location='/Admins/Adminprofile';</script>")



@method_decorator(user_login_required, name='dispatch')
class AdminPasswordchange(View):
    def post(self, request):
        id = request.session.get('id')
        print(id)
        user = AdminLogin.objects.filter(id=id)
        old_pass = request.POST.get("cpassword")
        new_pass1 = request.POST.get("newpassword")
        new_pass2 = request.POST.get("renewpassword")
        print(old_pass, new_pass1, new_pass2);
        current_password = AdminLogin.objects.filter(id=id).values('password').get()['password']
        if (new_pass1==new_pass2):
            if (old_pass == current_password):
                user.update(password=new_pass1)
                return HttpResponse(
                    "<script>alert('Succesfully updated');window.location='/Admins/Adminprofile';</script>")
            else:
                return HttpResponse("<script>alert('current password is wrong');window.location='/Admins/Adminprofile';</script>")
        else:
            return HttpResponse("<script>alert('Re-entered Password is wrong');window.location='/Admins/Adminprofile';</script>")

# class MyProduct(View):
#     model = MyProduct
#     def get(self,request):
#         queryset = MyProduct.objects.all()
#         return render(request,"home/text.html",{'queryset':queryset})

# email = "admin@gmail.com"
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
