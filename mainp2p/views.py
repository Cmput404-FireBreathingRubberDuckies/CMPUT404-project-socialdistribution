from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from mainp2p.models import Author
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json

def detail(request, userid):
	userid = User.objects.get(id=userid)
	context = {'userid': userid}
	return(render(request, 'mainp2p/detail.html', context))


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('mainp2p:main'))
    return render(request, 'mainp2p/login.html')

def authenticate_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('mainp2p:main'))
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('mainp2p:main'))
        else:
            return
    return HttpResponseRedirect(reverse('mainp2p:login'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('mainp2p:login'))

def signup_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('mainp2p:main'))
    if request.method == 'POST':
        user = User.objects.create_user(request.POST['username'], None, request.POST['password'])

        author = Author(user=user, host='localhost')
        author.save()

        a_user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if a_user is not None:
            if user.is_active:
                login(request, a_user)
                return HttpResponseRedirect(reverse('mainp2p:main'))
            else:
                return HttpResponseRedirect(reverse('mainp2p:signup'))
        return HttpResponseRedirect(reverse('mainp2p:signup'))
    else:
        return render(request, 'mainp2p/signup.html')

@login_required
def main(request):
    return render(request, 'mainp2p/index.html')
