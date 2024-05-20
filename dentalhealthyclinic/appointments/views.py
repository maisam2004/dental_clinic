from django.shortcuts import render, redirect
from .models import Service,Appointment,Dentist
from .forms import AppointmentForm
import random
from django.contrib import messages 

from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/') 
def book_appointment(request):
    services = Service.objects.all() 
    if request.method == 'POST':
        form = AppointmentForm(request.POST) 
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user

            # Get selected service
            selected_service = form.cleaned_data['service']

            # Get all dentists who offer the selected service
            available_dentists = Dentist.objects.filter(services=selected_service)

            # If there are available dentists, randomly choose one
            if available_dentists.exists():
                appointment.dentist = random.choice(available_dentists)
            else:
                messages.error(request, "No dentists are available for this service at the moment.")
                return render(request, 'appointments/book_appointment.html', {'form': form, 'services': Service.objects.all()})

            # Check for existing appointment at the same time and dentist
            try:
                existing_appointment = Appointment.objects.get(
                    dentist=appointment.dentist,
                    date=form.cleaned_data['date'],
                    time=form.cleaned_data['time']
                )
                messages.error(request, "This time slot is already booked. Please choose another time.")
                return render(request, 'appointments/book_appointment.html', {'form': form, 'services': Service.objects.all()})
            except Appointment.DoesNotExist:
                pass  # No conflict, proceed with booking

            appointment.save()  
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



