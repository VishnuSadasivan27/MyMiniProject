from django.urls import path
from . import views
from customer.views import Customerprofile,AddCart,Checkout,Cart,ViewCart,RemoveCart,Updatecustomer

# from Agrikart.home import views
urlpatterns = [
   path('customerprofile',Customerprofile.as_view(),name='Customerprofile'),
   path('AddCart/<id>/',AddCart.as_view(), name='AddCart'),
   path('/ViewCart',ViewCart.as_view(), name='ViewCart'),
   # path('Orderaddress',Orderaddress.as_view(), name='Orderaddress'),
   path('RemoveCart/',RemoveCart.as_view(), name='RemoveCart'),
   path('plusqty/',views.plusqty,name='plusqty'),
   path('payment',views.payment,name='payment'),
   path('Updatecustomer',Updatecustomer.as_view(),name='Updatecustomer'),
   path('minusqty/',views.minusqty,name='minusqty'),
   path('cart',Cart.as_view(), name='Cart'),
   path('Checkout',Checkout.as_view() , name='Checkout'),
]