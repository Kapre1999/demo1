from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import CsvForm
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
            csv_file = request.FILES['file']
            df = pd.read_csv(csv_file)
            # print(df.columns.tolist())
            #formD.save()
            # print(df)
            #first_row = df.iloc[0]

            model_fields = [field.name for field in Students._meta.get_fields() if not field.is_relation]
            model_fields.remove('id')
            if model_fields == df.columns.to_list():
                save_data(df)
                formD.save()
            else:
                return HttpResponse("DATA NOT MATCHED")
        else:
            return HttpResponse("ERROR")

    csvfrm = CsvForm()
    return render(request, 'upload_excel.html',{'form':csvfrm})



def save_data(file):
    data = []
    for i in range(0,file.shape[0]):
        data.append(file.iloc[i].to_dict())
        
    for j in data:
        id = j['student_id']
        name = j['student_name']
        email = j['student_email']
        print(id,name,email)
        stn = Students(student_id = id,student_name=name,student_email=email)
        stn.save()

        
