
# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.UUIDField(primary_key=True, default=uuid4, editable=False) 
    full_name = models.CharField(max_length=50)  # Collect full name
    email = models.EmailField(max_length=254)   # For order confirmation
    phone_number = models.CharField(max_length=20)  # Optionally collect phone number
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ])
    payment_status = models.CharField(max_length=50, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed')
    ])
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True, blank=True)  # Link to shipping address
    product_total = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Total for products only
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total including shipping
    original_bag = models.TextField(null=True, blank=True)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)  # Default to 0 to avoid errors
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # Adjust max_digits as needed
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, editable=False) # Automatically calculated

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=80)
    address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('Stripe', 'Stripe'), 
    ])
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)


#--------
""" 
The model structure you've provided seems well-designed and comprehensive for handling the checkout process in your Django project. Here are my thoughts and suggestions:

1. **Order Model**:
   - The `Order` model looks good and covers all the necessary fields, such as the user, order number, shipping address, order status, payment status, and totals.
   - Using `UUIDField` for the order number is a good approach as it provides a unique identifier for each order.
   - Including fields for the full name, email, and phone number directly in the `Order` model is a reasonable choice, as this information is typically required for placing an order.
   - The choice fields for `status` and `payment_status` are well-defined and cover the necessary states.
   - The `original_bag` field is a good addition, as it allows you to store the original cart/bag data for reference or potential order modifications.
   - The `stripe_pid` field suggests that you plan to integrate with the Stripe payment gateway, which is a good choice.

2. **OrderItem Model**:
   - The `OrderItem` model is correctly defined to store individual line items for an order, with references to the `Order` and `Product` models.
   - The `save` method override to calculate the `lineitem_total` is a good approach, as it ensures the line item total is always up-to-date.
   - Consider adding a `created_at` or `updated_at` field to the `OrderItem` model to track when each line item was added or modified.

3. **ShippingAddress Model**:
   - The `ShippingAddress` model covers all the necessary fields for capturing shipping information.
   - Having a separate model for shipping addresses allows for better data organization and potential reuse (e.g., storing multiple shipping addresses per user).

4. **Payment Model**:
   - The `Payment` model is well-structured and includes fields for the amount, payment method, and transaction ID.
   - The `payment_date` field is a good addition, as it allows you to track when the payment was made.
   - If you plan to support multiple payment methods in the future, consider making the `payment_method` field a foreign key to a separate `PaymentMethod` model, which would make it easier to add or modify payment methods.

Overall, your model structure seems well-designed and should serve your checkout process requirements effectively. However, keep in mind that as your project evolves, you may need to make adjustments or additions to these models to accommodate new features or requirements.

Additionally, ensure that you handle data validation, access control, and security appropriately, especially when dealing with sensitive information like payment details and user data. """