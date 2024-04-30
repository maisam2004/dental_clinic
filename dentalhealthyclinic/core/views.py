from django.shortcuts import render

# Create your views here.
def homepage(request):
    context = {}  # Add any context data needed for the homepage

    return render(request, 'core/homepage.html', context)