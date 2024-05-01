from django.shortcuts import render, redirect
from .models import Service
from .forms import AppointmentForm

from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/') 
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST) 
        if form.is_valid():
            appointment = form.save()
            return redirect('appointments:success') 
    else:
        services = Service.objects.all() 
        form = AppointmentForm()

    context = {'services': services, 'form': form}
    return render(request, 'appointments/book_appointment.html', context)

@login_required(login_url='/accounts/login/')
def success(request):
    return render(request, 'appointments/success.html')

