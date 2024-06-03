from django.shortcuts import render
from .models import Review
from .forms import ReviewForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Review

def display_reviews(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/reviews.html', context) 




@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('reviews')  # Adjust the redirect to your reviews list view
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    message = f"Error in {field}: {error}"
                    messages.add_message(request, messages.ERROR, message, extra_tags='toast')
    else:
        form = ReviewForm(user=request.user)

    return render(request, 'reviews/add_review.html', {'form': form})
