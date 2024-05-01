from django import forms
from .models import Service,Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['full_name', 'phone_number', 'email',  'dentist', 'date', 'time', 'service', 'notes']  # Adjust fields as needed


    # You can also define custom fields or widgets here for specific fields
    # Example:
    # date = forms.DateField(widget=forms.SelectDateWidget)
