from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import uuid
from cloudinary.models import CloudinaryField


class Author(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    host = models.CharField(max_length=100, default="http://socialp2p.herokuapp.com/")
    photo = CloudinaryField('image', default='image/upload/v1457219004/default-avatar.jpg', blank=True)
    friends = models.ManyToManyField('self', related_name="friends", blank=True)

    def displayname(self):
        return self.user.username

    def url(self):
        return self.host + 'api/author/' + str(self.uuid)

    def uuid_str(self):
        return str(self.uuid)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    markdown = models.BooleanField(default=False)
    title = models.TextField()
    content = models.TextField()
    image = CloudinaryField('image', null=True, blank=True)
    PUBLIC = 'PUB'
    FOAF = 'FOF'
    FRIENDS = 'FRS'
    PRIVATE = 'PRV'
    ONLY = 'ONL'
    LOCALFRI = 'LFS'
    SERVERONLY = 'SVO'
    Visibility_CHOICES = (
        (PUBLIC, 'Public to All'),
        (SERVERONLY, 'Public to Local'),
        (FOAF, 'Friends of Friends'),
        (FRIENDS, 'Friends'),
        (LOCALFRI, 'Local Friends'),
        (ONLY, 'Only This Person ...'),
        (PRIVATE, 'Only Me'),
    )
    visibility = models.CharField(max_length=3, choices=Visibility_CHOICES, default=PRIVATE)
    user_can_view = models.ForeignKey(Author, related_name='+', null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now=True)

class FriendRequest(models.Model):
    requester = models.ForeignKey(Author,related_name="requester", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Author,related_name="receiver", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.requester.user.username + " to " + self.receiver.user.username

    def url_friend(self):
        return self.host + 'api/author/' + str(self.uuid)
