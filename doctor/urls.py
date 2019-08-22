from django.urls import path
from . import views
urlpatterns = [
    path('',views.indexView,name='index-view'),
    path('login',views.loginView,name='login-view'),
    path('home',views.homeView,name="doctor-home-view"),
    path('logout',views.log_out,name="logout-view"),
    # path('viewStaff',views.)
]
