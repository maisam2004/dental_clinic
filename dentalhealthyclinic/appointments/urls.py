
from django.urls import path,include
from . import views


urlpatterns = [
    path('book/',views.book_appointment ,name='book_appointment'),
    path('success/<int:appointment_id>/', views.success, name='success'),
]