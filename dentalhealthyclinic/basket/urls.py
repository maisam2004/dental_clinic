
from django.urls import path,reverse
from . import views


urlpatterns = [
    path('',views.view_basket,name='view_basket')
]