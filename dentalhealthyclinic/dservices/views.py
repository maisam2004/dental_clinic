from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib import messages
from django.views.generic.base import TemplateView
# Create your views here.

class GeneralView(TemplateView):
    template_name = 'dservices/general.html'


class CosmeticView(TemplateView):
    template_name = 'dservices/cosmetic.html'


class RestoractiveView(TemplateView):
    template_name = 'dservices/restoractive.html'