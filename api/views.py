import uuid
import json
import requests
from PIL import Image
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponse
from socialp2p.models import Author, FriendRequest, Post, Node
from socialp2p import views
from api.serializations import *
from django.contrib.auth.models import User
from rest_framework import viewsets, status, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests

@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def author_list(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    # elif request.method == 'POST':
    #     serializer = AuthorSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def author_detail(request, author_uuid):
    author = None
    try:
        author_uuid = uuid.UUID(author_uuid)
    except Exception as e:
        print "FALIED"
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        author = Author.objects.get(uuid=author_uuid)
    except Author.DoesNotExist:
        endpoint = 'api/author/' 
        nodes = Node.objects.all()
        response_status = 404
        for node in nodes:
            if node.user.username == 'fbook':
                author_uuid_str = str(author_uuid)
                author_uuid_str = author_uuid_str.replace("-", "")
                url = node.host + endpoint + author_uuid_str

            r = requests.get(url, auth=('socialp2p', 'socialp2p'))
            if r.status_code == 200:
                response_status = 200
                author = r.json()
                break
        if response_status != 200:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if request.method == 'GET':
                return Response(author)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    elif request.method == 'POST':
	user = User.objects.get(author=author)
	edit_firstname = request.data.get('edit_firstname')
	edit_lastname = request.data.get('edit_lastname')
	edit_email = request.data.get('edit_email')

	if edit_firstname=='' or edit_lastname=='' or edit_email=='':
	    return HttpResponse("field cannot be empty")

	else:
		user.first_name = edit_firstname
	    	user.last_name = edit_lastname
	    	user.email = edit_email
	    	user.save()
        	if request.POST.get('edit_pic') !='':
           		cloudinary.uploader.destroy(author.photo, invalidate = True)
           		ret = cloudinary.uploader.upload(request.FILES['edit_pic'], invalidate = True)
           		image_id = ret['public_id']
       			author.photo = image_id
	    		author.save()
	    	serializer = AuthorSerializer(author)
	    	return HttpResponseRedirect(reverse('socialp2p:profile', args=[user.username]))
    elif request.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def friend_request(request):
    #current_user = User.objects.get(id=request.user.id)
    #current_author = Author.objects.get(user=current_user)
    #try:
        #author = Author.objects.get(uuid=author_uuid)
    #except Author.DoesNotExist:
        #return Response(status=status.HTTP_404_NOT_FOUND)
    #user = User.objects.get(author=author)

    #if request.method == 'GET':
        #requests = FriendRequest.objects.filter(requester=current_author, accepted=False)
        #serializer = FriendRequestSerializer(requests, many=True)
        #return Response(serializer.data)
    if request.method =='POST':

	user_uuid = json.loads(request.POST.get('author'))
	author_uuid = json.loads(request.POST.get('friend'))
	current_author = Author.objects.get(uuid=user_uuid)
	friend = Author.objects.get(uuid=author_uuid)

        if FriendRequest.objects.filter(requester=current_author, receiver=friend).exists():
            return HttpResponse("Already added Friend")
        else:
            friendRequest = FriendRequest(requester=current_author, receiver=friend)
            friendRequest.save()
	    serializer = FriendRequestSerializer(friendRequest)
            return Response(serializer.data)



@api_view(['GET', 'POST', 'DELETE'])
def friends(request, author_uuid):
    current_user = User.objects.get(id=request.user.id)
    # current_user = ''
    current_author = Author.objects.get(user=current_user)
    # current_author = ''
    try:
        author = Author.objects.get(uuid=author_uuid)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = User.objects.get(author=author)

    if request.method == 'GET':
        serializer = FriendSerializer(author)
        return Response(serializer.data)
    elif request.method == 'POST':

        if request.POST.get("accept"):
            current_author.friends.add(author)
            author.friends.add(current_author)
            friendRequest = FriendRequest.objects.get(requester=author, receiver=current_author)
            friendRequest.accepted = True
            friendRequest.save()
            return HttpResponseRedirect(reverse('socialp2p:profile', args=[request.user.username]))
	elif request.POST.get("delete"):
	    current_author.friends.remove(author)
            author.friends.remove(current_author)
	    if FriendRequest.objects.filter(requester=current_author, receiver=author).exists():
	        friendRequest = FriendRequest.objects.get(requester=current_author, receiver=author)
		friendRequest.accepted = False
		friendRequest.save()
            else:
		friendRequest = FriendRequest.objects.get(requester=author, receiver=current_author)
		friendRequest.accepted = False
		friendRequest.save()
	    return HttpResponseRedirect(reverse('socialp2p:profile', args=[request.user.username]))

# Currently only returning public, private, and friends posts but not friend of friend
@api_view(['GET'])
def posts(request):

    author = Author.objects.get(user=request.user)
    posts = Post.objects.filter(visibility="PUB")

    for i in author.friends.all():
        friends_posts = Post.objects.filter(author=i, visibility="FRS")
        posts = posts | friends_posts

    private_posts = Post.objects.filter(author=author, visibility="PRV")
    friends_posts = Post.objects.filter(author=author, visibility="FRS")
    posts = posts | friends_posts | private_posts

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# Currently only returning public, private, and friends posts but not friend of friend
@api_view(['GET'])
def author_posts(request, author_uuid):

    request_author = Author.objects.get(uuid=author_uuid)
    request_user = User.objects.get(author=request_author)
    current_author = Author.objects.get(user=request.user)
    posts = Post.objects.filter(author=request_author, visibility="PUB")
    private_posts = Post.objects.filter(author=request_author, visibility="PRV")

    if current_author.friends.filter(user=request_user).exists():
	friend_posts = Post.objects.filter(author=request_author, visibility="FRS")
    	posts = posts | private_posts | friend_posts

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# Currently returning a list of posts, needs changes to match requirements
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def public_posts(request):
    public_posts = Post.objects.filter(visibility="PUB")
    serializer = PostSerializer(public_posts, many=True)
    return Response({"query": "posts", "count": len(public_posts), "posts": serializer.data})

@api_view(['GET','POST', 'PUT', 'DELETE'])
def post_detail(request, post_uuid):
    try:
        post_uuid = uuid.UUID(post_uuid)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        post = Post.objects.get(uuid=post_uuid)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if request.method == 'POST':
        edit_content = request.data.get('post_content')
	if request.POST.get('check_remove_picture') != '':
		if post.image != None:
			cloudinary.uploader.destroy(post.image, invalidate = True)
			post.image = ''

        if request.POST.get('post_content') != '':
		post.content = edit_content

	if request.POST.get('post_image') !='':
		if post.image != None:
           		cloudinary.uploader.destroy(post.image, invalidate = True)
           	ret = cloudinary.uploader.upload(request.FILES['post_image'], invalidate = True)
           	image_id = ret['public_id']
		post.image = image_id
	post.save()
	return HttpResponseRedirect(reverse('socialp2p:profile', args=[post.author.user.username]))

