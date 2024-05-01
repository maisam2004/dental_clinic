from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f'{self.name}'

class Appointment(models.Model):
    full_name = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20,null=True) 
    dentist = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, related_name='appointments_as_dentist')  
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    service = models.ForeignKey('Service', on_delete=models.CASCADE,null=True)
    STATUS_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    notes = models.TextField(blank=True)
