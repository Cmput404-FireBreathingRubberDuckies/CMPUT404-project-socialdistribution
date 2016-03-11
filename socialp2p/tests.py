from django.test import TestCase
from socialp2p.models import Author, FriendRequest, Post
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import uuid
# Create your tests here.

class Tests(TestCase):

    def setup(self):
        self.client = APIClient()

    def test_create_author(self):

	Auuid = uuid.uuid4()

        user = User.objects.create_user("test", "test@hotmail.com", "testpassword")
	author = Author(user=user, uuid=Auuid)
	author.save()
	
	self.assertEqual(User.objects.count(), 1)
	self.assertEqual(Author.objects.count(), 1)
	self.assertEqual(author.uuid, Auuid)

    def test_author_list_api(self):

	ApiUrl = "http://127.0.0.1:8000/api/author/"
	response = self.client.get(ApiUrl)

	self.assertEqual(response.status_code, status.HTTP_200_OK)
	
    def test_author_api(self):

	Auuid = uuid.uuid4()
        user = User.objects.create_user("test", "test@hotmail.com", "testpassword")
	author = Author(user=user, uuid=Auuid)
	author.save()

	ApiUrl = "http://127.0.0.1:8000/api/author/" + str(Auuid) + "/"
	GetResponse = self.client.get(ApiUrl)
	
	data={"host":"hello"}
	PutResponse = self.client.put(ApiUrl, data, format='json')


	self.assertEqual(GetResponse.status_code, status.HTTP_200_OK)
	self.assertEqual(PutResponse.status_code, status.HTTP_200_OK)




