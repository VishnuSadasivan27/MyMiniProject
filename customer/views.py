from _decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.core.mail import EmailMultiAlternatives
from Agrikart.settings import EMAIL_HOST_USER
from django.views import View
import stripe
import requests
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.urls import reverse
from home.decorators import user_login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from home.models import MyProduct,MyAnalysisProduct
from customer.models import OrderItem,Cus_address
from delivaryboy.models import DelivaryAssign
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
    pro= OrderItem.objects.filter(id=id).values('product').get()['product']
    print(pro)
    print(cart.product.quantity)
    print(cart.quantity)
    if (int (cart.product.quantity) != 0):
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
        value = MyProduct.objects.get(id=pro)
        value.quantity=int(value.quantity)-1
        print(value.quantity)

        value.save()
        data = {'quantity': cart.quantity, 'total': cart.total, 'total1': total1,'shipping':shipping}
        return JsonResponse(data)
    else:
        data = {'error': 'Out of Stock'}
        return JsonResponse(data, status=400)

def minusqty(request):
    id = request.POST.get('ids')
    print("my id is",id)
    user = request.session.get('id')
    carts = OrderItem.objects.filter(customer_id=user)
    pro= OrderItem.objects.filter(id=id).values('product').get()['product']
    print(pro)

    cart = get_object_or_404(OrderItem, id=id)


    if int(cart.quantity) >= 1:
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
        value = MyProduct.objects.get(id=pro)
        value.quantity=int(value.quantity)+1
        print(value.quantity)
        value.save()
        data = {'quantity': cart.quantity, 'total': cart.total, 'total1': total1,'shipping':shipping,'value':value.quantity}
        return JsonResponse(data)
    else:
        data = {'error': 'negative is not applicable'}
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
        user = Registration.objects.get(id=id)
        carts = OrderItem.objects.filter(customer_id=id)
        if Address.objects.filter(user_id=id):
            print(carts)
            print("heyyyyyyyiww",id)

            total = 0
            for i in carts:
                print(i)
                total +=int( i.total )
            total=total+50
            print(total)
            address=Address.objects.get(user_id=id)

            return render(request,'customer/checkout.html',{'total':total,'user':user,'address':address})
        else:
            total = 0
            for i in carts:
                print(i)
                total += int(i.total)
            total = total + 50
            print(total)
            return render(request, 'customer/checkout.html', {'user': user,'total':total})

@method_decorator(user_login_required, name='dispatch')
class Cart(View):
    def get(self, request):
        user = Registration.objects.get(id=id)
        return render(request, 'customer/cart.html',{'user':user})
@method_decorator(user_login_required, name='dispatch')
class Customerprofile(View):
    def get(self,request):
        id=request.session.get('id')
        if Address.objects.filter(user_id=id).exists():
            user = Registration.objects.get(id=id)
            address=Address.objects.get(user_id=id)
            print(user)
            context={'user':user,'address':address}
            return render(request,'customer/customerprofile.html',context)
        else:
            user = Registration.objects.get(id=id)
            print(user)
            context = {'user': user}
            return render(request, 'customer/customerprofile.html', context)
@method_decorator(user_login_required, name='dispatch')
class AddCart(View):
    def get(self, request,id):
            # cart = MyProduct.objects.filter(id=id)
            customer = request.session.get('id')
            # print(cart)
            print(customer)
            if OrderItem.objects.filter(product_id=id,customer_id=customer).exists():
                return HttpResponse("<script>alert('Products already exists in cart');window.location='/customer/ViewCart';</script>")
            else:
                product=MyProduct.objects.get(id=id)
                quantity = MyProduct.objects.filter(id=id).values('quantity').get()['quantity']
                product.quantity=int(product.quantity)-1
                product.save()
                addcart=OrderItem(product_id=id,customer_id=customer,quantity=1)
                addcart.total=int(addcart.total)+int(addcart.product.price)

                addcart.totalproductcost = int(addcart.totalproductcost) + int(addcart.total)
                print("deyyyyyyyyyyyyyyyyyyyyy",addcart.totalproductcost)


                addcart.save()

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
    def post(self, request):
        id = request.POST.get('ids')
        print("remove item id",id)
        customer=request.session.get('id')
        cart_id= OrderItem.objects.filter(id=id)
        cart_quantity= OrderItem.objects.filter(id=id).values('quantity').get()['quantity']
        cart = OrderItem.objects.filter(customer_id=customer)
        pro = OrderItem.objects.filter(id=id).values('product').get()['product']
        value=MyProduct.objects.get(id=pro)
        cart_id.delete()
        value.quantity=int(value.quantity)+cart_quantity
        print(value.quantity)
        value.save()
        total1 = 0
        for i in cart:
            total1 += int(i.total)
        shipping = total1 + 50
        print(shipping)
        data={'total1':total1,'shipping':shipping}
        return JsonResponse(data)


@user_login_required
def payment(request):
    id = request.session.get('id')
    carts = OrderItem.objects.filter(customer_id=id)
    user = Registration.objects.get(id=id)

    total1 = 0
    for i in carts:
        total1 += int(i.total)

    total=(total1+50)*100

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
    address = Cus_address.objects.latest('updated_date')
    pinid=address.id
    pincode=Cus_address.objects.filter(id=pinid).values('pincode').get()['pincode']
    cart=OrderItem.objects.filter(customer_id=cus_id)
    boy=Address.objects.filter(user_id__role="Delivary_boy",pin=pincode)
    print(boy)
    print(address.id)
    for i in cart:
        complete="True"
        mycart= OrderItem.objects.filter(id=i.id)
        total = OrderItem.objects.filter(customer_id=cus_id,id=i.id).values('total').get()['total']
        totalcost = OrderItem.objects.filter(customer_id=cus_id,id=i.id).values('totalproductcost').get()['totalproductcost']
        quantity = OrderItem.objects.filter(customer_id=cus_id,id=i.id).values('quantity').get()['quantity']
        product = OrderItem.objects.filter(customer_id=cus_id,id=i.id).values('product').get()['product']
        productid = MyProduct.objects.get(id=product)
        productname = MyProduct.objects.filter(id=product).values('Product_name').get()['Product_name']
        farmerid=MyProduct.objects.filter(id=product).values('farmer_id').get()['farmer_id']
        farmeremail=Registration.objects.filter(id=farmerid).values('email').get()['email']
        customeremail = Registration.objects.filter(id=cus_id).values('email').get()['email']
        a=Order(myorder=address,cart=i,customer_id=cus_id,product=productid,quantity=quantity,totalproductcost=totalcost,total=total,complete=complete)
        print(cus_id,complete)
        a.save()
        text_content = "Your " + str(quantity) + "kg " + str(productname) + " was placed with a total cost of " + str(
            total)
        msg = EmailMultiAlternatives('Thank You For Purchasing the Product from Agrikart', text_content,
                                     EMAIL_HOST_USER, [customeremail])
        msg.send()
        text_content = "Your " + str(quantity) + "kg " + str(productname) + " was purchased with a total cost of " + str(total)
        msg = EmailMultiAlternatives('Your Product has purchased!!!!!!!!', text_content,
                                     EMAIL_HOST_USER, [farmeremail])
        msg.send()

    user=Registration.objects.get(id=cus_id)
    return render(request, 'customer/thanks.html',{'user':user})
@method_decorator(user_login_required, name='dispatch')
class Updatecustomer(View):
    def post(self, request):
        print('podaa')
        pimage = request.FILES.get("pimage")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        email = request.POST.get("email")
        phone_no = ','.join(request.POST.getlist("phone"))
        print(first_name, last_name, email, phone_no, pimage)
        id = request.session.get('id')
        if Address.objects.filter(user_id=id).exists():
            if pimage == None:
                user = Registration.objects.get(id=id)
                address = Address.objects.get(user_id=id)
                user.first_name = first_name
                user.last_name = last_name
                user.phone_no = phone_no
                user.email = email
                user.image = user.image
                user.save()
                print(user.image)
                context = {'user': user,'address':address}
                return render(request,'customer/customerprofile.html',context)
            else:
                user = Registration.objects.get(id=id)
                address = Address.objects.get(user_id=id)
                user.first_name = first_name
                user.last_name = last_name
                user.phone_no = phone_no
                user.email = email
                user.image = pimage
                user.save()
                print(user.image)
                context = {'user': user, 'address': address}
                return render(request, 'customer/customerprofile.html', context)
        else:
            if pimage == None:
                user = Registration.objects.get(id=id)
                address = Address.objects.get(user_id=id)
                user.first_name = first_name
                user.last_name = last_name
                user.phone_no = phone_no
                user.email = email
                user.image = user.image
                user.save()
                print(user.image)
                context = {'user': user}
                return render(request, 'customer/customerprofile.html', context)
            else:
                user = Registration.objects.get(id=id)
                address = Address.objects.get(user_id=id)
                user.first_name = first_name
                user.last_name = last_name
                user.phone_no = phone_no
                user.email = email
                user.image = pimage
                user.save()
                print(user.image)
                context = {'user': user}
                return render(request, 'customer/customerprofile.html', context)

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

@method_decorator(user_login_required, name='dispatch')
class OrderPlaced(View):
    def get(self, request):
        id=request.session.get('id')
        delivarydetails=DelivaryAssign.objects.filter(cart_id__customer_id=id)
        user=Registration.objects.get(id=id)
        myorder=Order.objects.filter(customer_id=id)
        return render(request, 'customer/Orderplaced.html',{'myorder':myorder,'user':user,'delivarydetails':delivarydetails})



class Trackmyemployee(View):
    def get(self, request):
        # Replace YOUR_ACCESS_TOKEN with your Mapbox access token
        mapbox_access_token = 'pk.eyJ1IjoidmlzaG51c2FkYXNpdmFuIiwiYSI6ImNsZzBkNzNxdDB0eGQzb21zOXliMGF2YzYifQ.7RmUJTHmLKMKR-ArFHqn2A'

        address = request.session.get('email')
        url = 'https://nominatim.openstreetmap.org/search'
        params = {'q': address, 'format': 'json'}

        response = requests.get(url, params=params)
        response.raise_for_status()

        # Get the latitude and longitude coordinates from the first result
        data = response.json()
        if len(data) == 0:
            raise ValueError(f'No results found for address "{address}"')
        latitude = float(data[0]['lat'])
        longitude = float(data[0]['lon'])

        delivery_boy_latitude = latitude
        delivery_boy_longitude = longitude

        # Pass the location data and Mapbox access token to the HTML template
        context = {
            'delivery_boy_latitude': delivery_boy_latitude,
            'delivery_boy_longitude': delivery_boy_longitude,
             }
        return render(request, 'customer/delivery_boy_location.html', context)

def farmerthanks(request, id):
    if request.method == 'GET':
        log=request.session.get('id')
        user=id
        payment1 = DelivaryAssign.objects.filter(cart_id__product_id__farmer_id=user,cart_id__product_id__farmer_id__role="Farmer", status='delivered',payforfarmer='pending')
        # payment = list(DelivaryAssign.objects.filter(cart_id__product_id__farmer_id=id,cart_id__product_id__farmer_id__role="Farmer", status='delivered',payforfarmer='pending').all())
        total = 0
        for i in payment1:
            total = total + i.cart.total
        total = int(total * 100)
        for j in payment1:
            j.payforfarmer = "payed"
            j.save()
        farmeremail = Registration.objects.filter(id=user).values('email').get()['email']
        text_content = "Your have payed a total of " + str(total) + "from Agrikart"
        msg = EmailMultiAlternatives('Thank You For Being the part of Agrikart', text_content,
                                     EMAIL_HOST_USER, [farmeremail])
        msg.send()

        return render(request, 'admin/paythanks.html')