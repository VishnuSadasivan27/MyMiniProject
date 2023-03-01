from django.urls import path
from . import views
from delivaryboy.views import Deliboyprofile,Viewmyjob
# from Agrikart.home import views
urlpatterns = [
   path('Deliboyprofile',Deliboyprofile.as_view(),name='Deliboyprofile'),
   path('Viewmyjob',Viewmyjob.as_view(),name='Viewmyjob'),
]