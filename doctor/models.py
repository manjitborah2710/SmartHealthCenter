  #!/usr/bin/env python3

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your models here.
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User

import datetime

MAX_ID_LENGTH = 20
MAX_LENGTH = 50


class IndividualRecord(models.Model):
    STUDENT = 'Student'
    FACULTY = 'Faculty'
    STAFF = 'Staff'
    CATEGORY_CHOICES = (
        (STUDENT, 'Student'),
        (FACULTY, 'Faculty'),
        (STAFF, 'Staff'),
    )
    person_id = models.CharField(max_length=MAX_ID_LENGTH, primary_key=True)
    name = models.CharField(max_length=MAX_LENGTH)
    category = models.CharField(
        max_length=10,
        choices = CATEGORY_CHOICES,
        default = STUDENT,
    )
    # https://docs.djangoproject.com/en/2.1/topics/auth/passwords/#module-django.contrib.auth.hashers
    password = models.CharField(max_length=MAX_ID_LENGTH)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    date_of_leaving = models.DateField(blank=True)

    def add_record(self, id,name,category,password,dob,doj,dol):
        self.person_id = id
        self.name = name
        self.category = category
        self.password = password
        self.date_of_birth = dob
        self.date_of_joining = doj
        self.date_of_leaving = dol
        self.save()

    def __str__(self):
        return self.person_id


class StudentRecord(models.Model):
    person_id = models.CharField(max_length=MAX_ID_LENGTH, primary_key=True)
    name = models.CharField(max_length=MAX_LENGTH)
    nationality = models.CharField(max_length=MAX_LENGTH)
    category = models.CharField(max_length=100)


    def __str__(self):
        return self.name

        

class HealthCentreStaff(models.Model):
    DOCTOR = 'DR'
    PHARMACIST = 'PR'
    MEDICAL_SUPERINTENDENT = 'MS'
    STAFF = 'ST'
    CATEGORY_CHOICES = (
        (DOCTOR, 'Doctor'),
        (PHARMACIST, 'Pharmacist'),
        (STAFF, 'Other staff'),
        (MEDICAL_SUPERINTENDENT, 'Medical Superintendent')
    )
    staff_id = models.CharField(max_length=MAX_LENGTH, primary_key=True)
    staff_name = models.CharField(max_length=200)
    staff_type = models.CharField( max_length=2,choices = CATEGORY_CHOICES,default = DOCTOR)
    staff_address = models.TextField()
    availability_from = models.CharField(max_length=4)
    availability_to = models.CharField(max_length=4)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE,default=6)

    def add_staff(self, staff_id, name, stype, address, a_from, a_to, user_id):
        self.staff_id = staff_id
        self.staff_name = name
        self.staff_type = stype
        self.staff_address = address
        self.availability_from = a_from
        self.availability_to = a_to
        self.user_id - user_id
        self.save()

    def __str__(self):
        return self.staff_name

class Prescription(models.Model):
    """
        Holds details about every prescription. The medicine details can be found in the MedicineIssue model
    """
    prescription_serial_no = models.CharField(max_length=MAX_LENGTH, primary_key=True)
    patient_id = models.ForeignKey(StudentRecord, db_column='person_id' , on_delete=models.CASCADE)
    date_of_issue = models.DateTimeField(auto_now_add=True)
    doctor_id = models.ForeignKey(HealthCentreStaff, db_column='staff_id', on_delete=models.CASCADE)
    issued = models.BooleanField(default=False)

    def new_prescription(self, sl_no, patient_id, date_of_issue, doctor_id):
        self.prescription_serial_no = sl_no
        self.patient_id = patient_id
        self.date_of_issue = date_of_issue
        self.doctor_id = doctor_id
        self.save()


    def __str__(self):
        return str(self.prescription_serial_no)


class Medicine(models.Model):
    SYRUP = 'Syrup'
    TABLET = 'Tablet'
    OINTMENT = 'Ointment'
    INJECTION = 'Injection'
    SOLUTION = 'Solution'
    EQUIPMENT = 'Equipment'
    DENTAL = 'Dental'
    CAPSULE = 'Capsule'
    OIL = 'Oil'
    POWDER = 'Powder'
    GARGLE = 'Gargle'
    OTHERS = 'Others'
    CATEGORY_CHOICES = (
        (SYRUP, 'Syrup'),
        (TABLET, 'Tablet'),
        (OINTMENT, 'Ointment'),
        (INJECTION, 'Injection'),
        (SOLUTION, 'Solution'),
        (EQUIPMENT, 'Equipment'),
        (DENTAL, 'Dental'),
        (CAPSULE, 'Capsule'),
        (OIL, 'Oil'),
        (POWDER, 'Powder'),
        (GARGLE, 'Gargle'),
        (OTHERS, 'Others')
    )
    medicine_id = models.CharField(max_length=MAX_ID_LENGTH,primary_key=True)
    medicine_name =  models.CharField(max_length = MAX_LENGTH)
    manufacturing_company = models.CharField(max_length = MAX_LENGTH, default='XX')
    quantity = models.IntegerField(default=0)
    category = models.CharField(
        max_length=3,
        choices=CATEGORY_CHOICES,
        default=TABLET) #syrup,tablet

    def add_new_medicine(self, medicine_id, name, company, quantity, category):
        self.medicine_id= medicine_id
        self.medicine_name= name
        self.manufacturing_company = company
        self.quantity = quantity
        self.category = category
        self.save()

    def __str__(self):
        return self.medicine_name


class MedicineIssue(models.Model):
    """
        Holds details about the medicines issued in a given prescription
    """
    prescription_serial_no = models.ForeignKey(Prescription,on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    medicine_quantity= models.IntegerField(blank=True, default=0)
    issue_status = models.BooleanField()
    non_issue_reason = models.CharField(blank=True, max_length=MAX_LENGTH)

    def add_prescribed_medicine(self, sl_no, medicine_id, medicine_quantity, issue_status, non_issue_reason, dosage):
        self.presciption_serial_no = sl_no
        self.medicine_id = medicine_id
        self.medicine_quantity = medicine_quantity
        self.issue_status = issue_status
        self.non_issue_reason = non_issue_reason
        self.save()

    def __str__(self):
        return str(self.medicine_id_id)


class EmpanelledFirm(models.Model):
    firm_id = models.CharField(max_length=MAX_ID_LENGTH,primary_key = True)
    firm_name = models.CharField(max_length=MAX_LENGTH)
    firm_email = models.EmailField(blank=True)
    firm_phone = models.CharField(max_length=10, default='0') # TODO:to be updated with PhoneNumberField

    def add_firm(self, firm_id, name, email, phone):
        self.firm_id = firm_id
        self.firm_name=name
        self.firm_email = email
        self.firm_phone = phone
        self.save()

    def __str__(self):
        return self.firm_id

class Stock(models.Model): 
    batch_no = models.CharField(max_length=MAX_LENGTH,primary_key=True)
    bill_no = models.CharField(max_length=MAX_LENGTH)
    firm_id = models.ForeignKey(EmpanelledFirm,on_delete=models.CASCADE)
    bill_date = models.DateField()
    

    def add_stock(self, batch, bill, firm, bill_date):
        self.batch_no = batch
        self.bill_no = bill
        self.firm_id = firm
        self.bill_date = bill_date
        self.save()

    def __str__(self):
        return self.batch_no


class StockMedicine(models.Model):
    batch_no = models.ForeignKey(Stock, on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    medicine_rate = models.DecimalField(max_digits=7,decimal_places=2)
    expiry_date = models.DateField()

    def add_stock_medicine(self, batch_no, medicine_id, quantity, expiry_date, rate):
        self.batch_no = batch_no
        self.medicine_id = medicine_id
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.medicine_rate = rate


    def has_expired(self):
        return timezone.now() > self.expiry_date

    
    def about_to_expire(self):
        return timezone.now() + datetime.timedelta(days=30) > self.expiry_date


    def __str__(self):
        return str(self.medicine_id)


class Requisition(models.Model):
    requisition_id = models.CharField(max_length=MAX_ID_LENGTH, primary_key=True)
    date_of_order = models.DateField()
    amount = models.DecimalField(max_digits=7,decimal_places=2)
    date_of_approval = models.DateField()
    memo = models.TextField()

    def add_requisition(self, req_id, quantity, odate, amount, adate, memo):
        self.requisition_id = req_id
        self.quantity = quantity
        self.date_of_order = odate
        self.amount = amount
        self.date_of_approval = adate
        self.memo = memo
        self.save()

    def __str__(self):
        return self.requisition_id


class DoctorRequisitionProposal(models.Model):
    requisition_id = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(HealthCentreStaff, db_column='staff_id', on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def add_requisiton_proposal(self, req_id, did, mid,qty):
        self.requisition_id = req_id
        self.doctor_id = did
        self.medicine_id = mid
        self.quantity=qty
        self.save()

    def __str__(self):
        return str(self.quantity)


class PatientRecord(models.Model):
    prescription_serial_no= models.ForeignKey(Prescription, default=None, null=True, blank=True, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(HealthCentreStaff, db_column='staff_id', on_delete=models.CASCADE)
    patient_id = models.ForeignKey(StudentRecord, db_column='person_id', on_delete=models.CASCADE,default='16-1-5-009')
    complaint = models.TextField()
    daignosis = models.TextField()
    test_result = models.TextField()
    follow_up_date = models.DateField()
    isDependant = models.BooleanField()
    testRecommended = models.BooleanField()

    def add_patient_record(self, sl, did, pid, comp, dai, test, fudate, isdependant, testrecomm):
        self.presciption_serial_no = sl
        self.doctor_id = did
        self.patient_id = pid
        self.complaint = comp
        self.daignosis = dai
        self.test_result = test
        self.follow_up_date = fudate
        self.isDependant = isdependant
        self.testRecommended = testrecomm
        self.save()

    def __str__(self):
        return self.complaint
    

class FollowUpReport(models.Model):
    patient_id = models.ForeignKey(PatientRecord, db_column='person_id', on_delete=models.CASCADE)
    follow_up_date = models.DateField()
    present = models.BooleanField()
    cured = models.BooleanField()
    furthercomments = models.TextField()

    def add_follow_up_report(self, pid, fudate, present, cured, fc):
        self.patient_id = pid
        self.follow_up_date = fudate
        self.present = present
        self.cured = cured
        self.furthercomments = fc
        self.save()

    def __str__(self):
        return self.furthercomments 


class RecommendedTest(models.Model):
    patient_id =  models.ForeignKey(PatientRecord, db_column='person_id', on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(HealthCentreStaff, db_column='staff_id', on_delete=models.CASCADE)
    test_name = models.CharField(max_length = MAX_LENGTH)

    def add_test(self, pid, did, test):
        self.patient_id = pid
        self.doctor_id = did
        self.test_name = test
        self.save()

    def __str__(self):
        return self.test_name


class Composition(models.Model):
    medicine_id = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    primary_ingredient = models.CharField(max_length = MAX_LENGTH)

    def add_composition(self, mid,ingredient):
        self.medicine_id = mid
        self.primary_ingredient = ingredient
        self.save()
    
    def __str__(self):
        return self.primary_ingredient


class Dependant(models.Model):
    person_id = models.ForeignKey(IndividualRecord, on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_LENGTH)
    date_of_birth = models.DateField()
    relation_with_person = models.CharField(max_length=MAX_ID_LENGTH)

    def add_dependant(self, dependee_id, name, dob, relation_with_person):
        self.person_id = dependee_id
        self.name = name
        self.date_of_birth = dob
        self.relation_with_person = relation_with_person
    
    def __str__(self):
        return self.name

class HealthCentreStaffContact(models.Model):
    staff_id = models.ForeignKey(HealthCentreStaff,on_delete=models.CASCADE)
    staff_phone_no = models.CharField(max_length=10)
    staff_email_id = models.EmailField(blank=True)

    def add_staff(self, staff_id, num, email):
        self.staff_id = staff_id
        self.staff_phone_no = num
        self.staff_email_id = email
        self.save()

    def __str__(self):
        return self.staff_phone_no

class DisposedMedicine(models.Model):
    medicine_id = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    batch_no = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    reason = models.TextField()
    quantity = models.IntegerField(validators = [MinValueValidator(1)])
    date = models.DateField()

    def add_disposed_medicine(self, medicine_id, batch, reason, quantity, date):
        self.medicine_id = medicine_id
        self.batch_no = batch
        self.reason = reason
        self.quantity = quantity
        self.date = date
        self.save()

    def __str__(self):
        return self.reason


class RequisitionMedicine(models.Model):
    requisition_id = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity_requested = models.IntegerField(validators = [MinValueValidator(1)])
    quantity_received = models.IntegerField(validators = [MinValueValidator(1)], blank=True)


    def add_requisition_medicine(self, requisition_id, medicine_id, quantity_requested, quantity_received):
        self.requisition_id = requisition_id
        self.medicine_id = medicine_id
        self.quantity_requested = quantity_requested
        self.quantity_received = quantity_received 
        self.save()

    def __str__(self):
        return str(self.quantity_received)

# class StaffUsernameRelationship(models.Model):
#     username=models.ForeignKey(User,to_field='username',on_delete=models.CASCADE,primary_key=True)
#     staff_id=models.ForeignKey(HealthCentreStaff,to_field='staff_id',on_delete=models.CASCADE,unique=True)

class Feedback(models.Model):
    user=models.CharField(max_length=254)
    feedback=models.TextField()

    def __str__(self):
        return str(self.feedback)