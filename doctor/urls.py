from django.urls import path
from . import views
urlpatterns = [
    path('',views.indexView,name='index-view'),
    path('login',views.loginView,name='login-view'),
    path('home',views.homeView,name="doctor-home-view"),
    path('logout',views.log_out,name="logout-view"),
    path('viewStaff',views.displayHealthCenterStaff,name="display-staff-view"),
    path('viewRequisitionMedicine',views.displayRequisitionMedicine,name="display-requisitionmedicine-view"),
    path('addRequisitionMedicine',views.addRequisitionMedicine,name="add-requisitionmedicine-view"),
    path('insertrequisitionmedicine',views.insertIntoRequisitionMedicine,name="insert-into-requisitionmedicine-view")
]
