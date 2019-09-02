from django.urls import path
from . import views
urlpatterns = [
    path('',views.indexView,name='index-view'),
    path('login',views.loginView,name='login-view'),
    path('home',views.homeView,name="doctor-home-view"),
    path('logout',views.log_out,name="logout-view"),

    path('viewStaff',views.displayHealthCenterStaff,name="display-staff-view"),
    path('addStaff',views.addHealthCenterStaff,name="add-staff-view"),
    path('editStaff/<int:pk>',views.editHealthCenterStaff,name="edit-staff-view"),
    path('deleteStaff/<int:pk>',views.deleteHealthCenterStaff,name="delete-staff-view"),
    path('insertIntoStaff',views.insertIntoHealthCenterStaff,name="insert-into-staff-view"),

    path('medicinestock',views.displayMedicine,name="display-medicine"),
    path('addStock',views.addStock,name='add-stock-view'),
    path('insertIntoStock',views.insertIntoStock,name='insert-into-stock-view'),

    path('viewRequisitionMedicine',views.displayRequisitionMedicine,name="display-requisitionmedicine-view"),
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

    path('editRequisition/<int:pk>',views.editRequistion,name="edit-requisition-view"),
    path('deleteRequiusition/<int:pk>',views.deleteRequisition,name="delete-requisition-view"),

    path('editRequisitionMedicine/<int:pk>',views.editRequisitionMedicine,name="edit-requisitionmedicine-view"),
    path('deleteRequisitionMedicine/<int:pk>',views.deleteRequisitionMedicine,name="delete-requisitionmedicine-view"),

    path('editRequisitionProposal/<int:pk>',views.editRequisitionProposal,name="edit-requisitionproposal-view"),
    path('deleteRequisition/<int:pk>',views.deleteRequisitionProposal,name="delete-requisitionproposal-view"),

    path('viewMyPatients',views.viewMyPatients,name="display-mypatients-view"),
    path('addNewPatient',views.addPatientRecord,name="add-newpatient-view"),
    path('insertNewPatient',views.insertIntoPatientRecord,name="insert-into-patientrecord-view"),
]
