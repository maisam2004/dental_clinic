from django.urls import path
from . import views



urlpatterns = [
    path('', views.fees_list, name='fees'),
]