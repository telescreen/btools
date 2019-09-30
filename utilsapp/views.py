""" Hash application views definitions """

from django.shortcuts import render

# Create your views here.
def index(request):
    """ Return a view to this application """
    return render(request, 'hash.html')
