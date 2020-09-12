import hashlib
import json
import logging
from enum import Enum

from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .forms import *
from .models import *

logger = logging.getLogger('app')

imgType = ['pf_scenery', 'zh_scenery', 'pf_canteen', 'zh_canteen', 'pf_doom', 'zh_doom']
img_folder = {'pf_scenery': '屏峰风光', 'zh_scenery': '朝晖风光', 'pf_canteen': '屏峰食堂',
              'zh_canteen': '朝晖食堂', 'pf_doom': '屏峰寝室', 'zh_doom': '朝晖寝室'}


class res_msg(Enum):
    MSG_ERROR = "请正确填写信息"
    MSG_NOT_FOUND = "没有查到你的信息",
    MSG_SYSTEM_ERROR = "系统错误请联系客服"


@cache_page(60 * 15)
def page_not_found(request, exception=None):
    return render(request, 'index.html')


@cache_page(60 * 15)
def page_error(request, exception=None):
    return render(request, 'index.html')


def img_show(request):
    img_type = request.GET.get('type')
    if not img_type.isdigit():
        message = res_msg.MSG_ERROR.value
        return render(request, 'index.html', locals())

    img_type = imgType[int(img_type) - 1]
    image_list = [i.imgurl for i in CampusImg.objects.filter(imgtype=img_type)]
    context = {'imgList': json.dumps(image_list), 'sname': 'sname'}
    return render(request, 'imgShow.html', context)


def index_dorm(request):
    print(request)
    return render(request, 'indexDorm.html')


def dorm_info(request):
    uf = getDormForm(request.POST)
    if not uf.is_valid():
        return render(request, 'indexDorm.html', {"message": res_msg.MSG_ERROR.value})

    sname = uf.cleaned_data['sname']
    sid = uf.cleaned_data['sid'].upper().replace("•", "·").replace(".", "·").replace("。", "·").replace(" ", '')
    sha = hashlib.md5()
    sha.update(sid.encode('utf8'))
    sid = sha.hexdigest()

    stu_cache = cache.get('GetID_' + sname + sid)
    if stu_cache is None:
        stu = Student.objects.filter(sname=sname, sid=sid)
        if not stu:
            return render(request, 'indexDorm.html', {"message": res_msg.MSG_NOT_FOUND.value})

        stu = stu[0]
        cache.set('GetID_' + sname + sid, stu)
    else:
        stu = stu_cache

    room_cache = cache.get('GetRoom_' + stu.shouse + stu.sroom)
    if room_cache is None:
        roommate = Student.objects.filter(sroom=stu.sroom, shouse=stu.shouse)
        cache.set('GetRoom_' + stu.shouse + stu.sroom, roommate)
    else:
        roommate = room_cache

    roommate = roommate.filter(~Q(sid=stu.sid))

    try:

        context = {'sname': stu.sname, 'sroom': stu.sroom, 'roommate': roommate,
                   'sbed': stu.sbed, 'shouse': stu.shouse, 'scampus': stu.scampus}
        return render(request, 'getDorm.html', context)

    except Exception:
        logger.error('sid:%s sname:%s 学生信息错误' % (sid, sname))
        return render(request, 'indexDorm.html', {"message": res_msg.MSG_SYSTEM_ERROR.value})


def index(request):
    return render(request, 'index.html')


def sid_info(request):
    uf = getIDForm(request.POST)
    if not uf.is_valid():
        return render(request, 'index.html', {"message": res_msg.MSG_ERROR.value})

    sname = uf.cleaned_data['sname']
    sid = uf.cleaned_data['sid'].upper().replace("•", "·").replace(".", "·").replace("。", "·").replace(" ", '')
    sha = hashlib.md5()
    sha.update(sid.encode('utf8'))
    sid = sha.hexdigest()
    stu_cache = cache.get('GetID_' + sname + sid)
    if stu_cache is None:
        stu = Student.objects.filter(sname=sname, sid=sid)
        if not stu:
            return render(request, 'index.html', {"message": res_msg.MSG_NOT_FOUND.value})

        stu = stu[0]
        cache.set('GetID_' + sname + sid, stu)
    else:
        stu = stu_cache

    try:
        context = {'sname': stu.sname, 'scard': stu.scard, 'smajor': stu.smajor,
                   'sclass': stu.sclass, 'scampus': stu.scampus}
        return render(request, 'getID.html', context)
    except Exception:
        logger.error('sid:%s sname:%s 学生信息错误' % (sid, sname))
        return render(request, 'index.html', {"message": res_msg.MSG_SYSTEM_ERROR.value})
