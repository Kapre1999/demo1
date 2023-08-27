from django.db import models
from datetime import datetime
# Create your models here.

class Students(models.Model):
    student_id = models.IntegerField(unique=True)
    student_name = models.CharField(max_length=200)
    student_email = models.EmailField(unique=False)

    def __str__(self):
        return self.student_name


class FileExel(models.Model):
    file = models.FileField(upload_to='exel_data')
    uploaded = models.DateField(default=datetime.today)

    