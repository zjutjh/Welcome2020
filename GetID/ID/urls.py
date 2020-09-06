from django.urls import path
from . import views

app_name = 'ID'

urlpatterns = [
    path('getID/', views.getID, name='getID'),
    path('getDorm/', views.getDorm, name='getDorm'),
    path('indexDorm/', views.indexDorm, name='indexDorm'),
    path('imgShow/', views.imgShow, name='imgShow'),
    path('', views.index, name='index'),
]
