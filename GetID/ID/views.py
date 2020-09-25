import hashlib
import json
import logging

from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .forms import *
from .models import *
from .utils import response_msg, index_type, index_link, get_student, img_type, get_roommates

logger = logging.getLogger('app')


@cache_page(60 * 15)
def page_error(request, exception=None):
    return render(request, 'index.html')


def index_dorm(request):
    return render(request, 'index.html', context={"title": index_type.Dorm.value, "url": index_link.Dorm.value})


def index(request):
    return render(request, 'index.html', context={"title": index_type.Sid.value, "url": index_link.Sid.value})


def img_show(request):
    img_type_index = request.GET.get('type')
    if not img_type_index.isdigit():
        context = {"message": response_msg.MSG_ERROR.value}
        return render(request, 'index.html', context)

    img_type_index = img_type[int(img_type_index) - 1]
    image_list = [i.imgurl for i in CampusImg.objects.filter(imgtype=img_type_index)]
    context = {'imgList': json.dumps(image_list), 'sname': 'sname'}
    return render(request, 'imgShow.html', context)


def dorm_info(request):
    uf = getDormForm(request.POST)
    if not uf.is_valid():
        return render(request, 'index.html', {"title": index_type.Dorm.value, "url": index_link.Dorm.value,
                                              "message": response_msg.MSG_ERROR.value})

    stu = get_student(uf)
    if stu is None:
        return render(request, 'index.html', {"title": index_type.Dorm.value, "url": index_link.Dorm.value,
                                              "message": response_msg.MSG_NOT_FOUND.value})

    roommates = get_roommates(stu)
    if roommates is None:
        context = {'sname': stu.sname, 'sroom': '无', 'roommate': None,
                   'sbed': '无', 'shouse': '无', 'scampus': stu.scampus}
        return render(request, 'getDorm.html', context)

    try:
        context = {'sname': stu.sname, 'sroom': stu.sroom, 'roommate': roommates,
                   'sbed': stu.sbed, 'shouse': stu.shouse, 'scampus': stu.scampus}
        return render(request, 'getDorm.html', context)

    except Exception:
        logger.error('sid:%s sname:%s 学生信息错误' % (stu.sid, stu.sname))
        context = {"title": index_type.Dorm.value, "url": index_link.Dorm.value,
                   "message": response_msg.MSG_SYSTEM_ERROR.value}
        return render(request, 'index.html', context)


def sid_info(request):
    uf = getIDForm(request.POST)
    if not uf.is_valid():
        context = {"message": response_msg.MSG_ERROR.value, "title": index_type.Sid.value, "url": index_link.Sid.value}
        return render(request, 'index.html', context)

    stu = get_student(uf)
    if stu is None:
        context = {"message": response_msg.MSG_NOT_FOUND.value, "title": index_type.Sid.value,
                   "url": index_link.Sid.value}
        return render(request, 'index.html', context)

    try:
        context = {'sname': stu.sname, 'scard': stu.scard, 'smajor': stu.smajor,
                   'sclass': stu.sclass, 'scampus': stu.scampus}
        return render(request, 'getID.html', context)

    except Exception:
        logger.error('sid:%s sname:%s 学生信息错误' % (stu.sid, stu.sname))
        context = {"title": index_type.Sid.value, "url": index_link.Sid.value,
                   'message': response_msg.MSG_SYSTEM_ERROR.value}
        return render(request, 'index.html', context)
