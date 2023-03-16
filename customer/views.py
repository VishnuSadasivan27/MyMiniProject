from django.http.response import HttpResponse
from django.views import View
import stripe
from django.conf import settings
from django.core.files.storage import default_storage
from django.urls import reverse
from django.shortcuts import redirect, render
from home.models import MyProduct
from customer.models import OrderItem,Cus_address

from django.shortcuts import redirect, render
from home.views import Registration
from customer.models import Order
stripe.api_key = settings.STRIPE_PRIVATE_KEY
def plusqty(request,id):
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

#minus
def minusqty(request,id):
    carts=OrderItem.objects.filter(id=id)
    print("hello",carts)
    for cart in carts:

        if int(cart.quantity) > 1:
            cart.quantity =cart.quantity-1;
            cart.total = int(cart.quantity) * int(cart.product.price)

            cart.save()
            return redirect('ViewCart')
        # messages.success(request, 'Out of Stock')
        return redirect('ViewCart')

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
        return render(request,'customer/checkout.html',{'total':total})
class Cart(View):
    def get(self, request):
        return render(request, 'customer/cart.html')

class Customerprofile(View):
    def get(self,request):
        l_id=request.session.get('id')
        print(l_id)
        return render(request,'customer/customerprofile.html')

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
class ViewCart(View):
    def get(self, request):
            # cart = MyProduct.objects.filter(id=id)
            customer = request.session.get('id')
            cartitem=OrderItem.objects.filter(customer_id=customer)

            print(cartitem)
            print(customer)
            context = {'items': cartitem}
            return render(request, 'customer/cart.html',context)

class RemoveCart(View):
    def get(self, request,id):
        cart_id= OrderItem.objects.get(id=id)
        cart_id.delete()
        return redirect('ViewCart')



def payment(request):

    id = request.session.get('id')
    carts = OrderItem.objects.filter(customer_id=id)

    total = 0
    for i in carts:
        print(i)
        total += int(i.total)
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price':'price_1MgYfzSIFeJdW3Ax15HlhI8O',
            'quantity': 1,

          
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('thanks'))+'?session_id = {CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('ViewCart')),
    )
    context = {
        'session_id': session.id,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'customer/payment.html', context)
def thanks(request):
    cus_id = request.session.get('id')
    cartitem = Cus_address.objects.filter(customer_id=cus_id)
    complete="True"
    a=Order(customer_id=cus_id,complete=complete)
    print(cus_id,complete)
    a.save()
    return render(request, 'customer/thanks.html')

class Updatecustomer(View):
    def post(self,request):
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone")
        user_image = request.FILES.get("p_image_select")
        print(first_name, last_name, email, phone_no,user_image)
        id=request.session.get('id')
        user = Registration.objects.filter(id=id)
        user.update(first_name=first_name, last_name=last_name, phone_no=phone_no, email=email,user_image=user_image )

        if user_image:
            # Save the file to a folder
            filename = default_storage.save('static/images' + ouser_image.name, user_image)
            user_image_url = default_storage.url(filename)
            print("785775869699690000000000000000000",user_image_url)
            context={'user_image':user_image_url}
        else:
            context={'user_image':None}

        return render(request,'customer/customerprofile.html',context)
