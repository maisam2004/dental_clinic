from django.shortcuts import render


def homepage(request):
    """ Renders the homepage of the website.

    This view function handles the rendering of the homepage template. """
    context = {'is_homepage': True,} 

    return render(request, 'core/homepage.html', context)