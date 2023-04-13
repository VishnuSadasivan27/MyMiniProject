from django.urls import path
from . import views
from farmer.views import Addproduct,ProductAdd,Editmyproduct,Editproduct,RemoveProduct,Viewaddedproduct,Addfarmeraddress,Farmerprofile,FarmerChangepassword,Updatefarmer
# from Agrikart.home import views
urlpatterns = [
   path('Addproduct',Addproduct.as_view(),name='Addproduct'),
   path('ProductAdd', ProductAdd.as_view(), name='ProductAdd'),
   path('Editproduct/<id>', Editproduct.as_view(), name='Editproduct'),
   path('Farmerprofile', Farmerprofile.as_view(), name='Farmerprofile'),
   path('Addfarmeraddress', Addfarmeraddress.as_view(), name='Addfarmeraddress'),
   path('Predictproduct', views.Predictproduct, name='Predictproduct'),
   path('Viewaddedproduct', Viewaddedproduct.as_view(),name='Viewaddedproduct'),
   path('RemoveProduct', RemoveProduct.as_view(), name='RemoveProduct'),
   path('FarmerChangepassword', FarmerChangepassword.as_view(), name='FarmerChangepassword'),
   path('Editmyproduct/<id>', Editmyproduct.as_view(), name='Editmyproduct'),

]