from django.urls import path
from . import views
from home.views import CustomerRegistration,Submit,LoginPage,MyProduct,Logout,Orderaddress,Changepassword,Catagorydisplay
from customer.views import Updatecustomer,Addaddress
# from Agrikart.home import views
urlpatterns = [
   path('',views.index,name='index'),
   path('Login/',views.Login,name='Login'),
   path('customer_reg/<str:role>',CustomerRegistration.as_view(),name='customer_reg'),
   path('customer_reg/submit/<str:role>',Submit.as_view(),name='submit'),
   # path('farmer_reg',views.farmer_reg,name='farmer_reg'),
   # path('deliveryboy_reg',views.deliveryboy_reg,name='deliveryboy_reg'),
   path('signup',views.signup,name='signup'),
   path('adminhome/',views.adminhome,name='adminhome'),
   path('farmerhome/',views.farmerhome,name='farmerhome'),
   path('delivaryhome/',views.delivaryhome,name='delivaryhome'),
   path('Login/loginpage/',LoginPage.as_view(),name="loginpage"),
   path('Orderaddress',Orderaddress.as_view(), name='Orderaddress'),
   path('Changepassword', Changepassword.as_view(), name='Changepassword'),
   path('store/', views.store, name="store"),
   path('searchbar/', views.searchbar, name='searchbar'),
   path('searchbar1/', views.searchbar1, name='searchbar1'),
   path('searchbar_id', views.searchbar_id, name='searchbar_id'),
   path('Logout',Logout.as_view(),name='Logout'),
   # path('kkk',MyProduct.as_view(),name='text'),
   path('update_item/', views.updateItem, name="update_item"),
   # path('Change_Password/', views.change_password, name='change_password'),
   # path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
   # path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
   # path('resetPassword/', views.resetPassword, name='resetPassword'),
   path('Updatecustomer',Updatecustomer.as_view(),name='Updatecustomer'),
   path('Catagorydisplay', Catagorydisplay.as_view(), name='Catagorydisplay'),
   path('Addaddress',Addaddress.as_view(),name='Addaddress'),
]

