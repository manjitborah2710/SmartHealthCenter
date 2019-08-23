from django.shortcuts import render,redirect
from django.http import HttpResponse


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