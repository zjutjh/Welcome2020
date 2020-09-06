from django.urls import path
from . import views

app_name='ID'

urlpatterns=[
    path('getID/',views.getID,name='getID'),
    path('getDoom/',views.getDoom,name='getDoom'),
    path('indexDoom/',views.indexDoom,name='indexDoom'),
    path('index/',views.index,name='index'),
    path('Imgshow/',views.Imgshow,name='Imgshow'),
]
