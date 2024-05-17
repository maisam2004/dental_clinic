from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.conf import settings
from django.contrib import messages
from .models import Product,Category
from django.db.models import Q
from django.db.models.functions import Lower 
from .forms import ProductForm

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
        'products':products,'search_term':query,'currnet_category':categories,'sort_by': sort_by,'MEDIA_URL': settings.MEDIA_URL   

    }
    return render(request,'products/products.html',context)

def product_detail(request,product_id):
    '''This show  product details of indivisual product '''
    product = get_object_or_404(Product,pk=product_id)
    context = {
        'product':product,
        'MEDIA_URL': settings.MEDIA_URL   

    }
    return render(request,'products/product_detail.html',context)
def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            #messages.error(request, 'Failed to add product. Please ensure the form is valid.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            return render(request, 'products/add_product.html', {'form': form})  

    else:
        form = ProductForm()


    form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

def edit_product(request, product_id):
    """ Edit a product in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            return render(request, 'products/edit_product.html', {'form': form})
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

