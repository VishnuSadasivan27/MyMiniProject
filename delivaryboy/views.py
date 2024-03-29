from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View
import random
from django.shortcuts import redirect, render
from home.models import MyProduct
from customer.models import OrderItem
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from Agrikart.settings import EMAIL_HOST_USER
from home.decorators import user_login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from home.views import Registration
from customer.models import Order,Cus_address
from delivaryboy.models import DelivaryAssign,DelivaryBoyLeave
from home.models import Address,MyProduct
# Create your views here.


class Leaveapplyform(View):
    def get(self,request):
        id=request.session.get('id')
        user = Registration.objects.get(id=id)
        return render(request, 'delivaryboy/leave.html', {'user': user})


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
        user=Registration.objects.get(id=id)
        if Address.objects.filter(user_id=id,user_id__status="active").exists():
            myorders=Order.objects.all()
            pincode = Address.objects.filter(user_id=id).values('pin').get()['pin']
            print(pincode)
            for order in myorders:
                print(order.myorder.pincode)
                if order.complete :
                    if order.myorder.pincode == str(pincode):
                        orders=Order.objects.filter(myorder_id__pincode=pincode,complete=True)
                        return render(request, 'delivaryboy/myjob.html',{'orders':orders,'user':user })
                    else:
                        return render(request, 'delivaryboy/myjob.html')
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
@method_decorator(user_login_required, name='dispatch')
class Delivaryjobaccept(View):
    def get(self,request,id):
        deliboy = request.session.get('id')
        deliid=Registration.objects.get(id=deliboy)
        orderplaced=Order.objects.get(id=id)
        customer=Order.objects.filter(id=id).values('customer').get()['customer']
        mail=Registration.objects.filter(id=customer).values('email').get()['email']
        print(mail)
        ## Generate Code and save it in a session
        request.session['code'] = random.randint(111111, 999999)
        ## Send email Functionality
        text_content = "The product code is " + str(
            request.session['code'])
        msg = EmailMultiAlternatives('This is the code for product Purchased in Agrikart', text_content, EMAIL_HOST_USER, [mail])
        msg.send()
        print(orderplaced.cart.product.farmer.id)
        farmeraddress=Address.objects.get(user_id=orderplaced.cart.product.farmer.id)
        r=DelivaryAssign(boy=deliid,farmer=farmeraddress,cart=orderplaced,delivarycode=request.session['code'])
        r.save()
        orderplaced.complete= False
        orderplaced.save()
        print(orderplaced.complete)
        return HttpResponse("<script>alert('Succesfully updated');window.location='/delivaryboy/Viewmyjob';</script>")

@method_decorator(user_login_required, name='dispatch')
class AcceptedJob(View):
    def get(self,request):
        id = request.session.get('id')
        user=Registration.objects.get(id=id)
        if Address.objects.filter(user_id=id,user_id__status="active").exists():
            delivary=DelivaryAssign.objects.filter(boy_id=id,status="pending")
            print(delivary)
            return render(request, 'delivaryboy/Accepted Job.html', {'delivary': delivary,'user':user})
        elif Address.objects.filter(user_id=id, user_id__status="inactive").exists():
            return HttpResponse(
                "<script>alert('please wait for admin approval');window.location='/delivaryhome/';</script>")
        else:
            return HttpResponse(
                "<script>alert('Add your Address in Your profile');window.location='/delivaryhome/';</script>")
@method_decorator(user_login_required, name='dispatch')
class ApplyLeave(View):
    def post(self,request):
        id = request.session.get('id')
        pin= Address.objects.filter(user_id=id).values('pin').get()['pin']
        user=Registration.objects.get(id=id)
        reason=request.POST.get('reason')
        date = request.POST.get('date')
        print(pin,reason,date)
        deli=DelivaryBoyLeave.objects.filter(id=1).values('required_date').get()['required_date']
        print(deli)
        if not DelivaryBoyLeave.objects.filter(boy_id=id,required_date=date, pincode=pin).exists():
            if not DelivaryBoyLeave.objects.filter(required_date=date,pincode=pin).exists():
                leave = DelivaryBoyLeave(boy_id=id,reason=reason,required_date=date,pincode=pin)
                leave.save()
                return HttpResponse("<script>alert('Your leave has succesfully applied');window.location='/delivaryhome/';</script>")

            else:
                return HttpResponse("<script>alert('Your companion has already applied on that date');window.location='/delivaryboy/Leaveapplyform';</script>")
        else:
            return HttpResponse("<script>alert('You have already applied leave on this date');window.location='/delivaryboy/Leaveapplyform';</script>")

class Leaveview(View):
    def get(self,request):
        id=request.session.get('id')
        user = Registration.objects.get(id=id)
        if Address.objects.filter(user_id=id, user_id__status="active").exists():
            leaves=DelivaryBoyLeave.objects.filter(boy_id=id)
            return render(request, 'delivaryboy/myleaves.html', {'user': user,'leaves':leaves})

        elif Address.objects.filter(user_id=id, user_id__status="inactive").exists():
            return HttpResponse("<script>alert('please wait for admin approval');window.location='/delivaryhome/';</script>")

        else:
            return HttpResponse("<script>alert('Add your Address in Your profile');window.location='/delivaryhome/';</script>")


@method_decorator(user_login_required, name='dispatch')
class Deletemyleave(View):
    def post(self, request):
        id = request.POST.get('ids')
        print("remove item id",id)
        if DelivaryBoyLeave.objects.filter(id=id,state="pending").exists():
            print("haiiiiiiiiiii123")
            cata_id=DelivaryBoyLeave.objects.filter(id=id, state="pending")
            cata_id.delete()
            data={'data':"succees"}
        elif DelivaryBoyLeave.objects.filter(id=id, state="Approved").exists():
            print("haiiiiiiiiiii")
            cata_id = DelivaryBoyLeave.objects.get(id=id, state="Approved")
            print(cata_id)
            cata_id.state="Cancelled"
            cata_id.save()
            data = {'data': "succees"}
        return JsonResponse(data)
class Orderplaced(View):
    def post(self,request):
        id=request.POST.get('ids')
        otp = request.POST.get('otp')
        print(id,otp)
        delivary = DelivaryAssign.objects.get(id=id)
        realotp=DelivaryAssign.objects.filter(id=id).values('delivarycode').get()['delivarycode']
        print(realotp)
        if realotp==otp:
            delivary.status="delivered"
            delivary.save()
            data = {'data': "succees"}
            return JsonResponse(data)
        else:
            print('jggghghgggggggggggggggggggggg')
            data = {'data': "error"}
            return JsonResponse(data)


