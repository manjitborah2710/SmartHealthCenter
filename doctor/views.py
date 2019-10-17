from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login,logout,authenticate
from .models import *
from django.db import IntegrityError
from django.contrib.auth.models import User,Group
# Create your views here.

# get user id
def getUserId(request):
    user = User.objects.get(username = request.user).id
    return user

#check if a user has a specific permission
def checkForPermission(request,permission):
    user=request.user
    if user.is_authenticated:
        if user.has_perm(permission):
            return 1
        return 0
    return -1

#check if user is a pharmacist
def checkIfPharmacist(request):
    if request.user.groups.filter(name__in=['pharmacist']).exists():
        return True
    return False

#view the index page (the landing page of the website)
def indexView(request):
    return render(request,'doctor/index.html')


#view the login page
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


#view the home page, the one with all the navigation buttons
def homeView(request):
    user=request.user
    if not user.is_authenticated:
        return redirect('login-view')
    return render(request,'doctor/home.html')

#for logging out of the website
def log_out(req):
    logout(req)
    return redirect('login-view')

#view all the Health centre staffs ie doctors, nurses, pharmacists
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

#add a new health centre staff ie doctor, nurse, pharmacist, etc
def addHealthCenterStaff(request):
    permcheck=checkForPermission(request,"doctor.add_healthcentrestaff")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        return render(request,'doctor/addStaff.html')

#edit the info of a health centre staff
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

#delete the record of a health centre staff
def deleteHealthCenterStaff(request, pk):
    permcheck = checkForPermission(request, "doctor.delete_healthcentrestaff")
    if permcheck == 1:
        HealthCentreStaff.objects.filter(staff_id=pk).delete()
        return redirect('display-staff-view')
    else:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")

#actually inserts into the table, this interacts with the databse
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


#display all the stores, shops, medicine centers from where medicines are purchased
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

#edit the information of a firm
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

#remove the record of a firm
def deleteFirm(request, pk):
    permcheck = checkForPermission(request, "doctor.delete_empanelledfirm")
    if permcheck == 1:
        EmpanelledFirm.objects.filter(firm_id=pk).delete()
        return redirect('display-firm-view')
    else:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")

#add a new firm
def addFirm(request):
    permcheck=checkForPermission(request,"doctor.add_empanelledfirm")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        return render(request,'doctor/addFirm.html')

#actually inserts into the database
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

#view all the medicines that are there in the stock
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

#insert a new medicine into the stock
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

#actually interacts with the database
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

#for entering feedback about the website
def submitFeedback(request):
    if request.method=='POST':
        fb=request.POST["feedback"]
        username=request.user.username
        Feedback.objects.create(user=username,feedback=fb)
        return redirect('doctor-home-view')
    return render(request,'doctor/error.html',{'msg':'Something\'s wrong. Please try again.'})

#for the doctors to view all their patients
def viewMyPatients(request):
    permcheck = checkForPermission(request, "doctor.view_patientrecord")
    print(permcheck)
    isDoc = False
    if permcheck == 1:
        try:
            staff_id = HealthCentreStaff.objects.get(user_id = getUserId(request))
        except ObjectDoesNotExist:
            return render(request, 'doctor/error.html',{'msg':'No data found'})
        try:
            data = PatientRecord.objects.filter(doctor_id = staff_id).order_by('-date_created')
            print(data)
        except ObjectDoesNotExist:
            data = []
        isDoc = True
        return render(request, 'doctor/myPatients.html', {'data': data, 'isDoc': isDoc})
    return render(request,'doctor/error.html')

#for the doctors to add a new patient file
def addPatientRecord(request):
    permcheck = checkForPermission(request, "doctor.add_patientrecord")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck == 1:
        patId = [i for i in StudentRecord.objects.all().values('person_id')]
        return render(request, 'doctor/addNewPatient.html',{'patId':patId})

#this actually inserts the patient file into the database
def insertIntoPatientRecord(request):
    permcheck = checkForPermission(request, "doctor.add_patientrecord")
    if permcheck == 1 and request.method == "POST":
        person_id = request.POST["person-id"]
        today_date = request.POST["today-date"]
        height = request.POST["height"]
        weight = request.POST["weight"]
        isDependant = request.POST["dependent"]
        u_id = HealthCentreStaff.objects.get(user_id = getUserId(request))

        obj, created = PatientRecord.objects.update_or_create(
            doctor_id = u_id,
            patient_id_id = person_id,

            defaults={
                'date_created': today_date,
                'height': height,
                'weight': weight,
                'isDependant': isDependant
            }
        )
        return redirect('display-mypatients-view')
    return redirect(request, 'doctor/error.html')

#a doctor can view the file of one patient using this. it lists all the prescriptions issued
def displayIndividualRecord(request,patient_id):
    permcheck = checkForPermission(request, "doctor.view_patientrecord")
    if permcheck == 1:
        data = PatientRecord.objects.filter(id = patient_id)
        presData = Prescription.objects.filter(patient_record_id=patient_id).order_by("-date_of_issue")
        ctx = {
            'id' : patient_id,
            'data': data,
            'presData': presData,
        }
        return render(request, 'doctor/individualRecord.html', ctx)
    return render(request, 'doctor/error.html')

#a doctor or a pharmacist can view a prescription of a patient and
# see the medicines that were prescribed and tests that were recommended
def displayPrescription(request,pres_id=1001):
    permcheck = checkForPermissions(request, "doctor.view_prescription","doctor.view_medicineissue")
    isPharm = checkIfPharmacist(request)
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck == 1:
        data=Prescription.objects.filter(prescription_serial_no=pres_id)
        name = data[0].patient_record_id.patient_id
        meds_pres = ""
        tests_recom = ""
        isPharm=checkIfPharmacist(request)
        if data[0].medicine_prescribed:
            meds_pres = MedicineIssue.objects.filter(prescription_serial_no=pres_id)
        if data[0].tests_recommended:
            tests_recom = RecommendedTest.objects.filter(prescription_serial_no=pres_id)
        ctx = {'data' : data[0],
               'name': name,
               'meds_pres': meds_pres,
               'tests_recom': tests_recom,
               'isPharm': isPharm,
               }
        return render(request, 'doctor/prescription.html', context=ctx)
    return render(request, 'doctor/error.html')

#a doctor can issue a new prescription to a patient using this
def addPrescription(request,record_id):
    permcheck=checkForPermission(request,'doctor.add_prescription')
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck ==1:
        ctx={
            'record_id':record_id,
        }
        return render(request,'doctor/addPrescription.html',context=ctx)

#this actually add the new prescription into the database
def insertIntoPrescription(request):
    permcheck = checkForPermission(request, 'doctor.add_prescription')
    if permcheck==1 and request.method=='POST':
        try:
            id_data = Prescription.objects.all().order_by('-prescription_serial_no')[0]
            id =  int(id_data.prescription_serial_no) + 1
        except:
            id = 1001
        record_id = request.POST["rec-id"]
        issue_date = request.POST["date-of-issue"]
        complaint = request.POST["complaint"]
        diagnosis = request.POST["diagnosis"]
        followup_date = request.POST["fup-date"]
        if followup_date=="":
            followup_date=None
        med_pres = request.POST["med-pres"]
        test_recom = request.POST.get("test-recom")
        try:
            Prescription.objects.create(
                prescription_serial_no =id,
                date_of_issue=issue_date,
                complaint=complaint,
                diagnosis=diagnosis,
                followup_date=followup_date,
                patient_record_id_id=record_id,
                medicine_prescribed=med_pres,
                tests_recommended=test_recom
                )

            if med_pres == '1':
                return redirect('add-medicineissue-view', id)
            return redirect('display-individualrecord-view', record_id)
        except IntegrityError as e:
            return render(request, 'doctor/error.html')
    return render(request, 'doctor/error.html')

#medicines are prescribed by a doctor to a patient using this
def addMedicineIssue(req, presc_no):
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

#this adds the prescribed medicine into the database
def insertIntoMedicineIssue(request):
    permcheck = checkForPermission(request, 'doctor.add_medicineissue')
    if permcheck==1 and request.method=='POST':
        pres_id = request.POST['presc-serial-no']
        p=Prescription.objects.get(prescription_serial_no=pres_id)
        record_id = p.patient_record_id_id
        doi=request.POST['date-of-issue']
        m=Medicine.objects.filter(medicine_id=request.POST['med-id'])[0]
        qty=request.POST['med-qty']
        i=request.POST['med-issued']
        nii=request.POST['nii']
        MedicineIssue.objects.create(prescription_serial_no=p,medicine_id=m,medicine_quantity=qty,issue_status=i,non_issue_reason=nii)

        if 'submit&cont' in request.POST:
            return redirect('add-medicineissue-view', pres_id)
        elif 'submit' in request.POST:
            return redirect('display-individualrecord-view', record_id)

    return render(request, 'doctor/error.html')

#this is used by a doctor to delete a prescribed medicine
def deleteMedicineIssue(request,pk):
    permcheck = checkForPermission(request, "doctor.delete_medicineissue")
    if permcheck == 1:
        p_no=MedicineIssue.objects.get(pk=pk).prescription_serial_no_id
        MedicineIssue.objects.get(pk=pk).delete()
        return redirect(reverse('display-prescription-view')+"?prescription-no="+p_no)
    return render(request, "doctor/error.html", {'msg': 'Deletion failed...you may not have the required permissions'})

#a pharmacist can issue medicines that are prescribed by a doctor using this
#this is currently not working properly as medicine_id_id returns a multivalued set
#update function updates every tuple's quantity value
def issueMedicine(request, presc_no, med_id):
    if checkIfPharmacist(request):
        med = MedicineIssue.objects.filter(medicine_id_id=med_id)
        issue_quantity = med[0].medicine_quantity
        stock_med = StockMedicine.objects.filter(medicine_id_id=med_id)
        if stock_med.exists():
            stock_quantity = stock_med[0].quantity
        else:
            stock_quantity = 0
        if stock_quantity>issue_quantity:
            new = stock_quantity - issue_quantity
            print (new)
            stock_med.update(quantity=new)
            med.update(issue_status=1)
        return redirect('display-prescription-view',presc_no)
    return render(request, "doctor/error.html", {'msg': 'You do not have the permission for this action'})

#this is probably redundant
def checkForPermissions(request,*args):
    user=request.user
    if user.is_authenticated:
        for i in args:
            if not user.has_perm(i):
                return 0
        return 1
    return -1

#this is used for adding a new medicine into the database.
#this differs from stock medicine as stock medicine gives us an idea about
# the medicines currently in stock while this just add a new kind of medicine into the database
def addMedicine(request):
    permcheck = checkForPermission(request, 'doctor.add_medicine')
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck == 1:

        return render(request, 'doctor/addMedicine.html')

#this actually interacts with the database
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
