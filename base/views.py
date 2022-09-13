#! when someone goes to a specific url these are going to be functions or classes which will fire off this like queries to the database , any templates that we need to render. this is whats going to be called when someone goes to a specific url

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room,Topic
from .form import RoomForm

# rooms = [
#     {"id": 1, "name":"lets learn python!"},
#     {"id": 2, "name":"Design with me"},
#     {"id": 3, "name":"Frontend developers"},
# ]

# Create your views here.
def home(request):
    q = request.GET.get('q') or ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |   
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    roomCount = rooms.count()
    context = {'rooms':rooms, 'topics':topics,"roomCount":roomCount}
    return render(request, 'base/home.html',context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, 'base/room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    
    context = { "form":form }
    return render(request, 'base/room_form.html',context)
    
def updateRoom(request,pk):
    room = Room.objects.get(pk=pk)
    form = RoomForm(instance=room)
    
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        
        if form.is_valid():
            form.save()
            return redirect('home')
    
    
    context = { "form":form }
    return render(request, 'base/room_form.html',context)
    
def deleteRoom(request,pk):
    room = Room.objects.get(pk=pk)
    context = { 'obj':room }
    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    return render(request, 'base/delete.html',context)