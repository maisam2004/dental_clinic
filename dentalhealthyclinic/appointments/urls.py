
from django.urls import path,include
from . import views


urlpatterns = [
    path('book/',views.book_appointment ,name='book_appointment'),
]