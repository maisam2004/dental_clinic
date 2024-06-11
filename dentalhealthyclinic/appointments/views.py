from django.shortcuts import render, redirect
from .models import Service,Appointment,Dentist

from .forms import AppointmentForm
from fee.models import Fee  
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages 
from django.db import transaction  

from django.contrib.auth.decorators import login_required




@login_required(login_url='/accounts/login/')
def success(request, appointment_id):
    """
    Handle successful appointments
    """
    appointment = Appointment.objects.get(id=appointment_id)
    # Send Confirmation Email
    try:
        customer_email = appointment.email
        subject = render_to_string(
            'appointments/confirmation_emails/confirmation_email_subject.txt',  # Adjust template path
            {'appointment': appointment}
        )
        body = render_to_string(
            'appointments/confirmation_emails/confirmation_email_body.txt',  # Adjust template path
            {'appointment': appointment, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [customer_email])
        messages.success(request, f'Appointment confirmed! A confirmation email has been sent to {appointment.email}.',extra_tags='bag_related=False')

    except Exception as e:  
        messages.error(request, f'There was an error sending the confirmation email: {e}')



    return render(request, 'appointments/success.html', {'appointment': appointment})



@login_required(login_url='/accounts/login/') 
def book_appointment(request):
    """
    Handles the booking of a new dental appointment.

    This view function:
    1. Renders the appointment booking form with available fees.
    2. Processes the form submission, validating the data.
    3. Assigns a random dentist who offers the selected service (if available).
    4. Checks for conflicting appointments with the chosen dentist and time.
    5. Saves the appointment if no conflicts are found.
    6. Redirects to a success page or re-renders the form with errors.

    If the user is authenticated, it also attempts to prefill the 'full_name' field from their last appointment.

    Args:
        request: The HttpRequest object representing the current request.

    Returns:
        HttpResponse: An HTTP response containing either:
            - The rendered appointment booking form (on GET request or invalid POST data).
            - A redirect to a success page (on successful appointment booking).
    """
    fees = Fee.objects.all()
    if request.method == 'POST':
        form = AppointmentForm(request.POST) 
        if form.is_valid():
            
            appointment = form.save(commit=False)
            appointment.user = request.user

                # Get selected service
            selected_fee = form.cleaned_data['service']

                # Get all dentists who offer the selected service
                #available_dentists = Dentist.objects.filter(services__service=selected_fee.service)
            available_dentists = Dentist.objects.filter(services=selected_fee)


            # If there are available dentists, randomly choose one
            if available_dentists.exists():
                appointment.dentist = random.choice(available_dentists)
            else:
                messages.error(request, "No dentists are available for this service at the moment.")
                return render(request, 'appointments/book_appointment.html', {'form': form, 'fees': fees})

            # Check for existing appointment at the same time and dentist
            try:
                existing_appointment = Appointment.objects.get(
                    dentist=appointment.dentist,
                    date=form.cleaned_data['date'],
                    time=form.cleaned_data['time']
                )
                messages.error(request, "This time slot is already booked. Please choose another time.")
                return render(request, 'appointments/book_appointment.html', {'form': form, 'fees': fees})
            except Appointment.DoesNotExist:
                pass  # No conflict, proceed with booking

            appointment.save()  
            return redirect('success', appointment_id=appointment.id)
    else:
        
        initial_data = {}
        if request.user.is_authenticated:
            

            initial_data['email'] = request.user.email
            try:
                # Get the latest appointment for the user
                #previous_appointment = Appointment.objects.filter(email=request.user.email).order_by('-date', '-time').first()
                #latest_appointment = Appointment.objects.filter(user=request.user).latest('date')  # Filter by user object
                latest_appointment = Appointment.objects.filter(user=request.user).latest('date')
                initial_data['full_name'] = latest_appointment.full_name

                # If a previous appointment exists, prefill the full name field
                
                #initial_data['full_name'] = previous_appointment.full_name
                
            except Appointment.DoesNotExist:
                initial_data['full_name'] = ""
                

        form = AppointmentForm(initial=initial_data)

    context = {'fees': fees, 'form': form}
    return render(request, 'appointments/book_appointment.html', context)

