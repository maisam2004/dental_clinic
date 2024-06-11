from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product
from django.contrib import messages

# Create your views here.

def view_basket(request):
    """
    Renders the shopping basket contents.

    This view retrieves the basket data from the session, fetches the corresponding product 
    details, and prepares the context to be displayed in the basket template.

    Args:
        request: The HttpRequest object representing the current request.

    Returns:
        HttpResponse: An HTTP response containing the rendered basket template.
   
 """
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
    
    #Adds a product to the shopping basket or updates its quantity.

    #This view handles the logic for adding products to the basket. It retrieves
   # the product, updates the basket in the session, and adds a success message.

   # Args:
      #  request: The HttpRequest object representing the current request.
      #  item_id: The ID of the product to add to the basket.

    
    product = Product.objects.get(pk=item_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request,f'Update quantity of  {product.name} ,now you have  {bag[item_id]} of this item in basket',extra_tags="show_bag_contents")
    else:
        bag[item_id] = quantity
        messages.success(request,f'Added {product.name} to you bag',extra_tags="show_bag_contents")

    request.session['bag'] = bag

    
    return redirect(redirect_url)


def update_basket(request):

    """
    Updates the quantity of a product in the basket or removes it.

    This view handles the logic for updating the basket when a user changes the quantity
    of a product or removes it entirely.

    Args:
        request: The HttpRequest object representing the current request.

    Returns:
        HttpResponseRedirect: Redirects the user to the basket view.
    """
    
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
                messages.info(request, f'Quantity for {product.name} updated to {quantity}.')  # Add this line

                
        request.session['bag'] = bag

    return redirect('view_basket')
