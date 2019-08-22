from django.shortcuts import render,redirect
from django.http import HttpResponse


from django.contrib.auth import login,logout,authenticate

# Create your views here.

def indexView(request):
    return render(request,'doctor/index.html')


def loginView(request):
    if request.method=='POST':
        user_name=request.POST['username-login']
        pwd=request.POST['pwd-login']
        user=authenticate(username=user_name,password=pwd)
        if user is not None:
            login(request,user)
            return redirect('doctor-home-view')
    user=request.user
    if not user.is_authenticated:
        return render(request,'doctor/login.html')
    return redirect('doctor-home-view')


def homeView(request):
    user=request.user
    if not user.is_authenticated:
        return redirect('login-view')
    return render(request,'doctor/home.html')

def log_out(req):
    logout(req)
    return redirect('login-view')


def displayHealthCenterStaff(req):
    pass