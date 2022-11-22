from django.urls import path
from . import views
from home.views import CustomerRegistration,Submit,LoginPage,MyProduct,Logout
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
   path('Login/loginpage/',LoginPage.as_view(),name="loginpage"),
   path('store/', views.store, name="store"),
   path('searchbar/', views.searchbar, name='searchbar'),
   path('Logout',Logout.as_view(),name='Logout'),
   # path('kkk',MyProduct.as_view(),name='text'),
     path('update_item/', views.updateItem, name="update_item"),
   # path('Change_Password/', views.change_password, name='change_password'),
   # path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
   # path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
   # path('resetPassword/', views.resetPassword, name='resetPassword'),

]

