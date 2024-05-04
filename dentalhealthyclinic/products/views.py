from django.shortcuts import render
from .models import Product
# Create your views here.
def all_products(request):
    '''This view show all product of database'''
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request,'products/products.html',context)

