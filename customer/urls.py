from django.urls import path
from . import views
from customer.views import Customerprofile,AddCart,Checkout,Cart,ViewCart,RemoveCart
# from Agrikart.home import views
urlpatterns = [
   path('customerprofile',Customerprofile.as_view(),name='Customerprofile'),
   path('AddCart/<id>/',AddCart.as_view(), name='AddCart'),
   path('ViewCart',ViewCart.as_view(), name='ViewCart'),
   path('RemoveCart/<id>/',RemoveCart.as_view(), name='RemoveCart'),
   path('cart',Cart.as_view(), name='Cart'),
   path('checkout',Checkout.as_view() , name='Checkout'),
]