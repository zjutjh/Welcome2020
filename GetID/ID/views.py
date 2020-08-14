from django.shortcuts import render
from django.http import HttpResponse
from ID.forms import *
from ID.models import *
# Create your views here.

def getID(request):
    if request.method=="POST":
        uf=getIDForm(request.POST)
        if uf.is_valid():
            sname=uf.cleaned_data['sname']
            sid=uf.cleaned_data['sid']
            stu=Student.objects.filter(sname=sname,sid=sid)
            if stu:
                stu=stu[0]
                context={'sname':stu.sname,'scard':stu.scard}
                return render(request,'getID.html',context)
            else:
                context={'message':'找不到符合条件的信息，请检查输入哦~'}
                return render(request,'getID.html',context)
    else:
        uf=getIDForm()
        return render(request,'getID.html',{'uf':uf})

