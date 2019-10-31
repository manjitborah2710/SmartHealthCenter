# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from . models import HealthCentreStaff, MedicineIssue ,Medicine ,EmpanelledFirm, Stock, Requisition, DoctorRequisitionProposal, PatientRecord, FollowUpReport, RecommendedTest, Composition, IndividualRecord, Dependant, HealthCentreStaffContact, DisposedMedicine, Prescription, StockMedicine, StudentRecord, RequisitionMedicine, Feedback
# Register your models here.

class CompositionInline(admin.TabularInline):
    model = Composition
    extra = 1

@admin.register(Medicine)
class MedicineAdmin(ImportExportModelAdmin):
    fields = ['medicine_id', 'medicine_name', 'manufacturing_company','quantity', 'category']
    inlines = [CompositionInline]
    list_display = ['medicine_id', 'medicine_name', 'manufacturing_company', 'quantity', 'category']
    search_fields = ['medicine_name']


class MedicineIssueInline(admin.TabularInline):
    model = MedicineIssue
    extra = 1

@admin.register(Prescription)
class PrescriptionIssueAdmin(ImportExportModelAdmin):
    inlines = [MedicineIssueInline]
    list_display = ['prescription_serial_no', 'patient_record_id', 'date_of_issue']
    list_filter = ['date_of_issue']
    search_fields = ['prescription_serial_no']


class HealthCentreStaffContactInline(admin.TabularInline):
    model = HealthCentreStaffContact
    extra = 1

@admin.register(HealthCentreStaff)
class HealthCentreStaffAdmin(ImportExportModelAdmin):
    inlines = [HealthCentreStaffContactInline]
    list_display = ['staff_id', 'staff_name', 'staff_type', 'staff_address']
    list_filter = ['staff_type']
    search_fields = ['staff_id', 'staff_name']

@admin.register(EmpanelledFirm)
class EmpanelledFirmListAdmin(ImportExportModelAdmin):
    list_display = ['firm_id', 'firm_name', 'firm_email', 'firm_phone']
    search_fields = ['firm_id', 'firm_name']


class DependantAdmin(admin.ModelAdmin):
    list_display = ['name', 'person_id', 'date_of_birth', 'relation_with_person']
    list_filter = ['relation_with_person']
    search_fields = ['name']


class StockInline(admin.TabularInline):
    model = StockMedicine
    extra = 1

@admin.register(Stock)
class StockAdmin(ImportExportModelAdmin):
    list_display = ['batch_no', 'bill_no', 'firm_id', 'bill_date']
    inlines = [StockInline]
    list_filter = ['firm_id', 'bill_date']
    search_fields = ['batch_no', 'bill_no']

class DoctorRequisitionProposalInline(admin.TabularInline):
    model = DoctorRequisitionProposal
    extra = 1

@admin.register(Requisition)
class RequisitionDetailsAdmin(ImportExportModelAdmin):
    inlines = [DoctorRequisitionProposalInline]
    list_display = ['requisition_id', 'date_of_order', 'amount', 'date_of_approval']
    search_fields = ['requisition_id']


class FollowUpReportInline(admin.TabularInline):
    model = FollowUpReport
    extra = 0

class RecommendedTestInline(admin.TabularInline):
    model = RecommendedTest
    extra = 0

@admin.register(PatientRecord)
class PatientRecordAdmin(ImportExportModelAdmin):
    inlines = [RecommendedTestInline, FollowUpReportInline]
    list_display = ['patient_id', 'doctor_id']
    search_fields = ['patient_id']
    list_filter = ['isDependant']

@admin.register(DisposedMedicine)
class DisposedMedicineAdmin(ImportExportModelAdmin):
    list_display = ['medicine_id', 'batch_no', 'reason', 'quantity', 'date']
    search_fields = ['medicine_id', 'batch_no']
    list_filter = ['date']

class IndividualRecordAdmin(admin.ModelAdmin):
    list_display = ['person_id', 'name', 'category', 'date_of_joining', 'date_of_leaving']
    search_fields = ['person_id', 'name']
    list_filter = ['date_of_joining', 'date_of_leaving']

# class RequisitionAdmin(admin.ModelAdmin):
#    list_display = []

# admin.site.register(HealthCentreStaff, HealthCentreStaffAdmin)
# admin.site.register(Medicine, MedicineAdmin)
#admin.site.register(EmpanelledFirm, EmpanelledFirmListAdmin)
# admin.site.register(Stock, StockAdmin)
# admin.site.register(PatientRecord, PatientRecordAdmin)
# admin.site.register(IndividualRecord, IndividualRecordAdmin)
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
@admin.register(RequisitionMedicine)
class RequisitionMedicineAdmin(ImportExportModelAdmin):
    list_display = ['medicine_id_id','medicine_id']

@admin.register(DoctorRequisitionProposal)
class DoctorRequisitionProposalAdmin(ImportExportModelAdmin):
    pass
# admin.site.register(DoctorRequisitionProposal)
admin.site.register(Feedback)
