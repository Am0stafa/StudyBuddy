from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('room/<str:pk>/',views.room, name='room'),
]