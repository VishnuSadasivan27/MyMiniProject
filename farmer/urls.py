from django.urls import path
from . import views
from farmer.views import Addproduct,ProductAdd,Farmerprofile
# from Agrikart.home import views
urlpatterns = [
   path('Addproduct',Addproduct.as_view(),name='Addproduct'),
   path('ProductAdd', ProductAdd.as_view(), name='ProductAdd'),
   path('Farmerprofile', Farmerprofile.as_view(), name='Farmerprofile'),
]