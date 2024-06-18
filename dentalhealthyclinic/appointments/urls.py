
from django.urls import path,include
from . import views


urlpatterns = [
    path('admin/appointments/', views.list_appointments, name='admin_list_appointments'),
    path('admin/appointments/cancel/<int:appointment_id>/', views.cancel_appointment, name='admin_cancel_appointment'),
    path('book/',views.book_appointment ,name='book_appointment'),
    path('success/<int:appointment_id>/', views.success, name='success'),

]