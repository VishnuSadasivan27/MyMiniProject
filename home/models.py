#
# from django.db import models
# from django.contrib.auth.models import User
# # Create your models here.
# # class Customer_reg(models.Model):
# #     name = models.CharField(max_length=200,null=True)
# #     email = models.EmailField(max_length=200,null=True)
# #     phonenumber=models.IntegerField(max_length=12,null=True)
# #     password = models.CharField(max_length=12,null=True)
# #     confirm_password = models.CharField(max_length=12, null=True)
# #     role = models.CharField(max_length=20,null=True)
#
#
# class user_login(models.Model):
#     username = models.CharField(max_length=200,null=True)
#     password = models.CharField(max_length=8,null=True)
# class Farmer_reg(models.Model):
#     name = models.CharField(max_length=200,null=True)
#     address = models.CharField
#     email = models.EmailField(max_length=200,null=True)
#     far_adar= models.IntegerField()
#     idproof = models.FileField()
#     district = models.CharField(max_length=200,null=True)
#     phone = models.IntegerField()
#     landmark = models.CharField(max_length=200,null=True)
#     city = models.CharField(max_length=200,null=True)
#     pin = models.IntegerField()
#     role = models.CharField(max_length=20,null=True)
# class Deliveryboy_reg(models.Model):
#     name = models.CharField(max_length=200,null=True)
#     email = models.EmailField(max_length=200,null=True)
#     phone = models.IntegerField()
#     location= models.CharField(max_length=200,null=True)
#     idproof = models.FileField()
from enum import unique
from django.db import models
import uuid
import datetime



class Registration(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_no = models.IntegerField( default=uuid.uuid1)
    role = models.CharField(max_length=200)
    status = models.CharField(max_length=200,default="inactive")
    password = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=100)
    image = models.ImageField(default='default.png',upload_to = 'userimage/')

    def int(self):
        return self.id

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Review(models.Model):
    date = models.DateField()
    Description = models.CharField(max_length=200)
    user = models.ForeignKey(Registration, on_delete=models.CASCADE, max_length=100, null=True)



class Address(models.Model):
    address = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    panchayat= models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    pin = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    idproof = models.ImageField(upload_to =  None)
    user = models.ForeignKey(Registration, on_delete=models.CASCADE, max_length=100, null=True)




    # class Meta:
    #     ordering = ['-first_name']
    #
    # def str(self):
    #     return self.first_name

# class Product(models.Model):
#     product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     Product_name = models.CharField(max_length = 200)
#     price = models.CharField(max_length=100)
#     quantity = models.CharField(max_length=100)
#     image = models.ImageField(upload_to=None)
#     adddate = models.DateField("adddate")
#     expirydate = models.DateField("expirydate")
#     review = models.ForeignKey(Review, on_delete=models.CASCADE, max_length=100, null=True)

class MyProduct(models.Model):
    Product_name = models.CharField(max_length = 200,null=True)
    price = models.CharField(max_length=100,null=True)
    quantity = models.CharField(max_length=100,null=True)
    image = models.ImageField(null=True, blank=True)
    adddate = models.DateField("adddate",null=True)
    expirydate = models.DateField("expirydate",null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, max_length=100, null=True)
    farmer = models.ForeignKey(Registration, on_delete=models.CASCADE, max_length=100, null=True)

    def __str__(self):
        return self.Product_name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url





# class UserLogin(models.Model):
#     user_id = models.ForeignKey(Registration, on_delete=models.CASCADE, max_length=200, null=True)
#     password = models.CharField(max_length=200)
#     email = models.EmailField(unique=True, max_length=100)
#     MyProduct = models.ForeignKey(MyProduct, on_delete=models.CASCADE, max_length=100, null=True)
#     address = models.ForeignKey(Address, on_delete=models.CASCADE, max_length=100, null=True)
#     review = models.ForeignKey(Review, on_delete=models.CASCADE, max_length=100, null=True)
#     # class Meta:
#     #     ordering = ['-first_name']
#
#     def str(self):
#         return self.email

class AdminLogin(models.Model):
    password = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=100)














