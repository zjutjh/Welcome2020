from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.db.models import Q
from .forms import *
from .models import *
import json
import hashlib
from enum import Enum

imgType = ['pf_scenery', 'zh_scenery', 'pf_canteen', 'zh_canteen', 'pf_doom', 'zh_doom']
img_folder = {'pf_scenery': '屏峰内景', 'zh_scenery': '朝晖内景', 'pf_canteen': '屏峰食堂',
              'zh_canteen': '朝晖食堂', 'pf_doom': '屏峰寝室', 'zh_doom': '朝晖寝室'}


class res_msg(Enum):
    MSG_ERROR = "请正确填写信息"
    MSG_NOT_FOUND = "没有查到你的信息"


def page_not_found(request, exception=None):
    return render(request, 'index.html')


def page_error(request, exception=None):
    return render(request, 'index.html')


def img_show(request):
    img_type = request.GET.get('type')
    img_type = imgType[int(img_type) - 1]
    image_list = [i.imgurl for i in CampusImg.objects.filter(imgtype=img_type)]
    context = {'imgList': json.dumps(image_list), 'sname': 'sname'}
    return render(request, 'imgShow.html', context)


def index_dorm(request):
    if request.method != "POST":
        return render(request, 'indexDorm.html')

    uf = getDormForm(request.POST)
    if not uf.is_valid():
        return render(request, 'indexDorm.html', {"message": res_msg.MSG_ERROR.value})

    sname = uf.cleaned_data['sname']
    sid = uf.cleaned_data['sid']
    sha = hashlib.sha256()
    sha.update(sid.encode('utf8'))
    sid = sha.hexdigest()
    stu = Student.objects.filter(sname=sname, sid=sid)
    if not stu:
        return render(request, 'indexDorm.html', {"message": res_msg.MSG_NOT_FOUND.value})

    request.session['sname'] = sname
    stu = stu[0]
    roommate = Student.objects.filter(sroom=stu.sroom, shouse=stu.shouse)
    roommate = roommate.filter(~Q(sid=stu.sid))
    context = {'sname': stu.sname, 'sroom': stu.sroom, 'scard': stu.scard, 'roommate': roommate,
               'img_folder': img_folder, 'sbed': stu.sbed, 'shouse': stu.shouse}
    return render(request, 'getDorm.html', context)


def index(request):
    if request.method != "POST":
        return render(request, 'index.html', locals())

    uf = getIDForm(request.POST)

    if not uf.is_valid():
        message = res_msg.MSG_ERROR.value
        return render(request, 'index.html', locals())

    sname = uf.cleaned_data['sname']
    sid = uf.cleaned_data['sid']
    sha = hashlib.sha256()
    sha.update(sid.encode('utf8'))
    sid = sha.hexdigest()

    stu = Student.objects.filter(sname=sname, sid=sid)
    if not stu:
        message = res_msg.MSG_NOT_FOUND.value
        return render(request, 'index.html', locals())

    request.session['sname'] = sname
    stu = stu[0]
    roommate = Student.objects.filter(sroom=stu.sroom)
    img_list = {}
    for img_type, v in img_folder.items():
        obj = CampusImg.objects.filter(imgtype=img_type)
        img_list[v] = [obj[0].imgurl, obj[1].imgurl, obj[2].imgurl, obj[3].imgurl]
    context = {'sname': stu.sname, 'sroom': stu.sroom, 'scard': stu.scard, 'roommate': roommate,
               'img_folder': img_folder, 'img_list': img_list, 'sclass': stu.sclass}
    return render(request, 'getID.html', context)
