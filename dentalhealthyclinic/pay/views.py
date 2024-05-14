from django.shortcuts import render,redirect,reverse
from django.contrib import messages 
#from django.urls import reverse
from .forms import OrderForm
from django.conf import settings

print(settings.PUBLISHER_KEY,'hhhhhhh')


# Create your views here.
def checkout(request):
    bag = request.session.get('bag',{})

    if not bag:
        messages.error(request,'there is nonthing in basket')
        return redirect(reverse('products'))
    order_form = OrderForm()
    template = 'pay/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': settings.PUBLISHER_KEY,
        'client_secret':'your secret key',
    }

    return render(request,template,context)


