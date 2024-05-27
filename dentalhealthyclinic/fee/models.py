from django.db import models

# Create your models here.
# fees/models.py
from django.db import models
from appointments.models import Service

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Fee(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='fees')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fees')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.service.name} - {self.description}"