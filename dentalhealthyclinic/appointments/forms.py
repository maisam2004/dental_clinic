from django import forms
from .models import Service,Appointment
from bootstrap_datepicker_plus.widgets import DateTimePickerInput,DatePickerInput,TimePickerInput
from datetime import date,datetime
from datetime import date, timedelta  
import re

def is_valid_phone_number(phone_number):
    # regular expression pattern for phone numbers
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone_number))

def is_valid_full_name(full_name):
    # pattern for full names
    pattern = r'^[a-zA-Z]+(([\'\,\.\-][a-zA-Z])?[a-zA-Z]*)*$'
    return bool(re.match(pattern, full_name))

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['full_name', 'phone_number', 'email',  'dentist', 'date', 'time', 'service', 'notes']  # Adjust fields as needed
        
        def clean_full_name(self):
            full_name = self.cleaned_data['full_name']
            if not is_valid_full_name(full_name):
                raise forms.ValidationError('Please enter a valid full name')
            return full_name

        def clean_phone_number(self):
            phone_number = self.cleaned_data['phone_number']
            if not is_valid_phone_number(phone_number):
                raise forms.ValidationError('Please enter a valid phone number')
            return phone_number
        
        

        
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
