from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.paginator import Paginator

from django.contrib.auth import login,logout,authenticate
from .models import *
from django.db import IntegrityError
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
    permcheck=checkForPermission(req,"doctor.view_healthcentrestaff")
    if permcheck==-1:
        return redirect('login-view')
    if permcheck==0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        data=HealthCentreStaff.objects.all()
        l=[]
        for i in data:
            d={
                'id':i.staff_id,
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

def addHealthCenterStaff(request):
    permcheck=checkForPermission(request,"doctor.add_healthcentrestaff")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        return render(request,'doctor/addStaff.html')

def editHealthCenterStaff(request, pk):
    permcheck = checkForPermission(request, "doctor.change_healthcentrestaff")
    if permcheck == 1:
        data = HealthCentreStaff.objects.get(staff_id=pk)
        ctx = {
            'data': {
                'id': data.staff_id,
                'name': data.staff_name,
                'type': data.staff_type,
                'address': data.staff_address,
                'availability_from': data.availability_from,
                'availability_to': data.availability_to,
            }
        }
    return render(request, 'doctor/addStaff.html', ctx)

def deleteHealthCenterStaff(request, pk):
    permcheck = checkForPermission(request, "doctor.delete_healthcentrestaff")
    if permcheck == 1:
        HealthCentreStaff.objects.filter(staff_id=pk).delete()
        return redirect('display-staff-view')
    else:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")


def insertIntoHealthCenterStaff(request):
    permcheck = checkForPermission(request, "doctor.add_healthcentrestaff")
    if permcheck == 1 and request.method == "POST":
        id = request.POST["staff-id"]
        name = request.POST["staff-name"]
        type = request.POST["staff-type"]
        address = request.POST["staff-address"]
        availability_from = request.POST["staff-availability_from"]
        availability_to = request.POST["staff-availability_to"]

        obj, created = HealthCentreStaff.objects.update_or_create(
            staff_id=id,

            defaults={
                'staff_name': name,
                'staff_type': type,
                'staff_address': address,
                'availability_from': availability_from,
                'availability_to': availability_to,
            }
        )

        return redirect('display-staff-view')
    return redirect(request, 'doctor/error.html')
    
def displayRequisitionMedicine(request):
    user=request.user
    permcheck=checkForPermission(request,"doctor.view_requisitionmedicine")
    if permcheck==-1:
        return redirect('login-view')
    if permcheck==0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        data=RequisitionMedicine.objects.all()
        l=[]
        for i in data:
            d={
                'req_id':i.requisition_id,
                'med_id':i.medicine_id,
                'qty_requested':i.quantity_requested,
                'qty_received':i.quantity_received
            }
            l.append(d)
        ctx={
            'data':l
        }
        return render(request,'doctor/requisitionMedicine.html',context=ctx)


def addRequisitionMedicine(request):
    permcheck=checkForPermission(request,"doctor.add_requisitionmedicine")
    if permcheck==-1:
        return redirect('login-view')
    if permcheck==0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        req_ids=Requisition.objects.all().values("requisition_id")
        rids=[]
        for i in req_ids:
            rids.append(i["requisition_id"])
        med_ids = Medicine.objects.all().values("medicine_id","medicine_name").order_by("medicine_name")
        meds=[]
        for i in med_ids:
            meds.append(i)
        ctx={
            'req_ids':rids,
            'meds':meds
        }
        return render(request,'doctor/addRequisitionMedicine.html',context=ctx)

def insertIntoRequisitionMedicine(request):
    permcheck=checkForPermission(request,"doctor.add_requisitionmedicine")
    if permcheck==1 and request.method=="POST":
        new_entry=RequisitionMedicine()
        r_id=int(request.POST["req-id"])
        requisition=Requisition.objects.filter(requisition_id=r_id)[0]
        m_id=int(request.POST["med-id"])
        print(requisition)
        medicine=Medicine.objects.filter(medicine_id=m_id)[0]
        q_req=request.POST["qty-requested"]
        q_rec=request.POST["qty-received"]
        new_entry.add_requisition_medicine(requisition,medicine,q_req,q_rec)
        return redirect('display-requisitionmedicine-view')
    return render(request,'doctor/error.html')

def checkForPermission(request,permission):
    user=request.user
    if user.is_authenticated:
        if user.has_perm(permission):
            return 1
        return 0
    return -1

def displayEmpanelledFirms(req):
    user = req.user
    if user.is_authenticated:
        if user.has_perm("doctor.view_empanelledfirm"):
            data_all=EmpanelledFirm.objects.all()
            paginator = Paginator(data_all, 10)
            page = req.GET.get('page')
            data = paginator.get_page(page)
            l = []
            for i in data:
                d={
                    'id' : i.firm_id,
                    'name' : i.firm_name,
                    'email' : i.firm_email,
                    'phone' : i.firm_phone
                  }
                l.append(d)
            ctx={
                'data':data
                }
            return render(req,'doctor/firmtable.html',context=ctx)
        else:
            return render(req,'doctor/error.html')

def editFirm(request, pk):
    permcheck = checkForPermission(request,"doctor.change_empanelledfirm")
    if permcheck == 1:
        data = EmpanelledFirm.objects.get(firm_id = pk)
        ctx = {
            'data': {
                'id': data.firm_id,
                'name': data.firm_name,
                'email': data.firm_email,
                'phone': data.firm_phone
            }
        }
    return render(request,'doctor/addFirm.html', ctx)

def deleteFirm(request, pk):
    permcheck = checkForPermission(request, "doctor.delete_empanelledfirm")
    if permcheck == 1:
        EmpanelledFirm.objects.filter(firm_id=pk).delete()
        return redirect('display-firm-view')
    else:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
def addFirm(request):
    permcheck=checkForPermission(request,"doctor.add_empanelledfirm")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        return render(request,'doctor/addFirm.html')

def insertIntoFirm(request):
    permcheck = checkForPermission(request, "doctor.add_empanelledfirm")
    if permcheck == 1 and request.method == "POST":
        id=request.POST["firm-id"]
        name=request.POST["firm-name"]
        email=request.POST["firm-email"]
        phone=request.POST["firm-phone"]

        print(id)
        
        obj, created = EmpanelledFirm.objects.update_or_create(
            firm_id = id,

            defaults = {
                'firm_name' : name,
                'firm_email': email,
                'firm_phone': phone,
            }
        )

        return redirect('display-firm-view')
    return redirect(request,'doctor/error.html')

def displayMedicine(req):
    user = req.user
    if user.is_authenticated:
        if user.has_perm("doctor.view_medicine") and user.has_perm("doctor.view_stockmedicine"):
            data_stockmeds= StockMedicine.objects.order_by('medicine_id','expiry_date')
            l = []
            for i in data_stockmeds:
                d = {
                    'name': i.medicine_id,
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

def displayRequisiton(request):
    permcheck=checkForPermission(request,"doctor.view_requisition")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        data=Requisition.objects.all()
        l=[]
        for i in data:
            l.append(i)
        ctx={
            'data':l
        }
        return render(request,'doctor/requisition.html',context=ctx)

def addRequistion(request):
    permcheck=checkForPermission(request,"doctor.add_requisition")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        return render(request,'doctor/addRequisition.html')

def insertIntoRequisition(request):
    permcheck = checkForPermission(request, "doctor.add_requisition")
    if permcheck == 1 and request.method == "POST":
        r_id=request.POST["req-id"]
        doo=request.POST["date-of-order"]
        amt=request.POST["amt"]
        doa=request.POST["date-of-approval"]
        memo=request.POST["memo"]
        try:
            Requisition.objects.create(requisition_id=r_id,date_of_order=doo,amount=amt,date_of_approval=doa,memo=memo)
        except IntegrityError as e:
            return render(request,'doctor/error.html',{'msg':'Requisition with provided ID already exists'})
        return redirect('display-requisition-view')
    return render(request,'doctor/error.html')


def displayRequisitionProposal(request):
    permcheck=checkForPermission(request,"doctor.view_doctorrequisitionproposal")
    if permcheck==-1:
        return redirect('login-view')
    if permcheck==0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        data=DoctorRequisitionProposal.objects.all()
        l=[]
        for i in data:
            print(i.medicine_id)
            l.append(i)
        ctx={
            'data':l
        }
        return render(request,'doctor/requisitionproposal.html',context=ctx)
def addRequisitionProposal(request):
    permcheck=checkForPermission(request,"doctor.add_doctorrequisitionproposal")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        req_ids = Requisition.objects.all().values("requisition_id")
        rids = []
        for i in req_ids:
            rids.append(i["requisition_id"])
        med_ids = Medicine.objects.all().values("medicine_id", "medicine_name").order_by("medicine_name")
        meds = []
        for i in med_ids:
            meds.append(i)
        staff=HealthCentreStaff.objects.filter(staff_type="DR").values("staff_id","staff_name").order_by("staff_name")
        ctx = {
            'req_ids': rids,
            'meds': meds,
            'staff':staff
        }
        return render(request,'doctor/addRequisitionProposal.html',context=ctx)

def insertIntoRequisitionProposal(request):
    permcheck=checkForPermission(request,"doctor.add_doctorrequisitionproposal")
    if permcheck==1 and request.method=='POST':
        new_entry=DoctorRequisitionProposal()
        req=Requisition.objects.filter(requisition_id=request.POST["req-id"])[0]
        staff=HealthCentreStaff.objects.filter(staff_id=request.POST["staff-id"])[0]
        med=Medicine.objects.filter(medicine_id=request.POST["med-id"])[0]
        new_entry.add_requisiton_proposal(req,staff,med,request.POST["qty"])
        return redirect('display-doctorrequisitionproposal-view')
    return render(request,'doctor/error.html')

def addStock(request):
    permcheck=checkForPermission(request,"doctor.add_stock")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        l=[]
        for i in EmpanelledFirm.objects.all().values("firm_id","firm_name"):
            l.append(i)
        ctx={
            'data':l
        }
        return render(request,'doctor/addStock.html',context=ctx)

def insertIntoStock(request):
    permcheck = checkForPermission(request, "doctor.add_stock")
    if permcheck == 1 and request.method == 'POST':
        ba_no=request.POST["batch-number"]
        bi_no=request.POST["bill-number"]
        bi_date=request.POST["bill-date"]
        f_id=EmpanelledFirm.objects.filter(firm_id=request.POST["firm-id"])[0]
        try:
            Stock.objects.create(batch_no=ba_no,bill_no=bi_no,bill_date=bi_date,firm_id=f_id)
            return redirect('doctor-home-view')
        except IntegrityError as err:
            return render(request, 'doctor/error.html',{'msg':'Stock with same batch number exists'})
    return render(request, 'doctor/error.html')

def addStockMedicine(request):
    permcheck=checkForPermission(request,"doctor.add_stockmedicine")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        bns=[i for i in Stock.objects.all().values('batch_no')]
        meds=[i for i in Medicine.objects.all().values('medicine_id','medicine_name').order_by('medicine_name')]
        ctx={
            'batch_no':bns,
            'meds':meds
        }
        return render(request,'doctor/addStockMedicine.html',context=ctx)
def insertIntoStockMedicine(request):
    permcheck = checkForPermission(request, "doctor.add_stockmedicine")
    if permcheck == 1 and request.method=='POST':
        med=Medicine.objects.filter(medicine_id=request.POST["med-id"])[0]
        batch=Stock.objects.filter(batch_no=request.POST["batch-no"])[0]
        qty=request.POST["qty"]
        exp_date=request.POST["expiry-date"]
        med_rate=request.POST["medicine-rate"]
        try:
            StockMedicine.objects.create(batch_no=batch,medicine_id=med,quantity=qty,expiry_date=exp_date,medicine_rate=med_rate)
            return redirect('display-medicine')
        except IntegrityError as e:
            return render(request,'doctor/error.html',{'msg':''})
    return render(request,'doctor/error.html')
