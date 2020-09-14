from django.urls import path
from . import views

app_name = 'ID'

urlpatterns = [
    path('sid/info', views.sid_info, name='indo_sid'),
    path('dorm/info', views.dorm_info, name='info_sid'),
    path('sid/', views.index, name='index_sid'),
    path('dorm/', views.index_dorm, name='indexDorm'),
    path('imgshow/', views.img_show, name='imgshow'),
    path('', views.index, name='index'),
]
