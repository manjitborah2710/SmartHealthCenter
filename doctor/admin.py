# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . models import HealthCentreStaff, MedicineIssue ,Medicine ,EmpanelledFirm, Stock, Requisition, DoctorRequisitionProposal, PatientRecord, FollowUpReport, RecommendedTest, Composition, IndividualRecord, Dependant, HealthCentreStaffContact, DisposedMedicine, Prescription, StockMedicine, StudentRecord, RequisitionMedicine
# Register your models here.

class CompositionInline(admin.TabularInline):
    model = Composition
    extra = 1


class MedicineAdmin(admin.ModelAdmin):
    fields = ['medicine_id', 'medicine_name', 'manufacturing_company','quantity', 'category']
    inlines = [CompositionInline]
    list_display = ['medicine_id', 'medicine_name', 'manufacturing_company', 'quantity', 'category']
    search_fields = ['medicine_name']


class MedicineIssueInline(admin.TabularInline):
    model = MedicineIssue
    extra = 1


class PrescriptionIssueAdmin(admin.ModelAdmin):
    inlines = [MedicineIssueInline] 
    list_display = ['prescription_serial_no', 'patient_id', 'date_of_issue', 'doctor_id']
    list_filter = ['date_of_issue']
    search_fields = ['prescription_serial_no']


class HealthCentreStaffContactInline(admin.TabularInline):
    model = HealthCentreStaffContact
    extra = 1


class HealthCentreStaffAdmin(admin.ModelAdmin):
    inlines = [HealthCentreStaffContactInline]
    list_display = ['staff_id', 'staff_name', 'staff_type', 'staff_address']
    list_filter = ['staff_type']
    search_fields = ['staff_id', 'staff_name']


class EmpanelledFirmListAdmin(admin.ModelAdmin):
    list_display = ['firm_id', 'firm_name', 'firm_email', 'firm_phone']
    search_fields = ['firm_id', 'firm_name']


class DependantAdmin(admin.ModelAdmin):
    list_display = ['name', 'person_id', 'date_of_birth', 'relation_with_person']
    list_filter = ['relation_with_person']
    search_fields = ['name']


class StockInline(admin.TabularInline):
    model = StockMedicine
    extra = 1


class StockAdmin(admin.ModelAdmin):
    list_display = ['batch_no', 'bill_no', 'firm_id', 'bill_date']
    inlines = [StockInline]
    list_filter = ['firm_id', 'bill_date']
    search_fields = ['batch_no', 'bill_no']

class DoctorRequisitionProposalInline(admin.TabularInline):
    model = DoctorRequisitionProposal
    extra = 1

class RequisitionDetailsAdmin(admin.ModelAdmin):
    inlines = [DoctorRequisitionProposalInline]
    list_display = ['requisition_id', 'date_of_order', 'amount', 'date_of_approval']
    search_fields = ['requisition_id']


class FollowUpReportInline(admin.TabularInline):
    model = FollowUpReport
    extra = 0

class RecommendedTestInline(admin.TabularInline):
    model = RecommendedTest
    extra = 0

class PatientRecordAdmin(admin.ModelAdmin):
    inlines = [RecommendedTestInline, FollowUpReportInline]
    list_display = ['patient_id', 'doctor_id', 'prescription_serial_no']
    search_fields = ['patient_id']
    list_filter = ['isDependant']


class DisposedMedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine_id', 'batch_no', 'reason', 'quantity', 'date']
    search_fields = ['medicine_id', 'batch_no']
    list_filter = ['date']

class IndividualRecordAdmin(admin.ModelAdmin):
    list_display = ['person_id', 'name', 'category', 'date_of_joining', 'date_of_leaving']
    search_fields = ['person_id', 'name']
    list_filter = ['date_of_joining', 'date_of_leaving']

# class RequisitionAdmin(admin.ModelAdmin):
#    list_display = []

admin.site.register(HealthCentreStaff, HealthCentreStaffAdmin)
admin.site.register(Medicine, MedicineAdmin)
admin.site.register(EmpanelledFirm, EmpanelledFirmListAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(PatientRecord, PatientRecordAdmin)
admin.site.register(IndividualRecord, IndividualRecordAdmin)
admin.site.register(Dependant, DependantAdmin)
admin.site.register(DisposedMedicine, DisposedMedicineAdmin)
admin.site.register(Prescription, PrescriptionIssueAdmin)
admin.site.register(Requisition, RequisitionDetailsAdmin)
admin.site.register(StudentRecord)
admin.site.register(RequisitionMedicine)
