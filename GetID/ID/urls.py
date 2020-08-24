from django.urls import path
from . import views

app_name='ID'

urlpatterns=[
    path('getID/',views.getID,name='getID'),
]