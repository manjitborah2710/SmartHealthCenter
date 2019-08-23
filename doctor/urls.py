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
    path('insertrequisition',views.insertIntoRequisition,name="insert-into-requisition-view")
]
