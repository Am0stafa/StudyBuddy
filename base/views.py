#! when someone goes to a specific url these are going to be functions or classes which will fire off this like queries to the database , any templates that we need to render. this is whats going to be called when someone goes to a specific url

from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# rooms = [
#     {"id": 1, "name":"lets learn python!"},
#     {"id": 2, "name":"Design with me"},
#     {"id": 3, "name":"Frontend developers"},
# ]

# Create your views here.
def home(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'base/home.html',context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, 'base/room.html',context)