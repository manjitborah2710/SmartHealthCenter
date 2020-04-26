from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.indexView,name='index-view'),
    path('login',views.loginView,name='login-view'),
    path('home',views.homeView,name="doctor-home-view"),
    path('logout',views.log_out,name="logout-view"),
    path('dash',views.dashHome,name='dash'),
    path('dashcontent',views.dashContent,name='dash-content'),

    path('viewStaff',views.displayHealthCenterStaff,name="display-staff-view"),
    path('addStaff',views.addHealthCenterStaff,name="add-staff-view"),

    path('editStaff/<int:pk>',views.editHealthCenterStaff,name="edit-staff-view"),
    path('deleteStaff/<int:pk>',views.deleteHealthCenterStaff,name="delete-staff-view"),
    path('insertIntoStaff',views.insertIntoHealthCenterStaff,name="insert-into-staff-view"),

    path('medicinestock',views.displayMedicine,name="display-medicine"),
    path('addBill',views.addBill,name='add-bill-view'),
    path('insertBill',views.insertBill,name='insert-into-bill-view'),

    path('viewRequisitionMedicine/<str:pk>',views.displayRequisitionMedicine,name="display-requisitionmedicine-view"),
    path('addRequisitionMedicine',views.addRequisitionMedicine,name="add-requisitionmedicine-view"),
    path('insertrequisitionmedicine',views.insertIntoRequisitionMedicine,name="insert-into-requisitionmedicine-view"),

    path('viewRequisition',views.displayRequisiton,name="display-requisition-view"),
    path('addRequisition',views.addRequistion,name="add-requisition-view"),
    path('insertrequisition',views.insertIntoRequisition,name="insert-into-requisition-view"),

    path('empanelledfirms',views.displayEmpanelledFirms,name="display-firm-view"),
    path('editfirm/<int:pk>',views.editFirm,name="edit-firm-view"),
    path('deletefirm/<int:pk>',views.deleteFirm,name="delete-firm-view"),
    path('addFirm',views.addFirm,name="add-firm-view"),
    path('insertfirm',views.insertIntoFirm,name="insert-into-firm-view"),

    path('viewDoctorRequisitionProposal',views.displayRequisitionProposal,name="display-doctorrequisitionproposal-view"),
    path('addRequisitionProposal',views.addRequisitionProposal,name="add-requisitionproposal-view"),
    path('insertRequistionProposal',views.insertIntoRequisitionProposal,name="insert-into-requisitionproposal-view"),
    
    path('addStockMedicine',views.addStockMedicine,name='add-stockmedicine-view'),
    path('insertIntoStockMedicine',views.insertIntoStockMedicine,name='insert-into-stockmedicine-view'),

    path('editRequisition/<str:pk>',views.editRequistion,name="edit-requisition-view"),
    path('deleteRequiusition/<str:pk>',views.deleteRequisition,name="delete-requisition-view"),

    path('editRequisitionMedicine/<int:pk>',views.editRequisitionMedicine,name="edit-requisitionmedicine-view"),
    path('deleteRequisitionMedicine/<int:pk>',views.deleteRequisitionMedicine,name="delete-requisitionmedicine-view"),

    path('editRequisitionProposal/<int:pk>/<int:user_id>',views.editRequisitionProposal,name="edit-requisitionproposal-view"),
    path('deleteRequisition/<int:pk>/<int:user_id>',views.deleteRequisitionProposal,name="delete-requisitionproposal-view"),

    # path('viewMyPatients',views.viewMyPatients,name="display-mypatients-view"),
    # path('addNewPatient',views.addPatientRecord,name="add-newpatient-view"),
    # path('insertNewPatient',views.insertIntoPatientRecord,name="insert-into-patientrecord-view"),

    path('viewPrescription',views.displayPrescription,name="display-prescription-view"),
    # path('addPrescription/<str:record_id>',views.addPrescription,name="add-prescription-view"),
    # path('insertPrescription',views.insertIntoPrescription,name="insert-into-prescription-view"),

    # path('individualRecord/<str:patient_id>', views.displayIndividualRecord, name="display-individualrecord-view"),

    # path('addMedicineIssue/<str:presc_no>',views.addMedicineIssue,name='add-medicineissue-view'),
    # path('insertMedicineIssue',views.insertIntoMedicineIssue,name='insert-into-medicineissue-view'),
    # path('deleteMedicineIssue/<int:pk>',views.deleteMedicineIssue,name='delete-medicineissue-view'),

    path('issueMedicine/<str:pres_id>/<str:med_id>', views.issueMedicine,name='issue-medicine-view'),

    path('submitfeedback',views.submitFeedback,name='submit-feedback'),

    path('addMedicine',views.addMedicine,name='add-medicine-view'),
    path('insertMedicine',views.insertIntoMedicine,name='insert-into-medicine-view'),
    path('medicinelist',views.displayMedicineList,name='display-medicinelist-view'),

    path('viewAllMedicinesIssued',views.viewAllMedicinesIssued,name='display-allmedicinesissued-view'),

    path('getReq',views.getReq,name='get-req'),
    path('confirm',views.confirmAdditionIntoRequisition,name='confirm-addition-into-requisition'),
    path('closeReq',views.closeRequisition,name='close-req'),

    path('search',views.searchMedicine, name='search-med'),

    path('newPrescription',views.newPrescription,name='new-presc'),
    path('addNewPresc',views.addNewPresc,name='add-newpresc-view'),
    path('insertNewpresc',views.insertIntoNewPresc,name='insert-into-newpresc-view'),
    path('selectBetweenStudentAndTeacher',views.studTeachSelect,name='stud-teach-select'),
    path('medSelect',views.medSelect,name='med-select'),
    path('viewAndEditPresc/<int:presc_id>',views.viewAndEditPresc,name='display-and-edit-presc-view'),
    path('updatePresc/<int:presc_id>',views.updatePresc,name='update-presc-view'),
    path('printPreview/<int:presc_id>',views.printPreview,name='print-preview'),
    path('viewMyPrescs',views.viewAllPrescs,name='display-myprescs-view'),
    path('deletePresc/<int:presc_id>',views.deletePresc,name='delete-presc'),

    path('preddata/',views.predData,name='prepare-predictiondata-view'),

]
