from django import forms
from .models import Service,Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'  # Include all fields from the Appointment model

    # You can also define custom fields or widgets here for specific fields
    # Example:
    # date = forms.DateField(widget=forms.SelectDateWidget)
