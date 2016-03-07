from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from socialp2p.models import Author
from api.serializations import AuthorSerializer
from django.contrib.auth.models import User

class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

def Author_detail(request, username):
	try:
		user = User.objects.get(username=username)
		userid = user.author.id
		author = Author.objects.get(id=userid)
	except Author.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = AuthorSerializer(author)
		return JSONResponse(serializer.data)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = AuthorSerializer(author, data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)
	elif request.method == 'DELETE':
		author.delete()
		return HttpResponse(status=204)
# Create your views here.
