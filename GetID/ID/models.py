from django.db import models


class Student(models.Model):
    sid = models.CharField(max_length=100, primary_key=True, db_index=True, verbose_name="身份证")
    sname = models.CharField(max_length=100, db_index=True, verbose_name="姓名")
    scard = models.CharField(max_length=100, verbose_name="学号")
    shouse = models.CharField(max_length=100, blank=True, default=None)
    sroom = models.CharField(max_length=100)
    smajor = models.CharField(max_length=100, blank=True, default=None)
    sclass = models.CharField(max_length=100, blank=True, default=None)
    sbed = models.CharField(max_length=100, blank=True, default=None)


class CampusImg(models.Model):
    imgtype = models.CharField(max_length=100)
    imgurl = models.CharField(max_length=999)
