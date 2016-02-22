from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from mainp2p.models import Author


def login(request):
    return render(request, 'mainp2p/login.html')

def main(request):
	Username = request.GET["UserName"]
    	Password = request.GET["Password"]
	if User.objects.filter(username=Username).exists():
		return render(request, 'mainp2p/login.html')
	else:
	    	user = User.objects.create_user(username=Username,
						 email="",
						password=Password)
	return render(request, 'mainp2p/index.html')
