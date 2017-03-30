from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import re, bcrypt
# from datetime import datetime
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$')
class UserManager(models.Manager):
    def register(self, postData):
            error_log = []
            current_date = datetime.datetime.today().strftime('%Y-%m-%d')
            if len(postData['first_name']) < 3:
                error_log.append("name must be at least 3 characters!")
            elif (postData['first_name']).isdigit():
                error_log.append("name must be alphabetical characters!")
            if len(postData['last_name']) < 3:
                error_log.append("name must be at least 3 characters!")
            elif (postData['last_name']).isdigit():
                error_log.append("name must be alphabetical characters!")
            if len(postData['username']) < 3:
                error_log.append("username must be at least 3 characters!")
            if len(postData['password']) < 8:
                error_log.append("password needs to be at least 8 characters!")
            if not postData['confirm_password'] == postData['password']:
                error_log.append("confirmation password does not match password!")
            if User.objects.filter(username = postData['username']).exists():
                error_log.append("username already exists!")
            if error_log == []:
                password = postData['password'].encode()
                password = bcrypt.hashpw(password, bcrypt.gensalt())
                user = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], username= postData['username'], password = password)
                return  {'theUser': user}
            else:
                return {'errors' : error_log}

    def login(self, postData):
        error_log = []
        if User.objects.filter(username = postData['username']).exists():
            password = postData['password'].encode('utf-8')
            stored_hashed = User.objects.get(username=postData['username']).password
            if bcrypt.hashpw(password, stored_hashed.encode()) != stored_hashed:
                error_log.append("incorrect password!")
            else:
                user = User.objects.get(username=postData['username'])
        else:
            error_log.append("username does not exist!")
        if error_log == []:
            return {"theUser": user}
        else:
            return { "errors": error_log}


class TripManager(models.Manager):
    def addtrip(self, postData):
        error_log = []
        current_date = datetime.datetime.today().strftime('%Y-%m-%d')
        if len(postData['destination']) < 1:
            error_log.append("destination must not be blank!")
        if len(postData['description']) < 1:
            error_log.append("description must not be blank!")
        if len(postData['datefrom']) < 1:
            error_log.append("Travel date from must not be blank!")
        elif postData['datefrom'] <= current_date:
            error_log.append("Are you from the futre?")
        if len(postData['dateto']) < 1:
            error_log.append("Travel date to must not be blank!")
        elif postData['dateto'] <= current_date:
            error_log.append("Travel date must be future-dated!")
        elif postData['dateto'] < postData['datefrom']:
            error_log.append("Travel date to must be after Travel date from")
        if error_log == []:
            trip = Trip.objects.create(destination = postData['destination'], description= postData['description'], datefrom = postData['datefrom'], dateto = postData['dateto'], planner = postData['planner'])
            return True
        else:
            return {"errors": error_log}

class User(models.Model):
    first_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 40)
    username = models.CharField(max_length = 45)
    password = models.CharField(max_length = 40)
    # email = models.CharField(max_length = 40)
    # birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    datefrom = models.DateField()
    dateto = models.DateField()
    planner = models.ForeignKey(User, related_name="trips")
    joiners = models.ManyToManyField(User, related_name = "plannedtrips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
