# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from . models import *
# Register your models here.

@admin.register(Medicine)
class MedicineAdmin(ImportExportModelAdmin):
    fields = ['medicine_name', 'manufacturing_company', 'category']
    list_display = ['medicine_name', 'manufacturing_company', 'category']
    search_fields = ['medicine_name']


class MedicineIssueInline(admin.TabularInline):
    model = MedicineIssue
    extra = 1

@admin.register(Prescription)
class PrescriptionIssueAdmin(ImportExportModelAdmin):
    inlines = [MedicineIssueInline]
    list_display = ['prescription_serial_no', 'patient_id', 'doctor_id', 'date_of_issue']
    list_filter = ['date_of_issue']
    search_fields = ['prescription_serial_no']

@admin.register(HealthCentreStaff)
class HealthCentreStaffAdmin(ImportExportModelAdmin):
    list_display = ['staff_id', 'staff_name', 'staff_type', 'staff_address']
    list_filter = ['staff_type']
    search_fields = ['staff_id', 'staff_name']

@admin.register(EmpanelledFirm)
class EmpanelledFirmListAdmin(ImportExportModelAdmin):
    list_display = ['firm_name', 'firm_dilno', 'firm_gstno', 'firm_phone']
    search_fields = ['firm_gstno', 'firm_name']


class DependantAdmin(admin.ModelAdmin):
    list_display = ['name', 'person_id', 'date_of_birth', 'relation_with_person']
    list_filter = ['relation_with_person']
    search_fields = ['name']


class StockInline(admin.TabularInline):
    model = StockMedicine
    extra = 1

@admin.register(Bill)
class BillAdmin(ImportExportModelAdmin):
    list_display = ['bill_no', 'firm_id', 'bill_date']
    inlines = [StockInline]
    list_filter = ['firm_id', 'bill_date']
    search_fields = ['bill_date', 'bill_no']

class DoctorRequisitionProposalInline(admin.TabularInline):
    model = DoctorRequisitionProposal
    extra = 1

@admin.register(Requisition)
class RequisitionDetailsAdmin(ImportExportModelAdmin):
    inlines = [DoctorRequisitionProposalInline]
    list_display = ['requisition_id', 'date_of_order', 'amount', 'date_of_approval']
    search_fields = ['requisition_id']



# admin.site.register(HealthCentreStaff, HealthCentreStaffAdmin)
# admin.site.register(Medicine, MedicineAdmin)
#admin.site.register(EmpanelledFirm, EmpanelledFirmListAdmin)
# admin.site.register(Bill, BillAdmin)
# admin.site.register(PatientRecord, PatientRecordAdmin)
#admin.site.register(Dependant, DependantAdmin)
# admin.site.register(DisposedMedicine, DisposedMedicineAdmin)
# admin.site.register(Prescription, PrescriptionIssueAdmin)
# admin.site.register(Requisition, RequisitionDetailsAdmin)

# admin.site.register(StudentRecord)

# class StudentRecordInline(admin.TabularInline):
#     model = StudentRecord
#     extra = 0

@admin.register(StudentRecord)
class StudentRecordAdmin(ImportExportModelAdmin):
    list_display = ['person_id','name']
    search_fields = ['person_id','name']


# admin.site.register(RequisitionMedicine)
# admin.site.register(DoctorRequisitionProposal)
admin.site.register(Feedback)
admin.site.register(StockMedicine)
admin.site.register(RegularStaff)
