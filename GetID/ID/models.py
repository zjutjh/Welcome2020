from django.db import models

# Create your models here.

class Student(models.Model):
    sid=models.CharField(max_length=100,primary_key=True)
    sname=models.CharField(max_length=100)
    scard=models.CharField(max_length=100)
    sroom=models.CharField(max_length=100)
    