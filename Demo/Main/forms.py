from django import forms
from .models import FileExel

class CsvForm(forms.ModelForm):
    class Meta:
        model = FileExel
        fields = ('file',)