from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login,logout,authenticate
from .models import *
from django.db import IntegrityError
from django.contrib.auth.models import User,Group
# Create your views here.

def getUserId(request):
    user = User.objects.get(username = request.user).id
    return user

def indexView(request):
    return render(request,'doctor/index.html')


def loginView(request):
    if request.method=='POST':
        user_name=request.POST['username-login']
        pwd=request.POST['pwd-login']
        user=authenticate(username=user_name,password=pwd)
        if user is not None:
            login(request,user)
            # if request.user.groups.filter(name__in=['doctor', 'pharmacist']).exists():
            #     id = User.objects.get(username = user).id
            #     try:
            #         HealthCentreStaff.objects.get(user_id = id)
            #     except ObjectDoesNotExist:
            #         return redirect('add-staff-view')
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
        u_id = User.objects.get(username = request.user)

        obj, created = HealthCentreStaff.objects.update_or_create(
            user_id=u_id,

            defaults={
                'staff_id': id,
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
        data=RequisitionMedicine.objects.all().order_by("requisition_id","medicine_id__medicine_name")
        l=[]
        for i in data:
            d={
                'pkey':i.pk,
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


def addRequisitionMedicine(request,**kwargs):
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
        if "data" in kwargs:
            ctx["data"]=kwargs["data"]
        return render(request,'doctor/addRequisitionMedicine.html',context=ctx)

def insertIntoRequisitionMedicine(request):
    permcheck=checkForPermission(request,"doctor.add_requisitionmedicine")
    if permcheck==1 and request.method=="POST":
        r_id = int(request.POST["req-id"])
        requisition = Requisition.objects.filter(requisition_id=r_id)[0]
        m_id = int(request.POST["med-id"])
        # print(requisition)
        medicine = Medicine.objects.filter(medicine_id=m_id)[0]
        q_req = request.POST["qty-requested"]
        q_rec = request.POST["qty-received"]
        if int(request.POST["p-key"])==-101:
            new_entry=RequisitionMedicine()
            new_entry.add_requisition_medicine(requisition,medicine,q_req,q_rec)
        else:
            p_key=int(request.POST["p-key"])
            RequisitionMedicine.objects.filter(pk=p_key).update(requisition_id=requisition,medicine_id=medicine,quantity_requested=q_req,quantity_received=q_rec)
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
    return render(request,'doctor/error.html')
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
        create=int(request.POST["create"])
        try:
            if create==1:
                Requisition.objects.create(requisition_id=r_id,date_of_order=doo,amount=amt,date_of_approval=doa,memo=memo)
            else:
                Requisition.objects.update_or_create(
                    requisition_id=r_id,
                    defaults={
                        'date_of_order':doo,
                        'amount':amt,
                        'date_of_approval':doa,
                        'memo':memo
                    }
                )
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
            # print(i.medicine_id)
            l.append(i)
        ctx={
            'data':l
        }
        return render(request,'doctor/requisitionproposal.html',context=ctx)
def addRequisitionProposal(request,**kwargs):
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
        staff=HealthCentreStaff.objects.all().values("staff_id","staff_name").order_by("staff_name")

        ctx = {
            'req_ids': rids,
            'meds': meds,
            'staff':staff
        }

        if "data" in kwargs:
            ctx["data"]=kwargs["data"]

        return render(request,'doctor/addRequisitionProposal.html',context=ctx)

def insertIntoRequisitionProposal(request):
    permcheck=checkForPermission(request,"doctor.add_doctorrequisitionproposal")
    if permcheck==1 and request.method=='POST':
        req = Requisition.objects.filter(requisition_id=request.POST["req-id"])[0]
        staff = HealthCentreStaff.objects.filter(staff_id=request.POST["staff-id"])[0]
        med = Medicine.objects.filter(medicine_id=request.POST["med-id"])[0]
        qty=request.POST["qty"]
        if int(request.POST["p-key"])==-101:
            new_entry = DoctorRequisitionProposal()
            new_entry.add_requisiton_proposal(req,staff,med,qty)
        else:
            p_key=int(request.POST["p-key"]);
            DoctorRequisitionProposal.objects.filter(pk=p_key).update(requisition_id=req,doctor_id=staff,medicine_id=med,quantity=qty)
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

        obj, created = StockMedicine.objects.update_or_create(
            batch_no = batch,
            medicine_id=med,
            defaults = {
            'quantity': qty,
            'expiry_date': exp_date,
            'medicine_rate': med_rate,
            }
        )
        return redirect('display-medicine')
    return render(request,'doctor/error.html')


def editRequistion(request,pk):
    permcheck=checkForPermission(request,"doctor.change_requisition")
    if permcheck==1:
        res=Requisition.objects.get(requisition_id=pk)
        ctx={
            'data':res
        }
        return render(request,'doctor/addRequisition.html',context=ctx)
    return render(request,'doctor/error.html')

def deleteRequisition(request,pk):
    permcheck=checkForPermission(request,"doctor.delete_requisiton")
    if permcheck == 1:
        Requisition.objects.filter(requisition_id=pk).delete()
        return redirect('display-requisition-view')
    else:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")

def editRequisitionMedicine(request,pk):
    permcheck=checkForPermission(request,"doctor.change_requisitionmedicine")
    if permcheck==1:
        res = RequisitionMedicine.objects.get(pk=pk)
        return addRequisitionMedicine(request,data=res)
    return render(request,"doctor/error.html")

def deleteRequisitionMedicine(request,pk):
    permcheck=checkForPermission(request,"doctor.delete_requisitionmedicine")
    if permcheck==1:
        RequisitionMedicine.objects.get(pk=pk).delete()
        return redirect('display-requisitionmedicine-view')
    return render(request,'doctor/error.html',{'msg':'Operation not performed..You may not have the required permissions'})

def editRequisitionProposal(request,pk):
    permcheck = checkForPermission(request, "doctor.change_doctorrequisitionproposal")
    if permcheck==1:
        res=DoctorRequisitionProposal.objects.get(pk=pk)
        return addRequisitionProposal(request,data=res)
    return render(request,"doctor/error.html")

def deleteRequisitionProposal(request,pk):
    permcheck = checkForPermission(request, "doctor.delete_doctorrequisitionproposal")
    if permcheck == 1:
        DoctorRequisitionProposal.objects.get(pk=pk).delete()
        return redirect('display-doctorrequisitionproposal-view')
    return render(request, "doctor/error.html",{'msg':'Deletion failed...you may not have the required permissions'})

def viewMyPatients(request):
    permcheck = checkForPermission(request, "doctor.view_patientrecord")
    isDoc = False
    if permcheck == 1:
        print (getUserId(request))
        try:
            staff_id = HealthCentreStaff.objects.get(user_id = getUserId(request))
        except ObjectDoesNotExist:
            return render(request, 'doctor/error.html')
        try:
            data = PatientRecord.objects.filter(doctor_id = staff_id)
            print(data)
        except ObjectDoesNotExist:
            data = []
        isDoc = True
        return render(request, 'doctor/myPatients.html', {'data': data, 'isDoc': isDoc})
    return render(request,'doctor/error.html')

def addPatientRecord(request):
    permcheck = checkForPermission(request, "doctor.add_patientrecord")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck == 1:
        patId = [i for i in StudentRecord.objects.all().values('person_id')]
        return render(request, 'doctor/addNewPatient.html',{'patId':patId})

def insertIntoPatientRecord(request):
    permcheck = checkForPermission(request, "doctor.add_patientrecord")
    if permcheck == 1 and request.method == "POST":
        person_id = request.POST["person-id"]
        complaint = request.POST["complaint"]
        diagnosis = request.POST["diagnosis"]
        isDependant = request.POST["dependent"]
        testRecommended = request.POST["recommended-test"]
        test_result = request.POST["test-result"]
        fup_date = request.POST["fup-date"]
        u_id = HealthCentreStaff.objects.get(user_id = getUserId(request))
        obj, created = PatientRecord.objects.update_or_create(
            doctor_id=u_id,
            patient_id_id = person_id,

            defaults={
                'complaint': complaint,
                'daignosis': diagnosis,
                'isDependant': isDependant,
                'testRecommended': testRecommended,
                'test_result': test_result,
                'follow_up_date': fup_date
            }
        )

        return redirect('display-mypatients-view')
    return redirect(request, 'doctor/error.html')

def displayPrescription(request):
    permcheck = checkForPermissions(request, "doctor.view_prescription","doctor.view_medicineissue")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck == 1:
        user_type=None
        data=None
        if request.user.groups.filter(name="doctor").exists():
            user_type="doctor"
            dr=HealthCentreStaff.objects.get(user_id=request.user.id).staff_id
            data=Prescription.objects.all().filter(doctor_id=dr).values('prescription_serial_no').order_by('prescription_serial_no')
        else:
            user_type="patient"
        ctx={
            'data':data
        }
        if request.method=='GET' and 'prescription-no' in request.GET:
            ctx['presc_data']=MedicineIssue.objects.all().filter(prescription_serial_no=request.GET["prescription-no"])
            ctx['selected']=request.GET["prescription-no"]
            ctx['get_acc']=True
        return render(request, 'doctor/prescription.html', context=ctx)

def addPrescription(request):
    permcheck=checkForPermission(request,'doctor.add_prescription')
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck ==1:
        dr = HealthCentreStaff.objects.get(user_id=request.user.id).staff_id
        people=[i for i in StudentRecord.objects.all().values("person_id")];
        ctx={
            'staff_id':dr,
            'people':people
        }
        return render(request,'doctor/addPrescription.html',context=ctx)

def insertIntoPrescription(request):
    permcheck = checkForPermission(request, 'doctor.add_prescription')
    if permcheck==1 and request.method=='POST':
        psn=request.POST["presc-serial-no"]
        doi=request.POST["date-of-issue"]
        si=HealthCentreStaff.objects.get(staff_id=request.POST["staff-id"])
        pi=StudentRecord.objects.get(person_id=request.POST["person-id"])

        i=request.POST["issued"]
        try:
            Prescription.objects.create(prescription_serial_no=psn,date_of_issue=doi,doctor_id=si,patient_id=pi,issued=i)
            return redirect('display-prescription-view')
        except IntegrityError as e:
            return render(request, 'doctor/error.html', {'msg': 'Prescription with same ID exists'})
    return render(request, 'doctor/error.html')


def addMedicineIssue(req,presc_no):
    permcheck = checkForPermission(req, 'doctor.add_medicineissue')
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck == 1:
        meds = [i for i in Medicine.objects.all().values('medicine_id', 'medicine_name').order_by('medicine_name')]
        ctx={
            'p_no':Prescription.objects.get(prescription_serial_no=presc_no),
            'meds':meds,
            'type':'doctor'
        }
        print(ctx['p_no'])
        return render(req,'doctor/addMedicineIssue.html',context=ctx)

def insertIntoMedicineIssue(request):
    permcheck = checkForPermission(request, 'doctor.add_medicineissue')
    if permcheck==1 and request.method=='POST':
        p=Prescription.objects.get(prescription_serial_no=request.POST['presc-serial-no'])
        doi=request.POST['date-of-issue']
        m=Medicine.objects.filter(medicine_id=request.POST['med-id'])[0]
        qty=request.POST['med-qty']
        i=request.POST['med-issued']
        nii=request.POST['nii']
        MedicineIssue.objects.create(prescription_serial_no=p,medicine_id=m,medicine_quantity=qty,issue_status=i,non_issue_reason=nii)
        return redirect(reverse('display-prescription-view')+"?prescription-no="+p.prescription_serial_no)
    return render(request, 'doctor/error.html')

def checkForPermissions(request,*args):
    user=request.user
    if user.is_authenticated:
        for i in args:
            if not user.has_perm(i):
                return 0
        return 1
    return -1

def deleteMedicineIssue(request,pk):
    permcheck = checkForPermission(request, "doctor.delete_medicineissue")
    if permcheck == 1:
        p_no=MedicineIssue.objects.get(pk=pk).prescription_serial_no_id
        MedicineIssue.objects.get(pk=pk).delete()
        return redirect(reverse('display-prescription-view')+"?prescription-no="+p_no)
    return render(request, "doctor/error.html", {'msg': 'Deletion failed...you may not have the required permissions'})


def submitFeedback(request):
    if request.method=='POST':
        fb=request.POST["feedback"]
        username=request.user.username
        Feedback.objects.create(user=username,feedback=fb)
        return redirect('doctor-home-view')
    return render(request,'doctor/error.html',{'msg':'Something\'s wrong. Please try again.'})


def addMedicine(request):
    permcheck = checkForPermission(request, 'doctor.add_medicine')
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck == 1:

        return render(request, 'doctor/addMedicine.html')

def insertIntoMedicine(request):
    permcheck = checkForPermission(request, 'doctor.add_medicine')
    if permcheck==1 and request.method=='POST':
        med_id=request.POST["med-id"]
        med_name=request.POST["med-name"]
        company=request.POST["company"]
        qty=request.POST["med-qty"]
        cat=request.POST["med-cat"]
        Medicine.objects.update_or_create(medicine_id=med_id,defaults={
            'medicine_name':med_name,
            'manufacturing_company':company,
            'quantity':qty,
            'category':cat
        })
        return redirect('doctor-home-view')
    return render(request, 'doctor/error.html')