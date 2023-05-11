from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
from home.models import MyProduct,MyAnalysisProduct
from sklearn.model_selection import train_test_split

from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View
from django.http import JsonResponse
from django.shortcuts import redirect, render
from home.models import Registration,Catagory,Address
import subprocess
from home.decorators import user_login_required
from django.utils.decorators import method_decorator
@user_login_required
def Predictproduct(request):
    id = request.session.get('id')
    if not Registration.objects.filter(id=id, status="active").exists():
       return HttpResponse("<script>alert('Add your Address to Activate your Account');window.location='/farmerhome/';</script>")
    else:
        subprocess.run(['python', 'farmer/Machine_learning_knn.py'])
        return redirect('/farmerhome')
@method_decorator(user_login_required, name='dispatch')
class Addproduct(View):
    def get(self,request):
        id = request.session.get('id')
        user=Registration.objects.get(id=id)
        if not Registration.objects.filter(id=id,status="active").exists():
            return HttpResponse(
                "<script>alert('Add your Address to Activate your Account');window.location='/farmerhome/';</script>")
        else:
            mycat=Catagory.objects.all()
            return render(request,'farmer/product_add.html',{'mycat':mycat,'user':user})

@method_decorator(user_login_required, name='dispatch')
class ProductAdd(View):
    def post(self, request):
        Product_name = request.POST.get("product_name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        image = request.FILES.get("primage")
        expirydate = request.POST.get("expiry")
        catagory= request.POST.get("catagory")
        print(Product_name, price, quantity, image, catagory, expirydate)
        data=Catagory.objects.filter(catagory_name=catagory).values('id').get()['id']
        cataid=Catagory.objects.get(id=data)
        print(cataid)
        id=request.session.get('id')
        user = Registration.objects.get(id=id)
        r = MyProduct(Product_name=Product_name , price=price, quantity=quantity,Addedquantity=quantity, image=image,expirydate=expirydate,catagory=cataid,farmer=user)
        r.save()
        return HttpResponse("<script>alert('Product Added');window.location='/farmer/Addproduct';</script>")
        return render(request, 'farmer/product_add.html')

@method_decorator(user_login_required, name='dispatch')
class Updatefarmer(View):
    def post(self, request):
        pimage = request.FILES.get("pimage")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        email = request.POST.get("email")
        phone_no = ','.join(request.POST.getlist("phone"))
        print(first_name, last_name, email, phone_no, pimage)
        id = request.session.get('id')
        if pimage==None:
            user = Registration.objects.get(id=id)
            user.first_name = first_name
            user.last_name = last_name
            user.phone_no = phone_no
            user.email = email
            user.image = user.image
            user.save()
            print(user.email)
            print(user.image)
            context = {'user': user}
            return render(request,'farmer/farmerprofile.html',context)
        else:
            user = Registration.objects.get(id=id)
            user.first_name = first_name
            user.last_name = last_name
            user.phone_no = phone_no
            user.email = email
            user.image = pimage
            user.save()
            print(user.email)
            print(user.image)
            context = {'user': user}
            return render(request,'farmer/farmerprofile.html',context)




@method_decorator(user_login_required, name='dispatch')
class Farmerprofile(View):
    def get(self,request):
        id = request.session.get('id')
        user = Registration.objects.get(id=id)
        if Address.objects.filter(user_id=id).exists():
            address = Address.objects.get(user_id=id)
            print(user)
            context = {'user': user, 'address': address}
            return render(request,'farmer/farmerprofile.html', context)
        else:
            context = {'user': user}
            return render(request,'farmer/farmerprofile.html', context)

@method_decorator(user_login_required, name='dispatch')
class FarmerChangepassword(View):
    def post(self, request):
        id = request.session.get('id')
        user = Registration.objects.filter(id=id)
        old_pass = request.POST.get("cpassword")
        new_pass1 = request.POST.get("newpassword")
        new_pass2= request.POST.get("renewpassword")
        print(old_pass,new_pass1,new_pass2);
        current_password = Registration.objects.filter(id=id).values('password').get()['password']
        if(old_pass==current_password):
             user.update(password=new_pass1)
             return HttpResponse("<script>alert('Succesfully updated');window.location='Farmerprofile';</script>")
        else:
            return HttpResponse("<script>alert('current password is wrong');window.location='Farmerprofile';</script>")


@method_decorator(user_login_required, name='dispatch')
class Addfarmeraddress(View):
    def post(self, request):
        id = request.session['id']
        if Registration.objects.filter(id=id,status="inactive"):
            if not Address.objects.filter(user_id=id).exists():

                address = request.POST.get("Address")
                District = request.POST.get("District")
                panchayat = request.POST.get("panchayat")
                city = request.POST.get("city")
                landmark = request.POST.get("landmark")
                pincode = request.POST.get("pincode")
                Aadhar = request.FILES.get("Aadhar")

                r=Address(address=address,district=District,panchayat=panchayat,city=city,Aadhar=Aadhar,landmark=landmark,pin=pincode,user_id=id)
                r.save()
                address = Address.objects.get(user_id=id)
                user = Registration.objects.get(id=id)
                context={'address':address,'user':user}
                return HttpResponse("<script>alert('profile updated.wait for adminApproval');window.location='Farmerprofile';</script>")

                return render(request, 'farmer/farmerprofile.html', context)
            else:
                address = request.POST.get("Address")
                District = request.POST.get("District")
                panchayat = request.POST.get("panchayat")
                city = request.POST.get("city")
                landmark = request.POST.get("landmark")
                pincode = request.POST.get("pincode")
                Aadhar = request.FILES.get("Aadhar")
                user = Address.objects.get(user_id=id)
                user.address = address
                user.district = District
                user.panchayat = panchayat
                user.city = city
                user.landmark = landmark
                user.pin = pincode
                user.Aadhar = Aadhar
                user.save()
                address = Address.objects.get(user_id=id)
                user = Registration.objects.get(id=id)
                context = {'address': address, 'user': user}
                return HttpResponse("<script>alert('Succesfully updated..wait for Approval');window.location='Farmerprofile';</script>")
                return render(request, 'farmer/farmerprofile.html', context)
        else:
            address = request.POST.get("Address")
            District = request.POST.get("District")
            panchayat = request.POST.get("panchayat")
            city = request.POST.get("city")
            landmark = request.POST.get("landmark")
            pincode = request.POST.get("pincode")
            Aadhar = request.FILES.get("Aadhar")
            user = Address.objects.get(user_id=id)
            user.address = address
            user.district = District
            user.panchayat = panchayat
            user.city = city
            user.landmark = landmark
            user.pin=pincode
            user.Aadhar = Aadhar
            user.save()
            address = Address.objects.get(user_id=id)
            user = Registration.objects.get(id=id)
            context={'address':address,'user':user}
            return HttpResponse("<script>alert('Succesfully updated');window.location='Farmerprofile';</script>")
            return render(request, 'farmer/farmerprofile.html', context)

@method_decorator(user_login_required, name='dispatch')
class Viewaddedproduct(View):
    def get(self,request):
        id = request.session.get('id')
        user=Registration.objects.get(id=id)
        myproduct=MyProduct.objects.filter(farmer_id=user)
        context= {'myproduct':myproduct,'user':user}
        return render(request, 'farmer/Productview.html', context)
@method_decorator(user_login_required, name='dispatch')
class RemoveProduct(View):
    def post(self, request):
        id = request.POST.get('ids')
        print("remove item id",id)
        product= MyProduct.objects.filter(id=id)

        product.delete()
        data={'data':"succees"}
        return JsonResponse(data)
@method_decorator(user_login_required, name='dispatch')
class Editproduct(View):
    def get(self,request,id):
        myid=request.session.get('id')
        user=Registration.objects.get(id=myid)
        product=MyProduct.objects.get(id=id)
        print(product.image)
        formatted_date = datetime.strftime(product.expirydate, '%Y-%m-%d')
        mycat = Catagory.objects.all()
        if not product.catagory:  # if product has no category, set default to the first category
            product.catagory = mycat.first()
        else:  # if product has a category, set default to the current category
            for cat in mycat:
                if cat.catagory_name == product.catagory.catagory_name:
                    product.catagory = cat
                    break
        context={'user':user,'product':product,'mycat':mycat,'formatted_date':formatted_date}
        return render(request,"farmer/productedit.html",context)

@method_decorator(user_login_required, name='dispatch')
class Editmyproduct(View):
    def post(self,request,id):
        print(id)
        Product_name = request.POST.get("product_name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        image = request.FILES.get("primage")
        expirydate = request.POST.get("expiry")
        cata = request.POST.get("catagory")
        catas=Catagory.objects.filter(catagory_name=cata).values('id').get()['id']
        catagory = Catagory.objects.get(id=catas)
        print(Product_name, price, quantity, image, catagory, expirydate)
        editproduct=MyProduct.objects.get(id=id)
        print(editproduct.image)
        editproduct.Product_name=Product_name
        editproduct.price = price
        editproduct.quantity = quantity
        editproduct.Addedquantity=quantity
        editproduct.expirydate = expirydate
        editproduct.catagory=catagory
        if image==None:
            editproduct.image = editproduct.image
        else:
            editproduct.image=image
        editproduct.save()

        return HttpResponse("<script>alert('Product Added');window.location='/farmer/Viewaddedproduct';</script>")

@method_decorator(user_login_required, name='dispatch')
class Predictproductcost(View):
        def get(self, request):

            return render(request, 'farmer/Predictcostpage.html')


# @method_decorator(user_login_required, name='dispatch')
# class PredictingCost(View):
#     def post(self, request):
#         Product_name = request.POST.get("proname")
#         expected_cost = float(request.POST.get("cost"))
#
#         # Filter the queryset to only include the same type of crop
#         queryset = MyAnalysisProduct.objects.filter(Product_name=Product_name)
#         print(queryset.count())
#
#         # Convert the queryset to a pandas dataframe
#         data = pd.DataFrame(list(queryset.values()))
#
#         # Encode categorical variables
#         data = pd.get_dummies(data, columns=['Product_name'],)
#         print("haii")
#         # Split the data into training and test sets
#
#
#         # Split the data into training and test sets
#         X_train, X_test, y_train, y_test = train_test_split(data.drop('price', axis=1), data['price'], test_size=0.2,
#                                                             random_state=42)
#         print("hello")
#         # Train a linear regression model on the training data
#         model = LinearRegression()
#         model.fit(X_train, y_train)
#         print(model)
#
#         # Evaluate the model on the test data
#         score = model.score(X_test, y_test)
#         print(score)
#
#         # Use the model to make a prediction for the expected cost
#         input_data = pd.DataFrame({'Product_name' + Product_name: [1], 'soldprice': [1]})
#         predicted_cost = model.predict([[expected_cost]])[0]
#
#         # Return the predicted cost
#         print(predicted_cost)
#
#         return render(request, 'farmer/Predictcostpage.html')


class PredictingCost(View):
    def post(self, request):
        Product_name = request.POST.get("proname")
        expected_cost = float(request.POST.get("cost"))
        print(Product_name,expected_cost)
        # Filter the queryset to only include the same type of crop
        if MyAnalysisProduct.objects.filter(Product_name=Product_name).exists():
            queryset = MyAnalysisProduct.objects.filter(Product_name=Product_name)
            print(queryset.count())
            if queryset.count()>12 :

                # Convert the queryset to a pandas dataframe
                data = pd.DataFrame(list(queryset.values()))

                # Encode categorical variables
                data = pd.get_dummies(data, columns=['Product_name'])

                # Split the data into training and test sets
                X_train, X_test, y_train, y_test = train_test_split(data.drop('price', axis=1), data['price'], test_size=0.8,
                                                                    random_state=42)

                # Train a linear regression model on the training data
                model = LinearRegression()
                model.fit(X_train, y_train)

                # Evaluate the model on the test data
                score = model.score(X_test, y_test)


                # Use the model to make a prediction for the expected cost
                input_data = pd.DataFrame({'Product_name_' + Product_name: [1], 'soldprice': [1],'quantity': [1], 'id': [1]})
                input_data['soldprice'] = expected_cost
                input_data = input_data[X_train.columns]  # Ensure column order is the same as in training data
                predicted_cost = model.predict(input_data)[0]
                print(predicted_cost)
                data = {'predicted_cost': predicted_cost}
                return JsonResponse(data)
                 # Return the predicted cost
            else:
                return HttpResponse("<script>alert('Not sufficient data to predict');window.location='/farmer/Predictcostpage.html';</script>")

        else:
            return HttpResponse("<script>alert('Product with that name doesnot exist in the database');window.location='/farmer/Predictcostpage.html';</script>")
        # return render(request, 'farmer/Predictcostpage.html', {'predicted_cost': predicted_cost})

