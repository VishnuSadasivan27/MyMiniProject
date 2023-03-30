from django.urls import path
from . import views
from delivaryboy.views import Deliboyprofile,Viewmyjob,Updatedelivaryboy,AddBoyaddress,DeliboyChangepassword

# from Agrikart.home import views
urlpatterns = [
   path('Deliboyprofile',Deliboyprofile.as_view(),name='Deliboyprofile'),
   path('Viewmyjob',Viewmyjob.as_view(),name='Viewmyjob'),
   path('Updatedelivaryboy', Updatedelivaryboy.as_view(), name='Updatedelivaryboy'),
   path('DeliboyChangepassword', DeliboyChangepassword.as_view(), name='DeliboyChangepassword'),
   path('AddBoyaddress', AddBoyaddress.as_view(), name='AddBoyaddress'),

]