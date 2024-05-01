from django import forms
from .models import Service,Appointment
from bootstrap_datepicker_plus.widgets import DateTimePickerInput,DatePickerInput,TimePickerInput
from datetime import date

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['full_name', 'phone_number', 'email',  'dentist', 'date', 'time', 'service', 'notes']  # Adjust fields as needed
        widgets = {
            #'start_date': DateTimePickerInput(options={"format": "DD-MM-YYYY"}),
            'date': DatePickerInput(options={
                    "format": "dd-mm-yyyy",  # Format for day, month, and year
  
                }),
            'time': TimePickerInput(options={
                    "format": "mm-hh",  # Format for day, month, and year
  
                }),
        }

    # You can also define custom fields or widgets here for specific fields
    # Example:
    # date = forms.DateField(widget=forms.SelectDateWidget)
