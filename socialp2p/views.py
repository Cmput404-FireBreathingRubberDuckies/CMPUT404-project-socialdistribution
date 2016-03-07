from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from socialp2p.models import Author, FriendRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json

def detail(request, username):
	if request.method=='GET':
		username = User.objects.get(username=username)
		context = {'username': username}
		return(render(request, 'socialp2p/detail.html', context))
      	elif request.method=='POST':
		if request.user.is_authenticated():
			username = User.objects.get(username=username)
			context = {'username': username}
			if FriendRequest.objects.filter(requester=request.user, receiver=username).exists():
				return HttpResponse("Already added Friend")
			else:
				friendRequest = FriendRequest(requester=request.user, receiver=username)
				friendRequest.save()
				return(render(request, 'socialp2p/detail.html', context))
		


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('socialp2p:main'))
    return render(request, 'socialp2p/login.html')

def authenticate_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('socialp2p:main'))
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('socialp2p:main'))
        else:
            return
    return HttpResponseRedirect(reverse('socialp2p:login'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('socialp2p:login'))

def signup_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('socialp2p:main'))
    if request.method == 'POST':
        user = User.objects.create_user(request.POST['username'], None, request.POST['password'])

        author = Author(user=user, host='localhost')
        author.save()

        a_user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if a_user is not None:
            if user.is_active:
                login(request, a_user)
                return HttpResponseRedirect(reverse('socialp2p:main'))
            else:
                return HttpResponseRedirect(reverse('socialp2p:signup'))
        return HttpResponseRedirect(reverse('socialp2p:signup'))
    else:
        return render(request, 'socialp2p/signup.html')

@login_required
def main(request):
    return render(request, 'socialp2p/index.html')
