from django.shortcuts import render, redirect
from .models import Service,Appointment
from .forms import AppointmentForm

from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/') 
def book_appointment(request):
    services = Service.objects.all() 
    if request.method == 'POST':
        form = AppointmentForm(request.POST) 
        if form.is_valid():
            appointment = form.save()
            return redirect('success', appointment_id=appointment.id)
    else:
        
        initial_data = {}
        if request.user.is_authenticated:

            initial_data['email'] = request.user.email
        form = AppointmentForm(initial=initial_data)

    context = {'services': services, 'form': form}
    return render(request, 'appointments/book_appointment.html', context)

@login_required(login_url='/accounts/login/')
def success(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'appointments/success.html', {'appointment': appointment})

