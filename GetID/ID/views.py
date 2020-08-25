from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from ID.forms import *
from ID.models import *
import hashlib

# Create your views here.

def getID(request):
    if request.method == "POST":
        uf = getIDForm(request.POST)
        message = "请检查填写的内容！"
        if uf.is_valid():
            sname = uf.cleaned_data['sname']
            sid = uf.cleaned_data['sid']
            sid = hashlib.sha256(sid.encode("utf-8")).hexdigest()
            print(sname,"****",sid)
            stu = Student.objects.filter(sname=sname, sid=sid)
            if stu:
                stu = stu[0]
                context = {'sname': stu.sname,'sroom':stu.sroom, 'scard': stu.scard}
                return render(request, 'getID.html',context)
            else:
                message = "信息输入有误，请重新输入！"
                return render(request, 'getID.html',locals())
    else:
        uf = getIDForm()
    return render(request, 'getID.html',locals())



