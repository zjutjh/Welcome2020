import hashlib
from enum import Enum

from django.core.cache import cache
from django.db.models import Q

from .models import Student


class response_msg(Enum):
    MSG_ERROR = "请正确填写信息"
    MSG_NOT_FOUND = "没有查到你的信息"
    MSG_SYSTEM_ERROR = "系统错误请联系精弘客服"


class index_type(Enum):
    Dorm = "寝室"
    Sid = "学号"


class index_link(Enum):
    Dorm = "/dorm/info"
    Sid = "/sid/info"


img_type = ['pf_scenery', 'zh_scenery', 'pf_canteen', 'zh_canteen', 'pf_doom', 'zh_doom']
img_folder = {'pf_scenery': '屏峰风光', 'zh_scenery': '朝晖风光', 'pf_canteen': '屏峰食堂',
              'zh_canteen': '朝晖食堂', 'pf_doom': '屏峰寝室', 'zh_doom': '朝晖寝室'}


def get_student(uf):
    stu_name = uf.cleaned_data['sname']
    sid = uf.cleaned_data['sid'].upper().replace("•", "·").replace(".", "·").replace("。", "·").replace(" ", '')
    sha = hashlib.md5()
    sha.update(sid.encode('utf8'))
    sid = sha.hexdigest()

    stu_cache = cache.get('GetID_' + stu_name + sid)
    if stu_cache is None:
        stu = Student.objects.filter(sname=stu_name, sid=sid)
        if not stu:
            return None
        stu = stu[0]
        cache.set('GetID_' + stu.sname + stu.sid, stu)
    else:
        stu = stu_cache
    return stu


def get_roommates(stu):
    room_cache = cache.get('GetRoom_' + stu.shouse + stu.sroom)
    if room_cache is None:
        roommates = Student.objects.filter(sroom=stu.sroom, shouse=stu.shouse)
        cache.set('GetRoom_' + stu.shouse + stu.sroom, roommates)
    else:
        roommates = room_cache

    return roommates.filter(~Q(sid=stu.sid))
