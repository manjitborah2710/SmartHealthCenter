from django.urls import path
from . import views
urlpatterns = [
    path('',views.indexView,name='index-view'),
    path('login',views.loginView,name='login-view'),
    path('home',views.homeView,name="doctor-home-view"),
    path('logout',views.log_out,name="logout-view"),
    path('viewStaff',views.displayHealthCenterStaff,name="display-staff-view"),
    path('empanelledfirms',views.displayEmpanelledFirms,name="display-empanelled-firms"),
    path('medicinestock',views.displayMedicine,name="display-medicine"),
    path('viewRequisitionMedicine',views.displayRequisitionMedicine,name="display-requisitionmedicine-view"),
    path('addRequisitionMedicine',views.addRequisitionMedicine,name="add-requisitionmedicine-view"),
    path('insertrequisitionmedicine',views.insertIntoRequisitionMedicine,name="insert-into-requisitionmedicine-view"),
    path('viewRequisition',views.displayRequisiton,name="display-requisition-view"),
    path('addRequisition',views.addRequistion,name="add-requisition-view"),
    path('insertrequisition',views.insertIntoRequisition,name="insert-into-requisition-view"),
    path('viewDoctorRequisitionProposal',views.displayRequisitionProposal,name="display-doctorrequisitionproposal-view"),
    path('addRequisitionProposal',views.addRequisitionProposal,name="add-requisitionproposal-view"),
    path('insertRequistionProposal',views.insertIntoRequisitionProposal,name="insert-into-requisitionproposal-view"),
    path('addEmpanelledFirm',views.addEmpanelledFirm,name='add-empanelledfirm-view'),
    path('insertEmpanelledFirm',views.insertIntoEmpanelledFirm,name='insert-into-empanelledfirm-view'),
    path('addStock',views.addStock,name='add-stock-view'),
    path('insertIntoStock',views.insertIntoStock,name='insert-into-stock-view')
]
