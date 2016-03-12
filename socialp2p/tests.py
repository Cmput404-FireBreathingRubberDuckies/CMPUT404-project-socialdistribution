from django.test import TestCase
from socialp2p.models import Author, FriendRequest, Post, Comment
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import uuid
# Create your tests here.

class Tests(TestCase):

    def setup(self):
        self.client = APIClient()
    
    #Testing the author model
    def test_create_author(self):

	Auuid = uuid.uuid4()
	Frienduuid = uuid.uuid4()

        user = User.objects.create_user("test", "test@hotmail.com", "testpassword")
	author = Author(user=user, uuid=Auuid)
	author.save()

	friend = User.objects.create_user("testFriend", "testFriend@hotmail.com", "FriendPassword")
	Friendauthor = Author(user=friend, uuid=Frienduuid)
	Friendauthor.save()

	author.friends.add(Friendauthor)
	
	self.assertEqual(User.objects.count(), 2)
	self.assertEqual(Author.objects.count(), 2)
	self.assertEqual(author.uuid, Auuid)
	self.assertEqual(author.friends.count(), 1)

    #Testing the FriendRequest model
    def test_friend_request(self):

	ReqUuid = uuid.uuid4()
	RecvUuid = uuid.uuid4()

	ReqUser = User.objects.create_user("Requester", "test@hotmail.com", "testpassword")
	ReqAuthor = Author(user=ReqUser, uuid=ReqUuid)
	ReqAuthor.save()

	RecvUser = User.objects.create_user("Receiver", "test@hotmail.com", "testpassword")
	RecvAuthor = Author(user=RecvUser, uuid=RecvUuid)
	RecvAuthor.save()
	
	friendrequest = FriendRequest(requester=ReqAuthor, receiver=RecvAuthor)
	friendrequest.save()
	
	self.assertEqual(FriendRequest.objects.count(), 1)
	self.assertEqual(friendrequest.requester.uuid, ReqUuid)
	self.assertEqual(friendrequest.receiver.uuid, RecvUuid)
    
    #Testing the post model
    def test_post(self):

	Postuuid = uuid.uuid4()
	
        user = User.objects.create_user("test", "test@hotmail.com", "testpassword")
	author = Author(user=user)
	author.save()

	posts = Post(author=author, title="test post", content="this is a test", visibility="PUBLIC", uuid=Postuuid)
	posts.save()

	self.assertEqual(Post.objects.count(), 1)
	self.assertEqual(posts.visibility, "PUBLIC")
	self.assertEqual(posts.uuid, Postuuid)

    #Testing the comment model
    def test_comment(self):

	Commentuuid = uuid.uuid4()

        user = User.objects.create_user("test", "test@hotmail.com", "testpassword")
	author = Author(user=user)
	author.save()

	posts = Post(author=author, title="test post", content="this is a test", visibility="PUBLIC")
	posts.save()

	comment = Comment(author=author, post=posts, uuid=Commentuuid)
	comment.save()

	self.assertEqual(Comment.objects.count(), 1)
	self.assertEqual(comment.uuid, Commentuuid)

    #Test author_list api that returns a list of authors 
    def test_author_list_api(self):

	ApiUrl = "http://127.0.0.1:8000/api/author/"
	response = self.client.get(ApiUrl)

	self.assertEqual(response.status_code, status.HTTP_200_OK)
	
    #Test the author api
    def test_author_api(self):

	Auuid = uuid.uuid4()
        user = User.objects.create_user("test", "test@hotmail.com", "testpassword")
	author = Author(user=user, uuid=Auuid)
	author.save()
	ApiUrl = "http://127.0.0.1:8000/api/author/" + str(Auuid) + "/"

	#Test GET method. The GET method returns a specific author
	GetResponse = self.client.get(ApiUrl)
	self.assertEqual(GetResponse.status_code, status.HTTP_200_OK)

	#Test DELETE method. The DELETE method delete the author
	DeleteResponse = self.client.delete(ApiUrl)
	self.assertEqual(DeleteResponse.status_code, status.HTTP_204_NO_CONTENT)

    #Test friend_request_api
    def test_friend_request_api(self):

	ReqUuid = uuid.uuid4()
	RecvUuid = uuid.uuid4()

	ReqUser = User.objects.create_user("Requester", "test@hotmail.com", "testpassword")
	ReqAuthor = Author(user=ReqUser, uuid=ReqUuid)
	ReqAuthor.save()

	self.client.login(username=ReqUser.username, password="testpassword")

	RecvUser = User.objects.create_user("Receiver", "test@hotmail.com", "testpassword")
	RecvAuthor = Author(user=RecvUser, uuid=RecvUuid)
	RecvAuthor.save()

	ApiUrl = "http://127.0.0.1:8000/api/friendrequest/" + str(RecvUuid) + "/"

	#Test POST method. The POST method create friend request
	PostResponse = self.client.get(ApiUrl)
	self.assertEqual(PostResponse.status_code, status.HTTP_200_OK)
    
	#Test GET method. The GET method returns a list of friend request
	GetResponse = self.client.get(ApiUrl)
	self.assertEqual(GetResponse.status_code, status.HTTP_200_OK)

    def test_friends_api(self):
	
	Auuid = uuid.uuid4()
	Frienduuid = uuid.uuid4()

        user = User.objects.create_user("test", "test@hotmail.com", "testpassword")
	author = Author(user=user, uuid=Auuid)
	author.save()

	friend = User.objects.create_user("testFriend", "testFriend@hotmail.com", "FriendPassword")
	Friendauthor = Author(user=friend, uuid=Frienduuid)
	Friendauthor.save()
   
	self.client.login(username=user.username, password="testpassword")

	ApiUrl = "http://127.0.0.1:8000/api/friends/" + str(Auuid) + "/"	

	#Test GET method. The GET method returns a list of friends
	GetResponse = self.client.get(ApiUrl)
	self.assertEqual(GetResponse.status_code, status.HTTP_200_OK)

	#Test POST method. The POST method create friend request
	PostResponse = self.client.get(ApiUrl)
	self.assertEqual(PostResponse.status_code, status.HTTP_200_OK)

    #Test post api
    def test_post_api(self):
	
        Auuid = uuid.uuid4()
	
        user = User.objects.create_user("test", "test@hotmail.com", "testpassword")
	author = Author(user=user, uuid=Auuid)
	author.save()

	posts = Post(author=author, title="test post", content="this is a test")
	posts.save()

	ApiUrl = "http://127.0.0.1:8000/api/posts/"

	#Test GET method. The GET method returns a list of posts
	GetResponse = self.client.get(ApiUrl)
	self.assertEqual(GetResponse.status_code, status.HTTP_200_OK)

