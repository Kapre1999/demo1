from django.urls import path
from . import views

urlpatterns = [
    path('',views.form),
    path('upload/', views.upload_excel, name='upload_excel'),
]