from django.contrib import messages
from django.contrib.messages import get_messages

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.user = request.user
            contact.save()
            print(contact)
            messages.success(request, 'Your message has been sent successfully!')
            form = ContactForm()
    else:
        form = ContactForm()

    context = {
        'form': form,
        'messages': get_messages(request),  # Add this line
    }
    return render(request, 'contact/contact.html', context)