from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from socialp2p.models import Author, FriendRequest, Post, Node, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json
import requests
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests


@login_required
def profile(request, author_uuid):
    if str(request.user.author.uuid) != str(author_uuid):
        if request.method=='GET':
            posts = {}
            is_friend = False
            if Author.objects.filter(uuid=author_uuid).exists():
                author = Author.objects.get(uuid=author_uuid)
                posts = Post.objects.filter(author=author).order_by('-datetime')
                if author.friends.filter(uuid=request.user.author.uuid).exists():
                    is_friend = True

            host = 'http://' + request.get_host()
            headers = {'Cookie': 'sessionid=' + request.COOKIES.get('sessionid')}
            r = requests.get(host + reverse('api:author_detail', args=(author_uuid,)), headers=headers)

            if r.status_code == 200:
                author = r.json()
                context = {'user_profile': author, 'is_friend': is_friend, 'posts': posts}
                return render(request, 'socialp2p/detail.html', context)

    else:
        author = Author.objects.get(uuid=author_uuid)
        activity = ""
        if author.github != '':
            github_url = 'https://api.github.com/users/' + author.github + '/events'
            r = requests.get(github_url)
            if r.status_code == 200:
                activity = r.json()

        reqs = FriendRequest.objects.filter(receiver=author, accepted=False)
        follow = FriendRequest.objects.filter(requester=author, accepted=False)
        is_friend = False # need to fix this
        context = {'requests':reqs, 'follow':follow, 'posts': Post.objects.order_by('-datetime'), "activity" : activity}
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
            return HttpResponse("Account not approved by admin yet. Try again later")
    return HttpResponseRedirect(reverse('socialp2p:login'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('socialp2p:login'))

def signup_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('socialp2p:main'))
    if request.method == 'POST':

	if User.objects.filter(username=request.POST['username']).exists():
	    return HttpResponse("Username already taken")

        user = User.objects.create_user(request.POST['username'], None, request.POST['password'])
	user.is_active = False
	user.save()
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
    return render(request, 'socialp2p/posts.html', {'posts': Post.objects.filter(visibility='PUBLIC').order_by('-datetime')})

@login_required
def main(request):
    if request.method == 'POST':
        if request.POST.get('image') == '':
            image_id = ''
        else:
            ret = cloudinary.uploader.upload(request.FILES['image'], sign_url=True)
            image_id = ret['public_id']
    	if request.POST['content'] != '':
                post = Post(author=Author.objects.get(user=request.user), title=request.POST['post-title'], content=request.POST['content'], markdown=request.POST.get('markdown', False), image=image_id, visibility=request.POST['visibility'])
		if request.POST['visibility'] == 'ONL':
		    share_to_author = Author.objects.get(uuid=request.POST['share_to'])
		    post.user_can_view = share_to_author
                post.save()
                return HttpResponseRedirect(reverse('socialp2p:main'))
    	else:
    	    return HttpResponse("Can't post an empty post")
    else:
        data = []
        nodes = Node.objects.all()
        endpoint = '/posts/'
        for node in nodes:
            url = node.host + endpoint
            r = requests.get(url, auth=(node.access_username, node.access_password))
            if r.status_code == 200:
                p = r.json().get('posts')
                data += p

        author = Author.objects.get(user=request.user)
        private_posts = Post.objects.filter(author=author, visibility='PRIVATE')
        my_friend_posts = Post.objects.filter(author=author, visibility='FRIENDS')
	my_other_posts = Post.objects.filter(author=author, visibility='ONL')
	local_public_posts = Post.objects.filter(author=author, visibility='SERVERONLY')
        posts = Post.objects.filter(visibility='PUBLIC')
        posts = posts | private_posts | my_friend_posts | my_other_posts | local_public_posts

        for i in author.friends.all():
            friends_posts = Post.objects.filter(author=i, visibility='FRIENDS')
	    friends_fof_posts = Post.objects.filter(author=i, visibility='FOAF')
	    posts = posts | friends_posts | friends_fof_posts
	    for fof in i.friends.all():
	        fof_posts = Post.objects.filter(author=fof, visibility='FOAF')
            	posts = posts | fof_posts
	
	
	ONL_posts = Post.objects.filter(user_can_view=author, visibility='ONL')
	posts = posts | ONL_posts

        posts = posts.order_by('-datetime')
        authors = Author.objects.order_by('user__username')
        current_author = Author.objects.get(user=request.user)
        comments = Comment.objects.order_by('-datetime')
        return render(request, 'socialp2p/main.html', {'Post': Post, 'posts': posts, 'authors': authors, 'current_author': current_author, 'comments': comments, 'remote_posts':data})

@login_required
def new_comment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        post_uuid = request.POST.get('post')
        comment = Comment(author=Author.objects.get(user=request.user), content=content, post=Post.objects.get(uuid=post_uuid))
        comment.save()
        return HttpResponseRedirect(reverse('socialp2p:main'))
