from django.shortcuts import render, redirect,render_to_response
from django.http import HttpResponse
import requests
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.sessions
from django import forms
from wifi import Cell, Scheme
import sys
import socket
import SocketServer
import threading
import time
from .models import Greeting

option = Cell.all('wlan0')
option1 = {}
for o in option:
    option1[o.ssid] = o.address
option2= map(lambda x : x.ssid,option)
options = set(option2)

listOfNotifis=[]

TCP_IP = '192.168.20.197'
TCP_PORT = 30
# MYHOST='192.168.18.214'
# MYPORT=40
def sendToPhoton(request):
    currentString = request.session.get('wifi')
    data1 = currentString.replace(":","")
    data = data1.decode('hex')
    message = "S" + data
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((TCP_IP,TCP_PORT))
    s.send(message)
    s.close()


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def buy(request):
    if request.method == 'POST':
        Message = 'B'
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((TCP_IP,TCP_PORT))
        s.send(Message)
        date =s.recv(1024)
        s.close()
        fail = False
        if date == 'n': #TODO INSERT DJANGO MAIL FUNCTION HERE BC BAD SHIT
            now = time.strftime("%c")
            listOfNotifis.append(now)
            print now
            sys.stdout.flush()
            fail = True
        return render(request,'buy.html',{'fail':fail})

    return render(request,'purchase.html')

def login(request): 
    return render(request, 'login.html',{'items':listOfNotifis})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
            	auth_login(request, user)
                request.session['user'] = username
                request.session['wifi'] = option1[request.POST['wifi']]
                print request.session['wifi']
                sys.stdout.flush()
                sendToPhoton(request)
            	return render(request, 'index.html')
    else:
        form = UserCreationForm()
    return render(request,'signup.html', {'form': form,'options': options})
    # return render(request, 'signup.html', {'form': form})

def profile(request): 
	return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

