from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import CsvForm
import pandas as pd
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist



def form(request):
    if request.POST:
        print(request.POST)
        print(request.FILES)
        return HttpResponse("Done")
    else:
        return render(request,'form.html')
    

# def upload_excel(request):
#     if request.method == 'POST':
#         formD = CsvForm(request.POST,request.FILES)
#         if formD.is_valid():
#             csv_file = request.FILES['file']
#             df = pd.read_csv(csv_file)
#             # print(df.columns.tolist())
#             #formD.save()
#             # print(df)
#             #first_row = df.iloc[0]

#             model_fields = [field.name for field in Students._meta.get_fields() if not field.is_relation]
#             model_fields.remove('id')
#             exel_data_students = get_exel_data(df)
#             if model_fields == df.columns.to_list():
#                 Std = Students.objects.all()
#                 if not Std.exists():
#                     save_data(exel_data_students)
#                     formD.save()
#                 else:
#                     update_data(Std,exel_data_students)
#                     return HttpResponse("DATA IS ALREDY THERE")
#             else:
#                 return HttpResponse("DATA NOT MATCHED")
#         else:
#             return HttpResponse("ERROR")

#     csvfrm = CsvForm()
#     return render(request, 'upload_excel.html',{'form':csvfrm})


# def update_data(std,data):
#     for d in data:
#         print(d)

        


# def save_data(data):
#     for j in data:
#         id = j['student_id']
#         name = j['student_name']
#         email = j['student_email']
#         print(id,name,email)
#         stn = Students(student_id = id,student_name=name,student_email=email)
#         stn.save()

        
# def get_exel_data(file):
#     data = []
#     for i in range(0,file.shape[0]):
#         data.append(file.iloc[i].to_dict())

#     return data

# def get_student_model():
#     students = Students.objects.all()
#     stn_dict = {}
#     for i in students:
#         stn_dict = {
#             'student_id':i.student_id,
#             'student_email':i.student_email,
#             'student_name':i.student_name
#         }
#     return stn_dict



#update to class based views 
class ExelUploadView(View):

    def save_data(self,data):
        for j in data:
            id = j['student_id']
            name = j['student_name']
            email = j['student_email']
            print(id,name,email)
            stn = Students(student_id = id,student_name=name,student_email=email)
            stn.save()
        

    def get_students_data(self):
        data = Students.objects.all()
        if data.exists():
            stn_dict = []
            for i in data:
                temp = {
                    'student_id':i.student_id,
                    'student_email':i.student_email,
                    'student_name':i.student_name
                }
                stn_dict.append(temp)
            return stn_dict
        else:
            return []

    def get_exel_data(self,file):
        data = []
        for i in range(0,file.shape[0]):
            data.append(file.iloc[i].to_dict())
        return data

    def update_data(self,exl,data):
        if exl == data:
            print("data is up to date")
            return False
        else:
            for i in exl:
                if i not in data:
                    try:
                        by_id = Students.objects.get(student_id = i['student_id'])
                        by_id.student_name = i['student_name']
                        by_id.student_email = i['student_email']
                        by_id.save()
                    except ObjectDoesNotExist:
                        by_id = Students(student_id = i['student_id'],student_name=i['student_name'],student_email=i['student_email'])
                        by_id.save()


    def get(self,request):
        print("here")
        return render(request,"upload_excel.html",{'form':CsvForm()})
    
    def post(self,request):
        formD = CsvForm(request.POST,request.FILES)
        if formD.is_valid():
            csv_file = request.FILES['file']
            df = pd.read_csv(csv_file)
            model_fields = [field.name for field in Students._meta.get_fields() if not field.is_relation]
            model_fields.remove('id')
            if(model_fields == df.columns.tolist()):
                excel_data = self.get_exel_data(df)
                data_student = self.get_students_data()
                #print(data_student)
                if len(data_student) == 0:
                    self.save_data(excel_data)
                    return HttpResponse("INSERTING DONE")
                else:
                    update = self.update_data(excel_data,data_student)
                    if update is False:
                        return HttpResponse("DATA IS UP TO DATE")
                    
                    return HttpResponse("Updating data")
            else:
                return HttpResponse("WRONG DATA")
        return HttpResponse("DATA RECIVED")