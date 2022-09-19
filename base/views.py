#! when someone goes to a specific url these are going to be functions or classes which will fire off this like queries to the database , any templates that we need to render. this is whats going to be called when someone goes to a specific url

from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Room,Topic,Message,User
from .form import RoomForm

# rooms = [
#     {"id": 1, "name":"lets learn python!"},
#     {"id": 2, "name":"Design with me"},
#     {"id": 3, "name":"Frontend developers"},
# ]

# Create your views here.

def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
             messages.error(request, 'User does not exist')
        
        user = authenticate(request,username=username,password=password)#! return error or user object that matches these cred
        
        if user is not None:
            login(request, user)#! adds that session in the database along with in cookies
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
        
        
    context = {'page':page}
    return render(request, 'base/loginRegister.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = "register"
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
          user =  form.save(commit=False)
          user.username = user.username.lower()
          user.save()
          login(request, user)
          return redirect('home')
        else:
          messages.error(request, 'An error occurred during registration')
    
    context = {'page':page,"form":form}
    return render(request, 'base/loginRegister.html',context)

def home(request):
    q = request.GET.get('q') or ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    numberOfTopics = topics.count()
    topics = topics[0:5]
    roomCount = rooms.count()
    
    roomMessages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    
    context = {'rooms':rooms, 'topics':topics,"roomCount":roomCount,"roomMessages":roomMessages,"numberOfTopics":numberOfTopics}
    return render(request, 'base/home.html',context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    roomMessages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,  
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
        
    context = {'room':room , "room_messages":roomMessages,"participants":participants}
    return render(request, 'base/room.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    roomMessages = user.message_set.all()

    context = {'user':user, 'rooms':rooms,'topics':topics,"roomMessages":roomMessages}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topicName = request.POST['topic']
        topic, created = Topic.objects.get_or_create(name=topicName)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    
    context = { "form":form , 'topics': topics}
    return render(request, 'base/room_form.html',context)
 
@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')   
def deleteRoom(request,pk):
    room = Room.objects.get(pk=pk)
    context = { 'obj':room }
    
    if request.user != room.host:
        return HttpResponse('Only the host of this room can update the room!!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    return render(request, 'base/delete.html',context)
    

@login_required(login_url='login')   
def deleteMessage(request,pk):
    message = Message.objects.get(pk=pk)
    context = { 'obj':message }
    
    if request.user != message.user:
        return HttpResponse('Only the host of this room can update the room!!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=message.room.id)
        
    return render(request, 'base/delete.html',context)

def topicsPage(request):
    queriesString = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=queriesString)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()[0:20]
    return render(request, 'base/activity.html', {'room_messages': room_messages})


@login_required(login_url='login')     
def updateUser(request):
    user = request.user
    if request.method == 'POST':
        return redirect('user-profile', pk=user.id)
        
    return render(request, 'base/update-user.html', {'form': ''})
