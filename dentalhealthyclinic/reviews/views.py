from django.shortcuts import render
from .models import Review
from .forms import ReviewForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Review
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



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




class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/edit_review.html'  # Create this template
    success_url = '/reviews/'
    def get_form_kwargs(self):
        """Pass the request.user to the form's constructor."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, "The Review was Edited successfully.")
        return super(ReviewUpdateView,self).form_valid(form)

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    context_object_name = 'review'
    success_url = '/reviews/'
    def form_valid(self, form):
        messages.success(self.request, "The review was deleted successfully.")
        return super(ReviewDeleteView,self).form_valid(form)