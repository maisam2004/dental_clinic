from django.contrib import admin
from django.urls import path,include
from . import views

handler404 = views.NotFoundView.as_view() 
urlpatterns = [
    path('',views.homepage ,name='home'),
]
