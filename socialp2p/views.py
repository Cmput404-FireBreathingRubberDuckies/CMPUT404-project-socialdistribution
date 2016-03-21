from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from socialp2p.models import Author, FriendRequest, Post, Node
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests as req


@login_required
def profile(request, author_uuid):
    author = None
    try:
        author = Author.objects.get(uuid=author_uuid)
    except Author.DoesNotExist:
        host = 'http://' + request.get_host()
        headers = {'Cookie': 'sessionid=' + request.COOKIES.get('sessionid')}
        r = req.get(host + reverse('api:author_detail', args=(author_uuid,)), headers=headers)
        author = r.json()
        is_friend = False
        context = {'user_profile': author, 'is_friend': is_friend}
        return render(request, 'socialp2p/detail.html', context)
    requests = FriendRequest.objects.filter(receiver=author, accepted=False)
    follow = FriendRequest.objects.filter(requester=author, accepted=False)
    # is_friend = False
    # if len(request.user.author.friends.filter(uuid=author.uuid)) == 1:
        # is_friend = True
    context = {'requests':requests, 'follow':follow, 'posts': Post.objects.order_by('-datetime')}
    return render(request, 'socialp2p/profile.html', context)



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

        author = Author(user=user)
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

# all posts public on server
@login_required
def posts_view(request):
    return render(request, 'socialp2p/posts.html', {'posts': Post.objects.filter(visibility='PUB').order_by('-datetime')})

@login_required
def main(request):
    if request.method == 'POST':
        if request.POST.get('image') == '':
            image_id = ''
        else:
            ret = cloudinary.uploader.upload(request.FILES['image'])
            image_id = ret['public_id']
        post = Post(author=Author.objects.get(user=request.user), content=request.POST['content'], markdown=request.POST.get('markdown', False), image=image_id, visibility=request.POST['visibility'])
        post.save()
        return HttpResponseRedirect(reverse('socialp2p:main'))
    else:

	author = Author.objects.get(user=request.user)
	private_posts = Post.objects.filter(author=author, visibility='PRV')
    	posts = Post.objects.filter(visibility='PUB')
	posts = posts | private_posts

        for i in author.friends.all():
	    friends_posts = Post.objects.filter(author=i, visibility='FRS')
	    posts = posts | friends_posts

        posts = posts.order_by('-datetime')
        return render(request, 'socialp2p/main.html', {'Post': Post, 'posts': posts, 'authors': Author.objects.order_by('user__username'), "current_author": Author.objects.get(user=request.user)})

