from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from home.models import MyProduct
from customer.models import OrderItem
from home.decorators import user_login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from home.views import Registration
from customer.models import Order,Cus_address
from home.models import Address
# Create your views here.
class Deliboyprofile(View):
    def get(self,request):
        l_id=request.session.get('id')
        print(l_id)
        if Address.objects.filter(user_id=l_id).exists():
            user=Registration.objects.get(id=l_id)
            address=Address.objects.get(user_id=l_id)

            return render(request,'delivaryboy/deliboyprofile.html',{'user':user,'address':address})
        else:
            user = Registration.objects.get(id=l_id)

            return render(request, 'delivaryboy/deliboyprofile.html', {'user': user })

class Viewmyjob(View):
    def get(self,request):
        id = request.session.get('id')
        pincode=Address.objects.filter(user_id=id).values('pin').get()['pin']
        print(pincode)
        if Address.objects.filter(user_id=id,user_id__status="active").exists():
            myorders=Order.objects.all()
            for order in myorders:
                print(order.myorder.pincode)
                if order.myorder.pincode == str(pincode):
                    orders=Order.objects.filter(myorder_id__pincode=pincode)
                    return render(request, 'delivaryboy/myjob.html',{'orders':orders})
                else:
                    return render(request, 'delivaryboy/myjob.html')
        elif  Address.objects.filter(user_id=id, user_id__status="inactive").exists():
            return HttpResponse("<script>alert('please wait for admin approval');window.location='/delivaryhome/';</script>")
        else:
            return HttpResponse("<script>alert('Add your Address in Your profile');window.location='/delivaryhome/';</script>")




@method_decorator(user_login_required, name='dispatch')
class Updatedelivaryboy(View):
    def post(self, request):
        pimage = request.FILES.get("pimage")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        email = request.POST.get("email")
        phone_no = ','.join(request.POST.getlist("phone"))
        print(first_name, last_name, email, phone_no, pimage)
        id = request.session.get('id')
        user = Registration.objects.get(id=id)
        user.first_name = first_name
        user.last_name = last_name
        user.phone_no = phone_no
        user.email = email
        user.image = pimage
        user.save()
        print(user.image)
        context = {'user': user}
        return redirect('Deliboyprofile')


@method_decorator(user_login_required, name='dispatch')
class DeliboyChangepassword(View):
    def post(self, request):
        id = request.session.get('id')
        user = Registration.objects.filter(id=id)
        old_pass = request.POST.get("cpassword")
        new_pass1 = request.POST.get("newpassword")
        new_pass2 = request.POST.get("renewpassword")
        print(old_pass, new_pass1, new_pass2);
        current_password = Registration.objects.filter(id=id).values('password').get()['password']
        if (old_pass == current_password):
            user.update(password=new_pass1)
            return HttpResponse(
                "<script>alert('Succesfully updated');window.location='Deliboyprofile';</script>")
        else:
            return HttpResponse(
                "<script>alert('current password is wrong');window.location='Deliboyprofile';</script>")



@method_decorator(user_login_required, name='dispatch')
class AddBoyaddress(View):
    def post(self, request):
        id = request.session['id']
        if Registration.objects.filter(id=id,status="inactive"):
            if not Address.objects.filter(user_id=id).exists():

                address = request.POST.get("Address")
                District = request.POST.get("District")
                panchayat = request.POST.get("panchayat")
                city = request.POST.get("city")
                landmark = request.POST.get("landmark")
                Aadhar = request.FILES.get("Aadhar")

                r=Address(address=address,district=District,panchayat=panchayat,city=city,Aadhar=Aadhar,landmark=landmark,user_id=id)
                r.save()
                address = Address.objects.get(user_id=id)
                user = Registration.objects.get(id=id)
                context={'address':address,'user':user}
                return HttpResponse("<script>alert('profile updated.wait for adminApproval');window.location='Deliboyprofile';</script>")

                return render(request, '', context)
            else:
                address = request.POST.get("Address")
                District = request.POST.get("District")
                panchayat = request.POST.get("panchayat")
                city = request.POST.get("city")
                landmark = request.POST.get("landmark")
                Aadhar = request.FILES.get("Aadhar")
                user = Address.objects.get(user_id=id)
                user.address = address
                user.district = District
                user.panchayat = panchayat
                user.city = city
                user.landmark = landmark
                user.Aadhar = Aadhar
                user.save()
                address = Address.objects.get(user_id=id)
                user = Registration.objects.get(id=id)
                context = {'address': address, 'user': user}
                return HttpResponse("<script>alert('Succesfully updated..wait for Approval');window.location='Deliboyprofile';</script>")
                return render(request, '', context)
        else:
            address = request.POST.get("Address")
            District = request.POST.get("District")
            panchayat = request.POST.get("panchayat")
            city = request.POST.get("city")
            landmark = request.POST.get("landmark")
            Aadhar = request.FILES.get("Aadhar")
            user = Address.objects.get(user_id=id)
            user.address = address
            user.district = District
            user.panchayat = panchayat
            user.city = city
            user.landmark = landmark
            user.Aadhar = Aadhar
            user.save()
            address = Address.objects.get(user_id=id)
            user = Registration.objects.get(id=id)
            context={'address':address,'user':user}
            return HttpResponse("<script>alert('Succesfully updated');window.location='Deliboyprofile';</script>")



