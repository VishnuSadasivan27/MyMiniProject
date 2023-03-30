from django.urls import path
from . import views
from farmer.views import Addproduct,ProductAdd,Addfarmeraddress,Farmerprofile,FarmerChangepassword,Updatefarmer
# from Agrikart.home import views
urlpatterns = [
   path('Addproduct',Addproduct.as_view(),name='Addproduct'),
   path('ProductAdd', ProductAdd.as_view(), name='ProductAdd'),
   path('Farmerprofile', Farmerprofile.as_view(), name='Farmerprofile'),
   path('Addfarmeraddress', Addfarmeraddress.as_view(), name='Addfarmeraddress'),
   path('Updatefarmer', Updatefarmer.as_view(), name='Updatefarmer'),
   path('Predictproduct', views.Predictproduct, name='Predictproduct'),
   path('FarmerChangepassword', FarmerChangepassword.as_view(), name='FarmerChangepassword'),

]