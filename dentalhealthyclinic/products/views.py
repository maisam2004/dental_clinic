from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib import messages
from .models import Product,Category
from django.db.models import Q
# Create your views here.
def all_products(request):
    '''This view show all product of database'''
    products = Product.objects.all()
    query=None
    category = None
    categories=None
    if request.GET:
        if 'category' in request.GET:
            rcategories = request.GET['category'].split(',')
            products = products.filter(category__name__in = rcategories)
            categories = Category.objects.filter(name__in = rcategories)

        if 'searchbar' in request.GET:
            query = request.GET['searchbar']
            if not query:
                messages.error(request,'You did not enter valid serch')
                return redirect(reverse('products'))
            else:
                queries = Q(name__icontains=query) | Q(description__icontains=query)
                products=products.filter(queries)

    context = {
        'products':products,'search_term':query,'currnet_category':categories
    }
    return render(request,'products/products.html',context)

def product_detail(request,product_id):
    '''This show  product details of indivisual product '''
    product = get_object_or_404(Product,pk=product_id)
    context = {
        'product':product,
        

    }
    return render(request,'products/product_detail.html',context)