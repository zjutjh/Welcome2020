from django.urls import path
from django.conf.urls import handler404,handler500
from . import views

app_name = 'ID'

handler404=views.page_not_found
handler500=views.page_error

urlpatterns = [
    path('sid/', views.index, name='index_sid'),
    path('dorm/', views.index_dorm, name='indexDorm'),
    path('Imgshow/', views.img_show, name='Imgshow'),
    path('', views.index, name='index'),
]
