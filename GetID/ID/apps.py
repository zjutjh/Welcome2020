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

        print("Cache OK!")
