from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def homeHome(request):
    return HttpResponse("<h2>Hello world</h2>")