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

class StudentRecord(models.Model):
    person_id = models.CharField(max_length=MAX_ID_LENGTH, primary_key=True)
    name = models.CharField(max_length=MAX_LENGTH)
    
    def __str__(self):
        return self.name


class RegularStaff(models.Model):
    staff_name = models.CharField(max_length=MAX_LENGTH)
    staff_dept = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):
        return self.staff_name



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
    staff_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=DOCTOR)
    staff_address = models.TextField()
    availability_from = models.CharField(max_length=4)
    availability_to = models.CharField(max_length=4)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=6,unique=True)

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
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=MAX_LENGTH)
    manufacturing_company = models.CharField(max_length=MAX_LENGTH, default='XX')
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default=TABLET)  # syrup,tablet

    def add_new_medicine(self, name, company, quantity, category):
        self.medicine_name = name
        self.manufacturing_company = company
        self.category = category
        self.save()

    def __str__(self):
        return self.medicine_name


class EmpanelledFirm(models.Model):
    firm_name = models.CharField(max_length=MAX_LENGTH)
    firm_dilno = models.CharField(max_length=MAX_LENGTH, blank=True)
    firm_phone = models.CharField(max_length=10, default='0')  
    firm_gstno = models.CharField(max_length=MAX_LENGTH,blank=True)

    def add_firm(self, name, dil_no, gst_no, phone):
        self.firm_dilno = dil_no
        self.firm_name = name
        self.firm_gstno = gst_no
        self.firm_phone = phone
        self.save()

    def __str__(self):
        return self.firm_name


class Bill(models.Model):
    bill_no = models.CharField(max_length=MAX_LENGTH, primary_key=True)
    firm_id = models.ForeignKey(EmpanelledFirm, on_delete=models.CASCADE)
    bill_date = models.DateField()

    def add_stock(self, bill, firm, bill_date):
        self.bill_no = bill
        self.firm_id = firm
        self.bill_date = bill_date
        self.save()

    def __str__(self):
        return self.bill_no


class StockMedicine(models.Model):
    bill_no = models.ForeignKey(Bill, on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    medicine_rate = models.DecimalField(max_digits=7, decimal_places=2)
    expiry_date = models.DateField()

    def add_stock_medicine(self, bill_no, medicine_id, quantity, expiry_date, rate):
        self.bill_no = bill_no
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
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date_of_approval = models.DateField()
    memo = models.TextField()
    closed=models.BooleanField(default=False)

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

    def add_requisiton_proposal(self, req_id, did, mid, qty):
        self.requisition_id = req_id
        self.doctor_id = did
        self.medicine_id = mid
        self.quantity = qty
        self.save()

    def __str__(self):
        return str(self.quantity)


# class PatientRecord(models.Model):
#     doctor_id = models.ForeignKey(HealthCentreStaff, db_column='staff_id', on_delete=models.CASCADE)
#     patient_id = models.ForeignKey(StudentRecord, db_column='person_id', on_delete=models.CASCADE, default='16-1-5-009')
#     date_created = models.DateField()
#     height = models.DecimalField(max_digits=5, decimal_places=2, default=0)
#     weight = models.DecimalField(max_digits=4, decimal_places=2, default=0)
#     isDependant = models.BooleanField()
#
#     def add_patient_record(self, did, pid, dc, h, w, isdependant):
#         self.doctor_id = did
#         self.patient_id = pid
#         self.date_created = dc
#         self.height = h
#         self.weight = w
#         self.isDependant = isdependant
#         self.save()
#
#     def __str__(self):
#         return self.patient_id_id
#

class Prescription(models.Model):
    """
        Holds details about every prescription. The medicine details can be found in the MedicineIssue model
    """
    prescription_serial_no = models.AutoField(primary_key=True)
    doctor_id = models.ForeignKey(HealthCentreStaff, db_column='staff_id', on_delete=models.CASCADE)
    prescription_no_of_doctor=models.IntegerField(default=1,null=False)
    patient_id = models.ForeignKey(StudentRecord, db_column='person_id', on_delete=models.CASCADE,null=True)
    teacher_id=models.ForeignKey(RegularStaff,on_delete=models.CASCADE,null=True)
    hostel=models.CharField(max_length=100,default=None)
    date_of_issue = models.DateField()
    complaint = models.CharField(max_length=MAX_LENGTH, default="Unspecified")
    diagnosis = models.CharField(max_length=MAX_LENGTH, default="Yet to be announced")
    # followup_date = models.DateField(blank=True, default=None, null=True)
    # medicine_prescribed = models.BooleanField(default=False)
    # tests_recommended = models.BooleanField(default=False)
    class Meta:
        unique_together=(('doctor_id','prescription_no_of_doctor'))


    def new_prescription(self, sl_no, doctor_id, patient_id,teach_id,  date_of_issue, complaint, diagnosis):
        self.prescription_serial_no = sl_no
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.teacher_id = teach_id
        self.date_of_issue = date_of_issue
        self.complaint = complaint
        self.diagnosis = diagnosis
        # self.followup_date = followup_date
        # self.medicine_prescribed = meds_pres
        # self.tests_recommended = test_pres
        self.save()

    def __str__(self):
        return str(self.prescription_serial_no)


class MedicineIssue(models.Model):
    """
        Holds details about the medicines issued in a given prescription
    """
    prescription_serial_no = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(StockMedicine, on_delete=models.CASCADE)
    medicine_quantity = models.IntegerField(default=0,null=False)
    dose=models.CharField(max_length=500,null=False,default=None)
    issue_status = models.BooleanField(default=0)
    # non_issue_reason = models.CharField(blank=True, max_length=MAX_LENGTH)

    def add_prescribed_medicine(self, sl_no, medicine_id, medicine_quantity, dosage, issue_status):
        self.prescription_serial_no = sl_no
        self.medicine_id = medicine_id
        self.medicine_quantity = medicine_quantity
        self.dose=dosage
        self.issue_status = issue_status
        # self.non_issue_reason = non_issue_reason
        self.save()

    def __str__(self):
        return str(self.medicine_id_id)

class Feedback(models.Model):
    user = models.CharField(max_length=254)
    feedback = models.TextField()

    def __str__(self):
        return str(self.feedback)
