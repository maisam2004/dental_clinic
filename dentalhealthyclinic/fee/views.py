from django.shortcuts import render
from fee.models import Fee, Category
from appointments.models import Service 
# Create your views here.

def fees_list(request):
    """Show list of fees and services from models"""
    fees = Fee.objects.select_related('service').all()
    services = Service.objects.all()
    context = {
        'fees': fees,
        'services': services,
    }
    return render(request, 'fee/fees_list.html', context)