import uuid
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponse
from socialp2p.models import Author, FriendRequest, Post
from socialp2p import views
from api.serializations import *
from django.contrib.auth.models import User
from rest_framework import viewsets, status, permissions

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['GET', 'POST'])
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

@api_view(['GET', 'PUT', 'DELETE'])
def author_detail(request, author_uuid):
    try:
        author_uuid = uuid.UUID(author_uuid)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        author = Author.objects.get(uuid=author_uuid)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def friend_request(request, author_uuid):
    current_user = User.objects.get(id=request.user.id)
    current_author = Author.objects.get(user=current_user)
    try:
        author = Author.objects.get(uuid=author_uuid)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = User.objects.get(author=author)

    if request.method == 'GET':
        requests = FriendRequest.objects.filter(requester=current_author, accepted=False)
        serializer = FriendRequestSerializer(requests, many=True)
        return Response(serializer.data)
    elif request.method =='POST':
        if FriendRequest.objects.filter(requester=current_author, receiver=author).exists():
            return HttpResponse("Already added Friend")
        else:
            friendRequest = FriendRequest(requester=current_author, receiver=author)
            friendRequest.save()
            return HttpResponseRedirect(reverse('socialp2p:profile', args=[user.username]))

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

# Currently returning a list of posts, needs changes to match requirements
@api_view(['GET', 'POST', 'DELETE'])
def public_posts(request):
    if request.method == 'GET':
        public_posts = Post.objects.filter(visibility="PUB")
        serializer = PostSerializer(public_posts, many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
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
