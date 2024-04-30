from django.shortcuts import render, redirect
from .models import Service
from .forms import AppointmentForm

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)  # Don't save immediately
            # Add any additional logic here (e.g., set patient or dentist)
            appointment.save()  # Save the appointment object to the database
            return redirect('appointments:success')  # Redirect to a success page
    else:
        services = Service.objects.all()  # Fetch available services
        form = AppointmentForm()

    context = {'services': services, 'form': form}
    return render(request, 'appointments/book_appointment.html', context)

def success(request):
    # Display a success message for booking an appointment
    return render(request, 'appointments/success.html')

