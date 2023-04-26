from django.urls import path
from . import views
from delivaryboy.views import Deliboyprofile,Deletemyleave,Leaveview,Leaveapplyform,ApplyLeave,AcceptedJob,Delivaryjobaccept,Viewmyjob,Updatedelivaryboy,AddBoyaddress,DeliboyChangepassword

# from Agrikart.home import views
urlpatterns = [
   path('Deliboyprofile',Deliboyprofile.as_view(),name='Deliboyprofile'),
   path('Deletemyleave', Deletemyleave.as_view(), name='Deletemyleave'),
   path('Leaveapplyform',Leaveapplyform.as_view(),name='Leaveapplyform'),
   path('Leaveview',Leaveview.as_view(),name='Leaveview'),
   path('ApplyLeave', ApplyLeave.as_view(), name='ApplyLeave'),
   path('AcceptedJob', AcceptedJob.as_view(), name='AcceptedJob'),
   path('Delivaryjobaccept/<int:id>',Delivaryjobaccept.as_view(), name='Delivaryjobaccept'),
   path('Viewmyjob',Viewmyjob.as_view(),name='Viewmyjob'),
   path('Updatedelivaryboy', Updatedelivaryboy.as_view(), name='Updatedelivaryboy'),
   path('DeliboyChangepassword', DeliboyChangepassword.as_view(), name='DeliboyChangepassword'),
   path('AddBoyaddress', AddBoyaddress.as_view(), name='AddBoyaddress'),

]