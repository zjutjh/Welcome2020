from django.urls import path
from . import views

app_name = 'ID'

urlpatterns = [
    path('sid/', views.index, name='index_sid'),
    path('dorm/', views.index_dorm, name='indexDorm'),
    path('imgShow/', views.img_show, name='imgShow'),
    path('', views.index, name='index'),
]
