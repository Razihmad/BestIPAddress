from os import name
from django.db import models
from datetime import date, timezone
# from django.db.models.query import ValuesQuerySet

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(default=date.today())

    def __str__(self):
        return self.name


class Bestip(models.Model):
    ip = models.CharField(max_length=30)
    city = models.CharField(max_length=200)
    login = models.CharField(max_length=100)
    session_id = models.CharField(max_length=10)
    score = models.IntegerField() 
    password = models.CharField(max_length=20)
    timezone = models.CharField(max_length=100)


    def __str__(self):
        return self.ip

class Allip(models.Model):
    ip = models.CharField(max_length=30)
    city = models.CharField(max_length=200)
    score = models.IntegerField()

    def __str__(self):
        return self.ip

        
