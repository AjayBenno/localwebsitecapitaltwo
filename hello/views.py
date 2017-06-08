from django.shortcuts import render, redirect,render_to_response
from django.http import HttpResponse
import requests
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
# from django.contrib.auth.forms import UserCreationForm
from .forms import CreditCardForm, UserCreateForm
# from django.contrib.sessions
from django import forms
from wifi import Cell, Scheme
import sys
import socket
import SocketServer
import threading
import time
import json
from .models import Greeting
from django.core.mail import send_mail
from django.http import HttpResponse

option1 = {}

def getWifiAPs():
    global option1
    option = Cell.all('wlan0')
    for o in option:
        option1[o.ssid] = o.address
    option2= map(lambda x : x.ssid,option)
    options = set(option2)
    return options
listOfNotifis=[]

TCP_IP = '192.168.20.197'
TCP_PORT = 30


def sendToPhoton(request):
    currentString = request.session.get('wifi')
    data1 = currentString.replace(":","")
    data = data1.decode('hex')
    message = "S" + data
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((TCP_IP,TCP_PORT))
    s.send(message)
    s.recv(1024)
    s.close()

def sendSimpleEmail(request,emailto):
    now = time.strftime("%c")
    res = send_mail("Review Credit Card Usage", "Hi %s, There was a usage of your credit card without a connection to your phone at time %s. Please review this transaction, and if this was not your purchase, contact your credit card company to cancel the transaction." % (request.session['firstname'],now), "sealteam6capitaltwo@gmail.com", [emailto], fail_silently=False)
    return HttpResponse('%s'%res)

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html', {'title':'Capital Two'})

def creditcardform(request):
	if request.method == 'POST':
		form = CreditCardForm(request.POST)
		if form.is_valid():
			age = str(form.cleaned_data.get('age'))
			income = str(form.cleaned_data.get('income'))
			costofliving= str(form.cleaned_data.get('costofliving'))
			numberdependents = str(form.cleaned_data.get('numberdependents'))
			spending = str(form.cleaned_data.get('spending'))
			creditscore = str(form.cleaned_data.get('creditscore'))
			delinquency = str(form.cleaned_data.get('delinquency'))
			maritalstatus = str(form.cleaned_data.get('maritalstatus'))
			res = {'age': age, 'income': income, 'cost_of_living': costofliving, 'dependents': numberdependents, 'spending/month': spending, 'credit_score': creditscore, 'delinquency': delinquency, 'marital_status': maritalstatus}
			headers = {'Content-type': 'application/json'}
			r = requests.post('https://carbonserver.herokuapp.com/new_card', data=json.dumps(res), headers = headers)
			print r.text
			get = requests.get('https://carbonserver.herokuapp.com/recommended_card')
			print get.status_code
			if get.status_code == requests.codes.ok:
				res = get.json().get('recommended')
			return render(request, 'creditcard_result.html', {'recommendation': res})
	else:
		form = CreditCardForm()
		return render(request, 'creditcard_form.html', {'form': form})

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
            sendSimpleEmail(request,request.session['email'])
            sys.stdout.flush()
            fail = True
        return render(request,'buy.html',{'fail':fail, 'title':'Amazebay'})

    return render(request,'purchase.html', {'title':'Amazebay'})


def login(request):
    return render(request, 'login.html',{'items':listOfNotifis, 'title':'Login'})


def signup(request):
    global option1
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            firstname=form.cleaned_data.get('firstname')
            lastname=form.cleaned_data.get('lastname')
            email=form.cleaned_data.get('email')
            cardnumber=form.cleaned_data.get('cardnumber')
            phone=form.cleaned_data.get('phone')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
            	auth_login(request, user)
                request.session['firstname'] = firstname
                request.session['email'] = email
                request.session['wifi'] = option1[request.POST['wifi']]
                res = {'first_name':firstname,'last_name':lastname,'phone':phone,'wifi_address':option1[request.POST['wifi']],'card_number':cardnumber,'email':email}
                headers = {'Content-type': 'application/json'}
                r = requests.post('https://carbonserver.herokuapp.com/accounts', data=json.dumps(res), headers = headers)
                print r.text
                sys.stdout.flush()
                sendToPhoton(request)
            	return render(request, 'index.html')
    else:
        form = UserCreateForm()

    # options = ['banana', 'pineapple', 'cheese']
    options = getWifiAPs()
    return render(request,'signup.html', {'form': form,'options': options, 'title':'Sign Up'})
    # return render(request, 'signup.html', {'form': form})

def profile(request):
	return render(request, 'index.html', {'title':'Capital Two Profile'})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings, 'title':"DB"})
