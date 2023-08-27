from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import CsvForm

# Create your views here.
from .models import *
import pandas as pd

def form(request):
    if request.POST:
        print(request.POST)
        print(request.FILES)
        return HttpResponse("Done")
    else:
        return render(request,'form.html')
    

def upload_excel(request):
    if request.method == 'POST':
        formD = CsvForm(request.POST,request.FILES)
        if formD.is_valid():
            formD.save()
        else:
            return HttpResponse("ERROR")

    csvfrm = CsvForm()
    return render(request, 'upload_excel.html',{'form':csvfrm})
