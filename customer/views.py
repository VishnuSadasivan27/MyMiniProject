from django.http.response import HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from home.models import MyProduct
from customer.models import OrderItem
from django.shortcuts import redirect, render
from home.views import Registration
from customer.models import Order

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

        return render(request,'customer/checkout.html')
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
            addcart.total=addcart.product.price
            addcart.totalproductcost=addcart.totalproductcost
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


