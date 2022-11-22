from django.urls import path
from . import views
from Admins.views import Farmer_approve,Customerview,Farmerview,Activate,Deactivate,Deletedcustomer,Activatecustomer,Farmerdeactivate,Adminprofile
urlpatterns = [
   path('Farmer_approval',Farmer_approve.as_view(),name='Farmer_approval'),
   path('Customerview',Customerview.as_view(),name='Customerview'),
   path('Deletecustomer',Deletedcustomer.as_view(),name='Deletecustomer'),
   path('Farmerview',Farmerview.as_view(),name='Farmerview'),
   path('Activate/<int:id>/',Activate.as_view(),name='Activate'),
   path('Activatecustomer/<int:id>/',Activatecustomer.as_view(),name='Activatecustomer'),
   path('Deactivate/<int:id>/',Deactivate.as_view(),name='Deactivate'),
   path('Farmerdeactivate/<int:id>/',Farmerdeactivate.as_view(),name='Farmerdeactivate'),
   path('customersearchbar/', views.customersearchbar, name='customersearchbar'),
   path('farmersearchbar/', views.farmersearchbar, name='farmersearchbar'),
   path('farmerdsearchbar/', views.farmerdsearchbar, name='farmerdsearchbar'),
   path('customerdsearchbar/', views.customerdsearchbar, name='customerdsearchbar'),
   path('Adminprofile/', Adminprofile.as_view(), name='Adminprofile'),
   ]