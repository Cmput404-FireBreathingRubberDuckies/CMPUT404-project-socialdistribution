from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from mainp2p.models import Author
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    return render(request, 'mainp2p/login.html')

def authenticate_view(request):
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

@login_required
def main(request):
	print request
	return render(request, 'mainp2p/index.html')
	# Username = request.GET["UserName"]
    # Password = request.GET["Password"]
	# if User.objects.filter(username=Username).exists():
		 # return render(request, 'mainp2p/login.html')
	# else:
	    	# user = User.objects.create_user(username=Username,
						 # email="",
						# password=Password)
		# name = Author.objects.all()
		# context = {"name": name, "Username" : Username}
		# return render_to_response('mainp2p/index.html', context, context_instance=RequestContext(request))
