from django.urls import path
from . import views
from .views import ExelUploadView

urlpatterns = [
    path('',views.form),
    path('upload/',ExelUploadView.as_view())
]