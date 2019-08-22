from django.shortcuts import render,redirect
from django.http import HttpResponse


from django.contrib.auth import login,logout,authenticate

from .models import HealthCentreStaff
# Create your views here.

def indexView(request):
    return render(request,'doctor/index.html')


def loginView(request):
    if request.method=='POST':
        user_name=request.POST['username-login']
        pwd=request.POST['pwd-login']
        user=authenticate(username=user_name,password=pwd)
        if user is not None:
            login(request,user)
            return redirect('doctor-home-view')
    user=request.user
    if not user.is_authenticated:
        return render(request,'doctor/login.html')
    return redirect('doctor-home-view')


def homeView(request):
    user=request.user
    if not user.is_authenticated:
        return redirect('login-view')
    return render(request,'doctor/home.html')

def log_out(req):
    logout(req)
    return redirect('login-view')


def displayHealthCenterStaff(req):
    user=req.user
    print(user)
    if user.is_authenticated:
        if user.has_perm("doctor.view_healthcentrestaff"):
            data=HealthCentreStaff.objects.all()
            l=[]
            for i in data:
                d={
                    'name':i.staff_name,
                    'type':i.staff_type,
                    'address':i.staff_address,
                    'availability':(i.availability_from+" to "+i.availability_to)
                }
                l.append(d)
            ctx={
                'data':l
            }
            return render(req,'doctor/stafftable.html',context=ctx)
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    return redirect('login-view')
    
