from django.shortcuts import render,redirect
from django.http import HttpResponse


from django.contrib.auth import login,logout,authenticate

from .models import *
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

def displayEmpanelledFirms(req):
    user = req.user
    if user.is_authenticated:
        if user.has_perm("doctor.view_empanelledfirm"):
            data=EmpanelledFirm.objects.all()
            l = []
            for i in data:
                d={
                    'name' : i.firm_name,
                    'email' : i.firm_email,
                    'phone' : i.firm_phone
                  }
                l.append(d)
            ctx={
                'data':l
                }
            return render(req,'doctor/firmtable.html',context=ctx)
        else:
            return render(req,'doctor/error.html')

def displayMedicine(req):
    user = req.user
    if user.is_authenticated:
        if user.has_perm("doctor.view_medicine") and user.has_perm("doctor.view_stockmedicine"):
            data_stockmeds= StockMedicine.objects.select_related("medicine_id").order_by('medicine_id','expiry_date')
            l = []
            for i in data_stockmeds:
                d = {
                    'name': i.medicine_id.medicine_name,
                    'category': i.medicine_id.category,
                    'batch_no': i.batch_no,
                    'price': i.medicine_rate,
                    'quantity': i.quantity,
                    'expiry_date': i.expiry_date,
                    'manufacturing_company':i.medicine_id.manufacturing_company
                    }
                l.append(d)
            ctx = {
                    'data': l
                  }
            return render(req,'doctor/medicinestock.html',context=ctx)
        else:
            return render(req,'doctor/error.html')