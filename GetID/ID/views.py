from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import redirect
from ID.forms import *
from ID.models import *
import json
import hashlib
import os

# Create your views here.

def Imgshow(request):
    type=request.GET.get('type')
    imglist=[]
    imgtype=['pf_scenery','zh_scenery','pf_canteen','zh_canteen','pf_doom','zh_doom']
    type=imgtype[int(type)-1]
    imgs=CampusImg.objects.filter(imgtype=type)
    for i in imgs:
        imglist.append(i.imgurl)
    folder=''
    context={'imglist':json.dumps(imglist),'sname':'sname'}
    return render(request,'Imgshow.html',context)

def getID(request):
    return render(request, 'getID.html')
def getDoom(request):
    return render(request, 'getDoom.html')


def indexDoom(request):
    if request.method=="POST":
        uf = getDoomForm(request.POST)
        if uf.is_valid():
            sname = uf.cleaned_data['sname']
            sid = uf.cleaned_data['sid']
            sha=hashlib.sha256()
            sha.update(sid.encode('utf8'))
            sid=sha.hexdigest()
            stu = Student.objects.filter(sname=sname, sid=sid)
            if stu:
                request.session['sname']=sname
                stu = stu[0]
                roommate=Student.objects.filter(sroom=stu.sroom)
                img_folder={'pf_scenery':'屏峰内景','zh_scenery':'朝晖内景','pf_canteen':'屏峰食堂',
                'zh_canteen':'朝晖食堂','pf_doom':'屏峰寝室','zh_doom':'朝晖寝室'}
                context = {'sname': stu.sname,'sroom':stu.sroom, 'scard': stu.scard,'roommate':roommate,'img_folder':img_folder}
                return render(request, 'getDoom.html',context)
        return render(request,'indexDoom.html')
    else:
        return render(request,'indexDoom.html')

def index(request):
    if request.method == "POST":
        uf = getIDForm(request.POST)
        message = "请检查填写的内容！"
        if uf.is_valid():
            sname = uf.cleaned_data['sname']
            sid = uf.cleaned_data['sid']
            sha=hashlib.sha256()
            sha.update(sid.encode('utf8'))
            sid=sha.hexdigest()
            stu = Student.objects.filter(sname=sname, sid=sid)
            if stu:
                request.session['sname']=sname
                stu = stu[0]
                roommate=Student.objects.filter(sroom=stu.sroom)
                img_folder={'pf_scenery':'屏峰内景','zh_scenery':'朝晖内景','pf_canteen':'屏峰食堂',
                'zh_canteen':'朝晖食堂','pf_doom':'屏峰寝室','zh_doom':'朝晖寝室'}
                img_list={}
                for k,v in img_folder.items():
                    obj=CampusImg.objects.filter(imgtype=k)
                    img_list[v]=[obj[0].imgurl,obj[1].imgurl,obj[2].imgurl,obj[3].imgurl]
                context = {'sname': stu.sname,'sroom':stu.sroom, 'scard': stu.scard,'roommate':roommate,'img_folder':img_folder,'img_list':img_list}
                return render(request, 'getID.html',context)
            else:
                message = "信息输入有误，请重新输入！"
                return render(request, 'index.html',locals())
    else:
        uf = getIDForm()
    return render(request, 'index.html',locals())



