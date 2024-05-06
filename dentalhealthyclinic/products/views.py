from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib import messages
from .models import Product,Category
from django.db.models import Q
from django.db.models.functions import Lower 
# Create your views here.
def all_products(request):
    '''This view show all product of database,add order by  sort by and searching products  '''
    products = Product.objects.all()
    query=None
    category = None
    categories=None
    sort_by = request.GET.get('sort_by', 'default')
    if request.GET:
        if 'category' in request.GET: #check if there are category word in request
            rcategories = request.GET['category'].split(',')
            products = products.filter(category__name__in = rcategories)#filter by using categroy model name field
            categories = Category.objects.filter(name__in = rcategories)#find the categories name to show in context as current_category

        if 'searchbar' in request.GET:  #check if there are searchbar word in request
            query = request.GET['searchbar']
            if not query:
                messages.error(request,'You did not enter valid serch')
                return redirect(reverse('products'))
            else:
                queries = Q(name__icontains=query) | Q(description__icontains=query)
                products=products.filter(queries)

        sort_mapping = {
                'default': 'pk',  # Default could be by primary key or any other field
                'name_asc': Lower('name'),
                'name_desc': Lower('name').desc(),
                'price_asc': 'price',
                'price_desc': '-price',
                'rating': '-rating',
                'category': 'category',
            }
        
        
        products = products.order_by(sort_mapping.get(sort_by))  
    context = {
        'products':products,'search_term':query,'currnet_category':categories,'sort_by': sort_by
    }
    return render(request,'products/products.html',context)

def product_detail(request,product_id):
    '''This show  product details of indivisual product '''
    product = get_object_or_404(Product,pk=product_id)
    context = {
        'product':product,
        

    }
    return render(request,'products/product_detail.html',context)