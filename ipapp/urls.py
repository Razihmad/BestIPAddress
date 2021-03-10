from django.contrib import admin
from django.urls import path,include
from ipapp import views

urlpatterns = [
    path('',views.home,name='home'),
    path('addcity/',views.addcity,name='addcity'),
]
