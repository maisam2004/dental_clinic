from django.shortcuts import render,redirect

# Create your views here.

def view_basket(request):
    """ A view that renders the basket contents """
    return render(request,'basket/basket.html')

def add_to_basket(request, item_id):
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag

    
    return redirect(redirect_url)


""" def update_basket(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        bag = request.session.get('bag', {})

        if action == 'remove':
            if item_id in bag:
                del bag[item_id]
        elif action == 'update':
            quantity = int(request.POST.get('quantity'))
            if item_id in bag:
                bag[item_id] = quantity

        request.session['bag'] = bag

    return redirect('view_basket') """
