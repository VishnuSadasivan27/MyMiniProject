from _decimal import Decimal
from django.http.response import HttpResponse
from django.views import View
import stripe
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.urls import reverse
from home.decorators import user_login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from home.models import MyProduct
from customer.models import OrderItem,Cus_address
from home.models import Address
from django.shortcuts import redirect, render
from home.views import Registration
from customer.models import Order

from django.views.decorators.csrf import csrf_protect
stripe.api_key = settings.STRIPE_PRIVATE_KEY



def user_login_required(function):
    def wrapper(request, login_url='Login', *args, **kwargs):
        if not 'email' in request.session:
            return redirect(login_url)
        else:
            return function(request, *args, **kwargs)

    return wrapper


@csrf_protect
def plusqty(request):
    id = request.POST.get('ids')
    print("my id is",id)
    user = request.session.get('id')
    carts = OrderItem.objects.filter(customer_id=user)
    cart = get_object_or_404(OrderItem, id=id)

    if int(cart.product.quantity) > cart.quantity:
        cart.quantity += 1
        cart.total = Decimal(str(cart.quantity)) * Decimal(str(cart.product.price))
        print(cart.total)
        print(cart.quantity)
        cart.save()
        total1= 0
        for i in carts:
            print(i)
            total1 += int(i.total)
        print("The rotal",total1)
        shipping = total1 + 50

        data = {'quantity': cart.quantity, 'total': cart.total, 'total1': total1, 'shipping': shipping}
        return JsonResponse(data)
    else:
        data = {'error': 'Out of Stock'}
        return JsonResponse(data, status=400)

def minusqty(request):
    id = request.POST.get('ids')
    print("my id is",id)
    user = request.session.get('id')
    carts = OrderItem.objects.filter(customer_id=user)
    cart = get_object_or_404(OrderItem, id=id)

    if int(cart.product.quantity) > 1:
        cart.quantity -= 1
        cart.total = Decimal(str(cart.quantity)) * Decimal(str(cart.product.price))
        print(cart.total)
        print(cart.quantity)
        cart.save()
        total1 = 0
        for i in carts:
            print(i)
            total1 += int(i.total)
        print("The rotal", total1)
        shipping=total1+50

        data = {'quantity': cart.quantity, 'total': cart.total, 'total1': total1,'shipping':shipping}
        return JsonResponse(data)
    else:
        data = {'error': 'Out of Stock'}
        return JsonResponse(data, status=400)
@user_login_required
def plusqty1(request,id):
    carts=OrderItem.objects.filter(id=id)
    print("hello",carts)
    for cart in carts:

        if int(cart.product.quantity) > cart.quantity:
            cart.quantity +=1
            cart.total = int(cart.quantity) * int(cart.product.price)

            cart.save()
            return redirect('ViewCart')
        # messages.success(request, 'Out of Stock')
        return redirect('ViewCart')




# @user_login_required
# def minusqty(request,id):
#     carts=OrderItem.objects.filter(id=id)
#     print("hello",carts)
#     for cart in carts:
#
#         if int(cart.quantity) > 1:
#             cart.quantity =cart.quantity-1;
#             cart.total = int(cart.quantity) * int(cart.product.price)
#
#             cart.save()
#             return redirect('ViewCart')
#         # messages.success(request, 'Out of Stock')
#         return redirect('ViewCart')
@method_decorator(user_login_required, name='dispatch')
class Checkout(View):
    def get(self,request):
        id=request.session.get('id')
        carts = OrderItem.objects.filter(customer_id=id)
        print(carts)
        print("heyyyyyyyiww",id)

        total = 0
        for i in carts:
            print(i)
            total +=int( i.total )
        print(total)
        user=Registration.objects.get(id=id)
        address=Address.objects.get(user_id=id)

        return render(request,'customer/checkout.html',{'total':total,'user':user,'address':address})

@method_decorator(user_login_required, name='dispatch')
class Cart(View):
    def get(self, request):
        user = Registration.objects.get(id=id)
        return render(request, 'customer/cart.html',{'user':user})
@method_decorator(user_login_required, name='dispatch')
class Customerprofile(View):
    def get(self,request):
        id=request.session.get('id')
        user = Registration.objects.get(id=id)
        address=Address.objects.get(user_id=id)
        print(user)
        context={'user':user,'address':address}
        return render(request,'customer/customerprofile.html',context)
@method_decorator(user_login_required, name='dispatch')
class AddCart(View):
    def get(self, request,id):
            # cart = MyProduct.objects.filter(id=id)
            customer = request.session.get('id')
            # print(cart)
            print(customer)
            addcart=OrderItem(product_id=id,customer_id=customer)
            addcart.total=int(addcart.total)+int(addcart.product.price)

            addcart.totalproductcost = int(addcart.totalproductcost) + int(addcart.total)
            print("deyyyyyyyyyyyyyyyyyyyyy",addcart.totalproductcost)


            addcart.save()
            # order, created = Order.objects.get_or_create(customer=customer, complete=False)
            # items = Order.orderitem_set.all()
            # items = []
            # context = {'items': items}
            return redirect('ViewCart')
@method_decorator(user_login_required, name='dispatch')
class ViewCart(View):
    def get(self, request):
            # cart = MyProduct.objects.filter(id=id)
            customer = request.session.get('id')
            cartitem=OrderItem.objects.filter(customer_id=customer)

            print(cartitem)
            print(customer)
            total1=0
            for i in cartitem:
                total1 += int(i.total)
            shipping = total1 + 50
            user = Registration.objects.get(id=customer)
            return render(request, 'customer/cart.html',{'items': cartitem,'user':user,'total1':total1,'shipping':shipping})
@method_decorator(user_login_required, name='dispatch')
class RemoveCart(View):
    def get(self, request,id):
        cart_id= OrderItem.objects.get(id=id)
        cart_id.delete()
        return redirect('ViewCart')


@user_login_required
def payment(request):
    id = request.session.get('id')
    carts = OrderItem.objects.filter(customer_id=id)
    user = Registration.objects.get(id=id)

    total1 = 0
    for i in carts:
        total1 += int(i.total)

    total=total1*100

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
        success_url=request.build_absolute_uri(reverse('thanks')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('ViewCart')),
    )

    context = {
        'session_id': session.id,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'user': user,
        'total': total
    }
    return render(request, 'customer/payment.html', context)
@user_login_required
def thanks(request):
    cus_id = request.session.get('id')
    cartitem = Cus_address.objects.filter(customer_id=cus_id)
    complete="True"
    a=Order(customer_id=cus_id,complete=complete)
    print(cus_id,complete)
    a.save()
    user=Registration.objects.get(id=cus_id)
    return render(request, 'customer/thanks.html',{'user':user})
@method_decorator(user_login_required, name='dispatch')
class Updatecustomer(View):
    def post(self, request):
        pimage = request.FILES.get("pimage")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        email = request.POST.get("email")
        phone_no = ','.join(request.POST.getlist("phone"))
        print(first_name, last_name, email, phone_no, pimage)
        id = request.session.get('id')
        user = Registration.objects.get(id=id)
        user.first_name = first_name
        user.last_name = last_name
        user.phone_no = phone_no
        user.email = email
        user.image = pimage
        user.save()
        print(user.image)
        context = {'user': user}
        return render(request,'customer/customerprofile.html',context)
@method_decorator(user_login_required, name='dispatch')
class Addaddress(View):
    def post(self, request):
        id = request.session['id']
        if not Address.objects.filter(user_id=id).exists():
            address = request.POST.get("Address")
            District = request.POST.get("District")
            panchayat = request.POST.get("panchayat")
            city = request.POST.get("city")
            landmark = request.POST.get("landmark")
            pincode = request.POST.get("pincode")

            r=Address(address=address,district=District,panchayat=panchayat,city=city,landmark=landmark,pin=pincode,user_id=id)
            r.save()
            address = Address.objects.get(user_id=id)
            user = Registration.objects.get(id=id)
            context={'address':address,'user':user}
            return render(request, 'customer/customerprofile.html', context)
        else:
            address = request.POST.get("Address")
            District = request.POST.get("District")
            panchayat = request.POST.get("panchayat")
            city = request.POST.get("city")
            landmark = request.POST.get("landmark")
            pincode = request.POST.get("pincode")
            user = Address.objects.get(user_id=id)
            user.address = address
            user.district = District
            user.panchayat = panchayat
            user.city = city
            user.landmark = landmark
            user.pin=pincode
            user.save()
            address = Address.objects.get(user_id=id)
            user = Registration.objects.get(id=id)
            context={'address':address,'user':user}
            return render(request, 'customer/customerprofile.html', context)