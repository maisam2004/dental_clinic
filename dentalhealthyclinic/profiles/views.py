from django.shortcuts import render,get_object_or_404
from .models import User,UserProfile
from appointments.models import Appointment
from .forms import UserProfileForm
from django.contrib import messages 
from pay.models import Order
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile,user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request,'Update failed, Please ensure the form is valid.')
    else:

        form = UserProfileForm(instance = profile)
    orders = profile.orders.all()
    appointments = Appointment.objects.filter(email=request.user.email)  # Assuming the Appointment model has an 'email' field
 





    template = 'profiles/profile.html'
    context = {
        'on_profile_page':profile,
        'form':form,
        'orders':orders,
        'user': request.user,  # user object in the context
        'appointments': appointments, 

        }
    
    return render(request, template, context)



@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'pay/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)