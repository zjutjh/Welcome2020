from django.apps import AppConfig
from django.core.cache import cache


class IdConfig(AppConfig):
    name = 'ID'

    def ready(self):
        cache.clear()
        from .models import Student
        students = Student.objects.all()
        for stu in students:
            cache.set('GetID_' + stu.sname + stu.sid, stu)
            if stu.shouse is not None and stu.sroom is not None:
                roommates = Student.objects.filter(sroom=stu.sroom, shouse=stu.shouse)
                cache.set('GetRoom_' + stu.shouse + stu.sroom, roommates)
        print("Cache OK!")
