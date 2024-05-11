from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'address2', 'town_or_city', 'county', 'postcode', 'country', 'phone_number']
        labels = {
            'address': 'Street Address',
            'address2': 'Apartment, Suite, etc. (optional)',
            'town_or_city': 'Town/City',
            'county': 'County/State (optional)',
            'postcode': 'Postal Code',
            'country': 'Country',
            'phone_number': 'Phone Number',
        }
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': '1234 Main St'}),
            'address2': forms.TextInput(attrs={'placeholder': 'Apartment, Suite, etc. (optional)'}),
            'town_or_city': forms.TextInput(attrs={'placeholder': 'Town/City'}),
            'county': forms.TextInput(attrs={'placeholder': 'County/State (optional)'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }



PAYMENT_CHOICES = [
    ('stripe', 'Stripe'),
    ('paypal', 'PayPal'),
]

class PaymentMethodForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)