from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import uuid
from cloudinary.models import CloudinaryField

# Create your models here.
class Post(models.Model):
	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	markdown = models.BooleanField(default=False)
	content = models.TextField()
	#image = models.ImageField(upload_to="images/post", null=True, blank=True)
	image = CloudinaryField('image', blank=True)
	visibility = models.CharField(max_length=30)
	user_can_view = models.ForeignKey(User, related_name='+', blank=True)

class Author(models.Model):
	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	host = models.CharField(max_length=30)
	#photo = models.ImageField(upload_to="images/profile", default="images/profile/default-avatar.jpg", null=True, blank=True)
	image = CloudinaryField('image', default='image/upload/v1457219004/default-avatar.jpg', blank=True)
	friends = models.ManyToManyField(User, related_name="friend", blank=True)

class Comment(models.Model):
	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	content = models.TextField()
