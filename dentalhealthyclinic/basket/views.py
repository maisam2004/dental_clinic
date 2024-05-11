from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product
from django.contrib import messages

# Create your views here.

def view_basket(request):
    """ A view that renders the basket contents """
    bag = request.session.get('bag', {})

    # ... other calculations ... (total, delivery, etc.) 

    # Prepare context data
    bag_items = []
    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        bag_items.append({
            'item_id': item_id ,
            'quantity': quantity,
            'product': product,
        })

    context = {
        'bag_items': bag_items,
        # ... other variables for your template (total, delivery, etc.)
    }
    #print(bag_items)
    #print(request.session['bag'])
    return render(request, 'basket/basket.html', context) 


def add_to_basket(request, item_id):
    product = Product.objects.get(pk=item_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request,f'Update quantity of  {product.name} ,now you have  {bag[item_id]} of this item in basket')
    else:
        bag[item_id] = quantity
        messages.success(request,f'Added {product.name} to you bag')

    request.session['bag'] = bag

    
    return redirect(redirect_url)


def update_basket(request):
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        bag = request.session.get('bag', {})
        
        product = Product.objects.get(pk=item_id)
        
        if action == 'remove':
            if item_id in bag:
                del bag[item_id]
                messages.warning(request,f'removed {product.name} from you basket ')
        elif action == 'update':
            quantity = int(request.POST.get('quantity'))
            if item_id in bag:
                bag[item_id] = quantity
                
                
        request.session['bag'] = bag

    return redirect('view_basket')
