from django import forms
from .models import Service,Appointment
from bootstrap_datepicker_plus.widgets import DateTimePickerInput,DatePickerInput,TimePickerInput
from datetime import date,datetime
from datetime import date, timedelta  

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['full_name', 'phone_number', 'email',  'dentist', 'date', 'time', 'service', 'notes']  # Adjust fields as needed
        widgets = {
            
            'date': DatePickerInput(options={
                    "format": "DD-MM-yyy",  # Format for day, month, and year
                    "minDate": date.today() + timedelta(days=1),  # Key change
                    "daysOfWeekDisabled": [0, 6], 
                    }),

            'time': TimePickerInput(options={
                    "format": "HH:mm",  # Format for day, month, and year
                    "stepping": 15,
                    "enabledHours": [ 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                    
                }),
        }

    # You can also define custom fields or widgets here for specific fields
    # Example:
    # date = forms.DateField(widget=forms.SelectDateWidget)
