from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login,logout,authenticate
from .models import *
from django.db import IntegrityError
from django.contrib.auth.models import User,Group

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
from itertools import chain

from django.db.models import Max,Min,Sum,Avg,Q
import json
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


def checkIfCommitteeMember(request):
    if request.user.groups.filter(name__in=['approval_committee']).exists():
        return True
    return False

def checkIfDoctor(request):
    if request.user.groups.filter(name__in=['doctor']).exists():
        return True
    return False

#view the index page (the landing page of the website)
def indexView(request):
    if request.user.is_authenticated:
        return loginView(request)
    return redirect('login-view')


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
    return HttpResponse("You do not have permissions for this operation")

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
            data_all=filterFirms(req,data_all)
            paginator = Paginator(data_all, 10)
            page = req.GET.get('page')
            data = paginator.get_page(page)
            l = []
            for i in data:
                d={
                    'id': i.id,
                    'name' : i.firm_name,
                    'dil_no' : i.firm_dilno,
                    'gst_no' : i.firm_gstno,
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
        data = EmpanelledFirm.objects.get(id = pk)
        ctx = {
            'data': {
                'id': data.id,
                'name': data.firm_name,
                'dil_no': data.firm_dilno,
                'gst_no': data.firm_gstno,
                'phone': data.firm_phone
            }
        }
        return render(request,'doctor/addFirm.html', ctx)
    return render(request,'doctor/error.html')

#remove the record of a firm
def deleteFirm(request, pk):
    permcheck = checkForPermission(request, "doctor.delete_empanelledfirm")
    if permcheck == 1:
        EmpanelledFirm.objects.filter(id=pk).delete()
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
        dil_no=request.POST["firm-dilno"]
        gst_no=request.POST["firm-gstno"]
        phone=request.POST["firm-phone"]

        print(request.POST["edit_or_add"])
        
        
        #edit
        if request.POST["edit_or_add"]=='0':
            EmpanelledFirm.objects.filter(id=id).update(
                firm_name = name,
                firm_dilno= dil_no,
                firm_gstno= gst_no,
                firm_phone= phone,
        )
        #add
        elif request.POST["edit_or_add"]=='1':
            print("Here\n\n\n\n")
            EmpanelledFirm.objects.create(
                firm_name = name,
                firm_dilno= dil_no,
                firm_gstno= gst_no,
                firm_phone= phone,
        )

        return redirect('display-firm-view')
    return redirect(request,'doctor/error.html')

#view all the medicines that are there in the stock
def displayMedicine(req):
    user = req.user
    if user.is_authenticated:
        if user.has_perm("doctor.view_medicine") and user.has_perm("doctor.view_stockmedicine"):
            data_stockmeds= StockMedicine.objects.order_by('medicine_id__medicine_name','expiry_date')
            l = []
            for i in data_stockmeds:
                d = {
                    'name': i.medicine_id,
                    'category': i.medicine_id.category,
                    'bill_no': i.bill_no,
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
        bns=[i for i in Bill.objects.all().values('bill_no')]
        meds=[i for i in Medicine.objects.all().values('medicine_id','medicine_name').order_by('medicine_name')]
        ctx={
            'bill_no':bns,
            'meds':meds
        }
        return render(request,'doctor/addStockMedicine.html',context=ctx)

#actually interacts with the database
def insertIntoStockMedicine(request):
    permcheck = checkForPermission(request, "doctor.add_stockmedicine")
    if permcheck == 1 and request.method=='POST':
        med=Medicine.objects.filter(medicine_id=request.POST["med-id"])[0]
        bill=Bill.objects.filter(bill_no=request.POST["bill-no"])[0]
        qty=request.POST["qty"]
        exp_date=request.POST["expiry-date"]
        med_rate=request.POST["medicine-rate"]

        obj, created = StockMedicine.objects.update_or_create(
            bill_no = bill,
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
            'data':l,
            'user_id':request.user.id,
            'isCommittee':checkIfCommitteeMember(request)
        }
        return render(request,'doctor/requisitionproposal.html',context=ctx)

def addRequisitionProposal(request,**kwargs):
    permcheck=checkForPermission(request,"doctor.add_doctorrequisitionproposal")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        req_ids = Requisition.objects.filter(closed=False).values("requisition_id")
        rids = []
        for i in req_ids:
            rids.append(i["requisition_id"])
        med_ids = Medicine.objects.all().values("medicine_id", "medicine_name").order_by("medicine_name")
        meds = []
        for i in med_ids:
            meds.append(i)
        staff=HealthCentreStaff.objects.filter(user_id_id=request.user.id).values("staff_id","staff_name")

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


def displayRequisitionMedicine(request,pk):
    user=request.user
    permcheck=checkForPermission(request,"doctor.view_requisitionmedicine")
    if permcheck==-1:
        return redirect('login-view')
    if permcheck==0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        data=RequisitionMedicine.objects.filter(requisition_id=pk).order_by("requisition_id","medicine_id__medicine_name")
        l=[]
        for i in data:
            d={
                'pkey':i.pk,
                'req_id':i.requisition_id,
                'med_id':i.medicine_id,
                'qty_requested':i.quantity_requested,
                'qty_received':i.quantity_received,
            }
            l.append(d)
        closed_status=Requisition.objects.get(requisition_id=pk).closed
        ctx={
            'data':l,
            'req':pk,
            'isClosed':closed_status
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
        isClosed=requisition.closed
        if isClosed:
            return render(request,'doctor/error.html',context={'msg':'This list has been closed and you cannot enter any more medicines here'})
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
        return redirect(reverse('display-requisitionmedicine-view',kwargs={'pk':r_id}))

    return render(request,'doctor/error.html')

def addBill(request):
    permcheck=checkForPermission(request,"doctor.add_stock")
    if permcheck == -1:
        return redirect('login-view')
    if permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    if permcheck==1:
        l=[]
        for i in EmpanelledFirm.objects.all().values("id","firm_name"):
            l.append(i)
        ctx={
            'data':l
        }
        return render(request,'doctor/addBill.html',context=ctx)

def insertBill(request):
    permcheck = checkForPermission(request, "doctor.add_stock")
    if permcheck == 1 and request.method == 'POST':
        bi_no=request.POST["bill-number"]
        bi_date=request.POST["bill-date"]
        f_id=EmpanelledFirm.objects.filter(id=request.POST["firm-id"])[0]
        try:
            Bill.objects.create(bill_no=bi_no,bill_date=bi_date,firm_id=f_id)
            return redirect('doctor-home-view')
        except IntegrityError as err:
            return render(request, 'doctor/error.html',{'msg':'Stock with same bill number exists'})
    return render(request, 'doctor/error.html')

def editRequistion(request,pk):
    permcheck=checkForPermission(request,"doctor.change_requisition")
    if permcheck==1:
        res=Requisition.objects.get(requisition_id=pk)
        ctx={
            'data':res
        }
        return render(request,'doctor/addRequisition.html',context=ctx)
    return HttpResponse("<p>You do not have the permissions for this operation</p>")

def deleteRequisition(request,pk):
    permcheck=checkForPermission(request,"doctor.delete_requisition")
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
    return HttpResponse("<p>You do not have the permissions for this operation</p>")

def deleteRequisitionMedicine(request,pk):
    permcheck=checkForPermission(request,"doctor.delete_requisitionmedicine")
    if permcheck==1:
        r_id=RequisitionMedicine.objects.get(pk=pk).requisition_id
        RequisitionMedicine.objects.get(pk=pk).delete()
        return redirect(reverse('display-requisitionmedicine-view',kwargs={'pk':r_id}))
    return HttpResponse("<p>You do not have the permissions for this operation</p>")

def editRequisitionProposal(request,pk,user_id):
    if (user_id==request.user.id):
        permcheck = checkForPermission(request, "doctor.change_doctorrequisitionproposal")
        if permcheck==1:
            res=DoctorRequisitionProposal.objects.get(pk=pk)
            return addRequisitionProposal(request,data=res)
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    return HttpResponse("<h1 style='color:red'>YOU ARE TRYING TO EDIT DATA YOU HAVE NOT ADDED</h1>")

def deleteRequisitionProposal(request,pk,user_id):
    permcheck = checkForPermission(request, "doctor.delete_doctorrequisitionproposal")
    if permcheck == 1:
        DoctorRequisitionProposal.objects.get(pk=pk).delete()
        return redirect('display-doctorrequisitionproposal-view')
    return render(request, "doctor/error.html",{'msg':'Deletion failed...you may not have the required permissions'})

#for entering feedback about the website
#this is the most important part of the entire website
#a project without feedback is like a ship without a rudder
def submitFeedback(request):
    if request.method=='POST':
        fb=request.POST["feedback"]
        username=request.user.username
        Feedback.objects.create(user=username,feedback=fb)
        return redirect('doctor-home-view')
    return render(request,'doctor/error.html',{'msg':'Something\'s wrong. Please try again.'})

#for the doctors to view all their patients
# def viewMyPatients(request):
#     permcheck = checkForPermission(request, "doctor.view_patientrecord")
#     print(permcheck)
#     isDoc = False
#     if permcheck == 1:
#         try:
#             staff_id = HealthCentreStaff.objects.get(user_id = getUserId(request))
#         except ObjectDoesNotExist:
#             return render(request, 'doctor/error.html',{'msg':'No data found'})
#         try:
#             data = PatientRecord.objects.filter(doctor_id = staff_id).order_by('-date_created')
#             print(data)
#         except ObjectDoesNotExist:
#             data = []
#         isDoc = True
#         return render(request, 'doctor/myPatients.html', {'data': data, 'isDoc': isDoc})
#     return render(request,'doctor/error.html')
#
# #for the doctors to add a new patient file
# def addPatientRecord(request):
#     permcheck = checkForPermission(request, "doctor.add_patientrecord")
#     if permcheck == -1:
#         return redirect('login-view')
#     if permcheck == 0:
#         return HttpResponse("<p>You do not have the permissions for this operation</p>")
#     if permcheck == 1:
#         patId = [i for i in StudentRecord.objects.all().values('person_id')]
#         return render(request, 'doctor/addNewPatient.html',{'patId':patId})
#
# #this actually inserts the patient file into the database
# def insertIntoPatientRecord(request):
#     permcheck = checkForPermission(request, "doctor.add_patientrecord")
#     if permcheck == 1 and request.method == "POST":
#         person_id = request.POST["person-id"]
#         today_date = request.POST["today-date"]
#         height = request.POST["height"]
#         weight = request.POST["weight"]
#         isDependant = request.POST["dependent"]
#         u_id = HealthCentreStaff.objects.get(user_id = getUserId(request))
#
#         obj, created = PatientRecord.objects.update_or_create(
#             doctor_id = u_id,
#             patient_id_id = person_id,
#
#             defaults={
#                 'date_created': today_date,
#                 'height': height,
#                 'weight': weight,
#                 'isDependant': isDependant
#             }
#         )
#         return redirect('display-mypatients-view')
#     return redirect(request, 'doctor/error.html')
#
# #a doctor can view the file of one patient using this. it lists all the prescriptions issued
# def displayIndividualRecord(request,patient_id):
#     permcheck = checkForPermission(request, "doctor.view_patientrecord")
#     if permcheck == 1:
#         data = PatientRecord.objects.filter(id = patient_id)
#         presData = Prescription.objects.filter(patient_record_id=patient_id).order_by("-date_of_issue")
#         ctx = {
#             'id' : patient_id,
#             'data': data,
#             'presData': presData,
#         }
#         return render(request, 'doctor/individualRecord.html', ctx)
#     return render(request, 'doctor/error.html')
#
#a doctor or a pharmacist can view a prescription of a patient and
# see the medicines that were prescribed and tests that were recommended
def displayPrescription(request):
    ctx={}
    isPharm = checkIfPharmacist(request)
    if isPharm:
        pres_id=None
        if request.GET:
            pres_id=request.GET['p_no']
        if pres_id:
            permcheck = checkForPermissions(request, "doctor.view_prescription","doctor.view_medicineissue")
            if permcheck == -1:
                return redirect('login-view')
            if permcheck == 0:
                return HttpResponse("<p>You do not have the permissions for this operation</p>")
            if permcheck == 1:
                data=Prescription.objects.filter(prescription_serial_no=pres_id)
                if data[0].patient_id != None:
                    name = data[0].patient_id
                else:
                    name = data[0].teacher_id
                p_number=data[0].prescription_serial_no
                p_number_of_doctor=data[0].prescription_no_of_doctor
                isPharm=checkIfPharmacist(request)
                meds_pres = MedicineIssue.objects.filter(prescription_serial_no=pres_id)
                ctx = {'data' : data[0],
                       'name': name,
                       'meds_pres': meds_pres,
                       'isPharm': isPharm,
                       'p_no':str(p_number)+"("+str(p_number_of_doctor)+")",
                       'doctor':data[0].doctor_id
                       }
        prescriptions = [i['prescription_serial_no'] for i in
                         Prescription.objects.all().values('prescription_serial_no').order_by('prescription_serial_no')]
        ctx['p_nos'] = prescriptions
        return render(request, 'doctor/prescription.html', context=ctx)
    return render(request, 'doctor/error.html')

# #a doctor can issue a new prescription to a patient using this
# def addPrescription(request,record_id):
#     permcheck=checkForPermission(request,'doctor.add_prescription')
#     if permcheck == -1:
#         return redirect('login-view')
#     if permcheck == 0:
#         return HttpResponse("<p>You do not have the permissions for this operation</p>")
#     if permcheck ==1:
#         ctx={
#             'record_id':record_id,
#         }
#         return render(request,'doctor/addPrescription.html',context=ctx)
#
# #this actually add the new prescription into the database
# def insertIntoPrescription(request):
#     permcheck = checkForPermission(request, 'doctor.add_prescription')
#     if permcheck==1 and request.method=='POST':
#         try:
#             id_data = Prescription.objects.all().order_by('-prescription_serial_no')[0]
#             id =  int(id_data.prescription_serial_no) + 1
#         except:
#             id = 1001
#         record_id = request.POST["rec-id"]
#         issue_date = request.POST["date-of-issue"]
#         complaint = request.POST["complaint"]
#         diagnosis = request.POST["diagnosis"]
#         med_pres = request.POST["med-pres"]
#         test_recom = 0
#         try:
#             Prescription.objects.create(
#                 prescription_serial_no =id,
#                 date_of_issue=issue_date,
#                 complaint=complaint,
#                 diagnosis=diagnosis,
#                 patient_record_id_id=record_id,
#                 medicine_prescribed=med_pres,
#                 )
#
#             if med_pres == '1':
#                 return redirect('add-medicineissue-view', id)
#             return redirect('display-individualrecord-view', record_id)
#         except IntegrityError as e:
#             return render(request, 'doctor/error.html')
#     return render(request, 'doctor/error.html')

#medicines are prescribed by a doctor to a patient using this
# def addMedicineIssue(req, presc_no):
#     permcheck = checkForPermission(req, 'doctor.add_medicineissue')
#     if permcheck == -1:
#         return redirect('login-view')
#     if permcheck == 0:
#         return HttpResponse("<p>You do not have the permissions for this operation</p>")
#     if permcheck == 1:
#         meds = [i for i in StockMedicine.objects.all().values('medicine_id', 'medicine_id__medicine_name', 'id', 'batch_no').order_by('medicine_id__medicine_name')]
#         ctx={
#             'p_no':Prescription.objects.get(prescription_serial_no=presc_no),
#             'meds':meds,
#             'type':'doctor'
#         }
#         print(ctx['p_no'])
#         return render(req,'doctor/addMedicineIssue.html',context=ctx)
#
# #this adds the prescribed medicine into the database
# def insertIntoMedicineIssue(request):
#     permcheck = checkForPermission(request, 'doctor.add_medicineissue')
#     if permcheck==1 and request.method=='POST':
#         pres_id = request.POST['presc-serial-no']
#         p=Prescription.objects.get(prescription_serial_no=pres_id)
#         if not p.medicine_prescribed:
#             p.medicine_prescribed=True
#             p.save()
#         record_id = p.patient_record_id_id
#         doi=request.POST['date-of-issue']
#         m=StockMedicine.objects.get(id=request.POST['med-id'])
#         qty=request.POST['med-qty']
#         i=request.POST['med-issued']
#         nii=request.POST['nii']
#         MedicineIssue.objects.create(prescription_serial_no=p,medicine_id=m,medicine_quantity=qty,issue_status=i,non_issue_reason=nii)
#
#         if 'submit&cont' in request.POST:
#             return redirect('add-medicineissue-view', pres_id)
#         elif 'submit' in request.POST:
#             return redirect('display-individualrecord-view', record_id)
#
#     return render(request, 'doctor/error.html')
#
# #this is used by a doctor to delete a prescribed medicine
# def deleteMedicineIssue(request,pk):
#     permcheck = checkForPermission(request, "doctor.delete_medicineissue")
#     if permcheck == 1:
#         p_no=MedicineIssue.objects.get(pk=pk).prescription_serial_no_id
#         print(p_no)
#         MedicineIssue.objects.get(pk=pk).delete()
#         return redirect(reverse('display-prescription-view', kwargs={'pres_id':p_no}))
#     return render(request, "doctor/error.html", {'msg': 'Deletion failed...you may not have the required permissions'})

#a pharmacist can issue medicines that are prescribed by a doctor using this
#this is currently not working properly as medicine_id_id returns a multivalued set
#update function updates every tuple's quantity value
def issueMedicine(request,pres_id, med_id): #med_id is the id of the entry in the medicineissue table
    if checkIfPharmacist(request):
        med_to_issue = MedicineIssue.objects.get(id = med_id)
        med_in_stock = StockMedicine.objects.get(id = med_to_issue.medicine_id_id)

        quant_req = med_to_issue.medicine_quantity
        quant_avail = med_in_stock.quantity

        if(quant_req>quant_avail):
            return render(request, "doctor/error.html", {'msg': 'Insufficient Stock!'})
        else:
            quant_avail = quant_avail - quant_req
            if(quant_avail>0):
                StockMedicine.objects.filter(id = med_to_issue.medicine_id_id).update(quantity = quant_avail)
            else:
                StockMedicine.objects.filter(id = med_to_issue.medicine_id_id).delete()
            MedicineIssue.objects.filter(id = med_id).update(issue_status = 1)
        return redirect('display-prescription-view',pres_id)
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

#display all the medicine information in the database
def displayMedicineList(request):
    permcheck = checkForPermission(request, 'doctor.view_medicine')
    if permcheck == -1:
        return redirect('login-view')
    elif permcheck == 0:
        return HttpResponse("<p>You do not have the permissions for this operation</p>")
    elif permcheck == 1:
        meds = Medicine.objects.all()
        l = []
        for i in meds:
            l.append(i)
        ctx={
            'data':l,
        }
        return render(request,'doctor/medicine.html',context=ctx)

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
        cat=request.POST["med-cat"]
        #add
        if med_id=="-1":
            Medicine.objects.create(
                medicine_name = med_name,
                manufacturing_company =company,
                category = cat
            )
        return redirect('doctor-home-view')
    return render(request, 'doctor/error.html')

def viewAllMedicinesIssued(request):
    isAdmin=request.user.is_superuser
    if isAdmin:
        allIssuedMeds=[i for i in MedicineIssue.objects.all().values('prescription_serial_no','prescription_serial_no__date_of_issue','medicine_id__bill_no','medicine_id__medicine_id__medicine_name','medicine_quantity','medicine_id__quantity').order_by('prescription_serial_no__date_of_issue')]
        print(allIssuedMeds[0])
        ctx={
            'data':allIssuedMeds
        }
        return render(request,'doctor/allIssuedMedicines.html',context=ctx)
    return HttpResponse('You need to have admin privileges for this operation')

def getReq(request):
    if request.method=='GET':
        p_id=request.GET['p_no']
        return redirect(reverse('display-prescription-view', kwargs={'pres_id':p_id}))
    return HttpResponse("Bad Request")

def confirmAdditionIntoRequisition(request):
    if request.method=='POST' and checkForPermission(request,'doctor.add_requisitionmedicine')==1:
        med_id=Medicine.objects.get(medicine_id=request.POST["med-id"])
        req_id=Requisition.objects.get(requisition_id=request.POST["req-id"])
        qty=request.POST["qty"]
        pk=request.POST['id']
        DoctorRequisitionProposal.objects.filter(pk=pk).delete()
        RequisitionMedicine.objects.create(requisition_id=req_id,medicine_id=med_id,quantity_requested=qty,quantity_received=0)
        return redirect('display-doctorrequisitionproposal-view')
    return HttpResponse("Bad Request")

def closeRequisition(request):
    isCommittee=checkIfCommitteeMember(request)
    if request.method=='POST' and isCommittee:
        req_id=request.POST["req-id-for-closing"]
        if request.POST['submit']=='Close':
            Requisition.objects.filter(requisition_id=req_id).update(closed=True)
        else:
            Requisition.objects.filter(requisition_id=req_id).update(closed=False)
        return redirect('display-requisition-view')
    return HttpResponse("You don't have the permissions for this operation")

def searchMedicine(request):
    user = request.user
    if user.is_authenticated:
        if user.has_perm("doctor.view_medicine") and user.has_perm("doctor.view_stockmedicine"):
            if request.method == "POST":
                search_text = request.POST.get('search_text', False)
                logger.error(search_text)
            else:
                search_text = ''
            medicines = Medicine.objects.filter(medicine_name__icontains=search_text)
            medicines = StockMedicine.objects.filter(medicine_id__in=medicines)
            l = []
            for i in medicines:
                d = {
                    'name': i.medicine_id,
                    'category': i.medicine_id.category,
                    'price': i.medicine_rate,
                    'quantity': i.quantity,
                    'expiry_date': i.expiry_date,
                    'manufacturing_company':i.medicine_id.manufacturing_company
                }
                l.append(d)
            ctx = {
                    'data': l
                  }
            return render(request,'doctor/medicinestock.html',context=ctx)
        else:
            return render(request,'doctor/error.html')


def newPrescription(request):
    if request.user.is_authenticated and checkIfDoctor(request):
        return render(request,'doctor/newPrescription.html')
    return render(request,'doctor/error.html',context={'msg':'You do not have permissions'})

def addNewPresc(request):
    pass
def insertIntoNewPresc(request):
    if checkForPermission(request,'doctor.add_prescription') and checkForPermission(request,'doctor.add_medicineissue'):
        try:
            date=request.POST['date-of-issue']
            type=request.POST['type_of_patient']
            patient_id=request.POST['id_of_patient']
            complaint=request.POST['complaint']
            diagnosis=request.POST['diagnosis']

            id_of_user=request.user.id
            staff_rec=HealthCentreStaff.objects.get(user_id=id_of_user)

            staff_id=staff_rec.staff_id

            presc_rec=Prescription.objects.filter(doctor_id=staff_id)
            last_presc_no=presc_rec.aggregate(Max('prescription_no_of_doctor'))
            prescription_no_of_doctor=1
            if presc_rec:
                prescription_no_of_doctor=last_presc_no[list(last_presc_no.keys())[0]]+1
            id_of_presc_added=None
            if type=='stud':
                id_of_presc_added=Prescription.objects.create(date_of_issue=date,complaint=complaint,diagnosis=diagnosis,doctor_id=staff_rec,patient_id_id=patient_id,prescription_no_of_doctor=prescription_no_of_doctor)
            elif type=='teach':
                id_of_presc_added=Prescription.objects.create(date_of_issue=date, complaint=complaint, diagnosis=diagnosis,doctor_id=staff_rec, teacher_id_id=patient_id,prescription_no_of_doctor=prescription_no_of_doctor)
            no_of_meds=request.POST['no_of_meds_in_presc']
            # print(date," ",type," ",patient_id," ",complaint," ",diagnosis," ",no_of_meds," ")
            for i in range(int(no_of_meds)):
                med=request.POST['med'+str(i+1)]
                qty=request.POST['qty'+str(i+1)]
                dose=request.POST['dose'+str(i+1)]
                # print(med,"-",qty,"-",dose)
                MedicineIssue.objects.create(medicine_id_id=med,medicine_quantity=qty,dose=dose,prescription_serial_no=id_of_presc_added)

            ctx={
                'pres_id':prescription_no_of_doctor,
                'pk_of_presc':id_of_presc_added.prescription_serial_no,
                'staff_id_of_current_user':staff_id
            }
            return render(request,'doctor/resultAfterAddingPrescription.html',context={'data':ctx})
        except:
            return HttpResponse("Error")

    return render(request,'doctor/error.html',context={'msg':'Error'})

def studTeachSelect(request):
    pat_type=request.GET['type_of_patient']
    if pat_type=='stud':
        s_ids=[i.person_id for i in StudentRecord.objects.all()]
        r_data=json.dumps(s_ids)
        return HttpResponse(r_data,content_type="application/json")
    elif pat_type=='teach':
        teach=RegularStaff.objects.all();
        r_data={ k.id:k.staff_name for k in teach}
        return HttpResponse(json.dumps(r_data), content_type="application/json")
    return HttpResponse("")

def medSelect(request):
    meds=StockMedicine.objects.all()
    l={k.id:k.medicine_id.medicine_name for k in meds}
    # print(l)
    return HttpResponse(json.dumps(l),content_type='application/json')


def viewAndEditPresc(request,presc_id):
    if request.user.is_authenticated and checkIfDoctor(request):

        prescription=Prescription.objects.get(prescription_serial_no=presc_id)

        staff_id=prescription.doctor_id_id
        staff_rec=HealthCentreStaff.objects.get(staff_id=staff_id)
        breach=(request.user.id!=staff_rec.user_id_id)
        if not breach:
            ctx={
                'presc_id':prescription.prescription_serial_no,
                'presc_id_for_doctor':prescription.prescription_no_of_doctor,
                'date':prescription.date_of_issue,
                'student_id':prescription.patient_id_id,
                'teacher_id':prescription.teacher_id_id,
                'teacher_name':prescription.teacher_id,
                'complaint':prescription.complaint,
                'diagnosis':prescription.diagnosis
            }
            meds_prescribed=MedicineIssue.objects.filter(prescription_serial_no=presc_id)
            meds_to_be_passed_in_ctx=None
            if meds_prescribed:
                meds_to_be_passed_in_ctx=[]
                k=0
                for i in meds_prescribed:
                    k=k+1
                    d={
                        'idx':k,
                        'med_id':i.medicine_id_id,
                        'med_name':i.medicine_id.medicine_id.medicine_name,
                        'med_qty':i.medicine_quantity,
                        'med_dose':i.dose
                    }
                    meds_to_be_passed_in_ctx.append(d)
            # print(meds_to_be_passed_in_ctx)
            ctx['meds']=meds_to_be_passed_in_ctx
            if meds_prescribed:
                ctx['total_meds']=len(meds_to_be_passed_in_ctx)
            else:
                ctx['total_meds']=0
            return render(request,'doctor/viewAndEditPrescription.html',context={'data':ctx})
        else:
            return render(request,'doctor/error.html',context={'msg':'You\'re trying to look into other doctor\'s info' })
    return render(request, 'doctor/error.html', context={'msg': 'You do not have permissions'})


def updatePresc(request,presc_id):
    if request.method=='POST':
        prescription=Prescription.objects.get(prescription_serial_no=presc_id)
        staff_rec=prescription.doctor_id
        uid=HealthCentreStaff.objects.get(staff_id=staff_rec.staff_id).user_id_id

        breach=not(uid==request.user.id)
        if breach:
            return render(request,'doctor/error.html',context={'msg':'You\'re trying to trespass'})

        date = request.POST['date-of-issue']
        type = request.POST['type_of_patient']
        patient_id = request.POST['id_of_patient']
        complaint = request.POST['complaint']
        diagnosis = request.POST['diagnosis']
        no_of_meds = request.POST['no_of_meds_in_presc']


        prescription.date_of_issue=date
        prescription.complaint=complaint
        prescription.diagnosis=diagnosis
        if type=='stud':
            prescription.patient_id_id=patient_id
            prescription.teacher_id=None
        elif type=='teach':
            prescription.patient_id=None
            prescription.teacher_id_id=patient_id

        prescription.save()

        MedicineIssue.objects.filter(prescription_serial_no=prescription).delete()

        for i in range(int(no_of_meds)):
            med = request.POST['med' + str(i + 1)]
            qty = request.POST['qty' + str(i + 1)]
            dose = request.POST['dose' + str(i + 1)]
            MedicineIssue.objects.create(medicine_id_id=med, medicine_quantity=qty, dose=dose,prescription_serial_no=prescription)

        ctx = {
            'pres_id': prescription.prescription_no_of_doctor,
            'pk_of_presc': prescription.prescription_serial_no,
            'staff_id_of_current_user': prescription.doctor_id_id
        }
        return render(request, 'doctor/resultAfterAddingPrescription.html', context={'data': ctx})
    return render(request,'doctor/error.html',context={'msg':'Error!!'})

def printPreview(request,presc_id):
    prescription=Prescription.objects.get(prescription_serial_no=presc_id)
    staff_rec = prescription.doctor_id
    uid = HealthCentreStaff.objects.get(staff_id=staff_rec.staff_id).user_id_id

    breach = not (uid == request.user.id)
    if breach:
        return render(request, 'doctor/error.html', context={'msg': 'You\'re trying to trespass'})
    ctx={
        'presc_id':prescription.pk,
        'date':prescription.date_of_issue,
        'complaint':prescription.complaint,
        'diagnosis':prescription.diagnosis,
        'doctor':prescription.doctor_id.staff_name,
        'doctor_presc_id':prescription.prescription_no_of_doctor
    }
    if prescription.patient_id:
        ctx['student_id']=prescription.patient_id_id
        ctx['student_name']=prescription.patient_id.name
    if prescription.teacher_id:
        ctx['teacher_name']=prescription.teacher_id.staff_name
    medicines=MedicineIssue.objects.filter(prescription_serial_no=prescription)
    med_data=None
    if medicines:
        med_data=[]
        for i in medicines:
            d={
                'med':i.medicine_id.medicine_id.medicine_name,
                'qty':i.medicine_quantity,
                'dose':i.dose
            }
            med_data.append(d)
        ctx['meds']=med_data
    return render(request,'doctor/printPreview.html',context=ctx)

def viewAllPrescs(request):
    if checkIfDoctor(request):
        uid=request.user.id
        staff_rec=HealthCentreStaff.objects.get(user_id_id=uid)
        prescriptions=Prescription.objects.filter(doctor_id=staff_rec)
        prescriptions=filterPrescs(request,prescriptions)
        data=None
        if prescriptions:
            data=[]
            for i in prescriptions:
                d={
                    'p_id':i.prescription_serial_no,
                    'p_id_doctor':i.prescription_no_of_doctor,
                    'p_date':i.date_of_issue
                }
                if i.patient_id:
                    d['patient_id']=i.patient_id.name + "\n("+i.patient_id_id+")"
                    d['patient_type']='Student'
                elif i.teacher_id:
                    d['patient_id']=i.teacher_id.staff_name
                    d['patient_type'] = 'Teacher'
                data.append(d)
        ctx={
            'data':data
        }
        return render(request,'doctor/viewAllPrescs.html',context=ctx)
    return render(request,'doctor/error.html',context={'msg': 'Only doctors have prescriptions'})

def deletePresc(request,presc_id):
    Prescription.objects.get(prescription_serial_no=presc_id).delete()
    return redirect(reverse('display-myprescs-view'))


def filterFirms(req,data_all):
    s1=req.GET.get('s1','')
    if s1!='':
        data_all=data_all.filter(firm_name__icontains=s1)
    return data_all

def filterPrescs(request,prescriptions):
    searchString=request.GET.get('search','')
    dateFrom=request.GET.get('dateFrom','')
    dateTo=request.GET.get('dateTo','')
    if(searchString!=''):
        student_ids=prescriptions.values('patient_id')
        students=StudentRecord.objects.filter(person_id__in=student_ids).filter(Q(person_id__icontains=searchString) | Q(name__icontains=searchString))
        teacher_ids=prescriptions.values('teacher_id')
        teachers=RegularStaff.objects.filter(id__in=teacher_ids).filter(Q(id__icontains=searchString) | Q(staff_name__icontains=searchString))
        prescriptions1=prescriptions.filter(patient_id_id__in=students.values('person_id'))
        prescriptions2=prescriptions.filter(teacher_id_id__in=teachers.values('id'))
        prescriptions= prescriptions1 | prescriptions2
    if(dateFrom!=''):
        prescriptions= prescriptions.filter(date_of_issue__gte= dateFrom)
    if(dateTo!=''):
        prescriptions= prescriptions.filter(date_of_issue__lte= dateTo)
    return prescriptions

