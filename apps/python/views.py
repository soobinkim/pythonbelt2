from django.shortcuts import render, redirect
from .models import User, UserManager, TripManager, Trip
from django.db.models import Count
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "python/index.html")

def process(request):
    if request.POST['button'] == 'register':
        postData = {
        "first_name": request.POST['first_name'],
        "last_name" : request.POST['last_name'],
        "username": request.POST['username'],
        "password": request.POST['password'],
        "confirm_password":request.POST['confirm_password'],
        }
        validation = User.objects.register(postData)
        if 'theUser' in validation:
            messages.success(request, "successful registration!")
            return redirect("/")
        else:
            for message in validation['errors']:
                messages.error(request, message)
            return redirect('/')
    elif request.POST['button'] == 'login':
        postData = {
        "username" : request.POST['username'],
        "password" : request.POST['password']
        }
        validation = User.objects.login(postData)
        if 'theUser' in validation:
            request.session['user'] = validation['theUser'].id
            return redirect('/travels')
        else:
            messages.error(request, "invalid login!")
            return redirect ('/')
def logout(request):
    request.session.pop('user')
    return redirect('/')

def travel(request):
    context ={
    'user': User.objects.get(id = request.session['user']),
    'trips': Trip.objects.all()
    }
    return render(request, "python/travel.html", context)

def destination(request, id):
    thisuser = User.objects.get(id = request.session['user'])
    trip = Trip.objects.get(id = id)
    context = {
     'user': thisuser,
     'trips': trip
    }
    return render(request, "python/destination.html", context)

def join(request, id):
    thisuser = User.objects.get(id = request.session['user'])
    trip = Trip.objects.get(id = id)
    trip.joiners.add(thisuser)
    return redirect('/travels')

def add(request):
    thisuser = User.objects.get(id = request.session['user'])
    return render(request, "python/add.html")

def addplan(request):
    user = User.objects.get(id = request.session['user'])
    postData = {
        "planner" : user,
        "destination" : request.POST['destination'],
        "description" : request.POST['description'],
        "datefrom" : request.POST['datefrom'],
        "dateto" : request.POST['dateto'],
    }
    validation = Trip.objects.addtrip(postData)
    if validation == True:
        return redirect("/travels")
    else:
        for message in validation['errors']:
            messages.error(request, message)
            return redirect('/add')
