from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Room, Message, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'welcome to Javacript'},
#     {'id': 2, 'name': 'welcome to Python'},
#     {'id': 3, 'name': 'welcome to C++'}
# ]

def login_page(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, " Username OR Password Doesn't exist.")

    return render(request, 'base/login_register.html', {'page': 'login'})

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error('An error occur during registration! ')

    return render(request, 'base/login_register.html', {'form': form})

def logoutUser(request):

    try:
        logout(request)
        messages.success(request, "Sucessfully Logout!")
    except:
        messages.error(request, 'Cannot logout!')
    
    return redirect('home')

def home(request):
    q = None
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) | 
        Q(description__icontains=q)
        )
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    topics = Topic.objects.all()

    room_count = rooms.count()

    return render(request, 'base/home.html', {
        'rooms': rooms,
        'topics': topics,
        'rooms_count': room_count,
        'room_messages': room_messages
    })
def user_profile(request, id):
    user = User.objects.get(pk=id)
    rooms = user.room_set.all()
    topic = Topic.objects.all()
    room_messages = user.message_set.all()
    context = { 'rooms': rooms, 'user': user, 'topics': topic, 'room_messages': room_messages}
    return render(request, 'base/user_profile.html', context)

def room(request,id):
    room = Room.objects.get(pk=id)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('comment')
        )
        room.participants.add(request.user)
        return redirect('room', id=room.id)

    return render(request, 'base/room.html', {"room": room, "room_messages": room_messages, 'participants': participants})


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
    return render(request, 'base/room_form.html', {'form': form})

@login_required(login_url='login')
def update_room(request, id):
    room = Room.objects.get(pk=id)
    form = RoomForm(instance=room)

    if room.host != request.user:
        return HttpResponse('Your not Allowed to here.')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/room_form.html', {'form': form })

@login_required(login_url='login')
def delete_room(request, id):
    room = Room.objects.get(pk=id)

    if room.host != request.user:
        return HttpResponse('Your not Allowed to here.')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def delete_message(request, id):
    message = Message.objects.get(pk=id)

    if message.user != request.user:
        return HttpResponse('Your not Allowed to here.')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': message})


