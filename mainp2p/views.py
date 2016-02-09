from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render

def index(request):
    return render(request, 'mainp2p/index.html')
