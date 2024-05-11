from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from .views import Checkout,ShippingAddressView, PaymentMethodView, OrderReviewView, OrderConfirmationView

urlpatterns = [
   path('',Checkout.as_view,name='checkout' ),
   path('shipping/', ShippingAddressView.as_view(), name='shipping_address'),
   path('payment/', PaymentMethodView.as_view(), name='payment_method'),
   path('review/', OrderReviewView.as_view(), name='order_review'),
   path('confirmation/', OrderConfirmationView.as_view(), name='order_confirmation'),
]