from django.shortcuts import render
from django.views.generic import TemplateView,CreateView,FormView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.mixins import LoginRequiredMixin as AllAuthLoginRequiredMixin

from .models import ShippingAddress, Order
from .forms import ShippingAddressForm,PaymentMethodForm

# Create your views here.

class Checkout(TemplateView):
    template_name = 'checkout/checkout.html'




class ShippingAddressView(AllAuthLoginRequiredMixin, CreateView):
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'checkout/shipping_address.html'
    success_url = '/checkout/payment/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        order = Order.objects.create(
            user=self.request.user,
            # Set other order fields as needed
        )
        form.instance.order = order
        return super().form_valid(form)

class PaymentMethodView(LoginRequiredMixin, FormView):
    template_name = 'checkout/payment_method.html'
    form_class = PaymentMethodForm
    success_url = '/checkout/review/'

    def form_valid(self, form):
        # Process the payment method and save it to the order
        payment_method = form.cleaned_data['payment_method']
        order = self.request.user.order_set.last()
        order.payment_method = payment_method
        order.save()
        return super().form_valid(form)

class OrderReviewView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout/order_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.request.user.order_set.last()
        context['order'] = order
        return context
    
class OrderConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout/order_confirmation.html'

    def get(self, request, *args, **kwargs):
        order = request.user.order_set.last()
        if order.payment_status == 'Paid':
            # Process the order and update the status
            order.status = 'Processing'
            order.save()
            return super().get(request, *args, **kwargs)
        else:
            return redirect('/checkout/payment/')