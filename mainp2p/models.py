from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Posts(models.Model):
	uid = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.CharField(max_length=30)
	image = models.ImageField(upload_to="images/")
	contentType = models.TextField()
	visibilty = models.CharField(max_length=30)

class FriendRequest(models.Model):
	uid = models.ForeignKey(User, primary_key=true, on_delete=models.CASCADE)
	requests = ArrayField(models.ForeignKey(User))

class Friends(models.Model):
	uid = models.ForeignKey(User, primary_key=true, on_delete=models.CASCADE)
	friends = ArrayField(models.ForeignKey(User))
        followers = ArrayField(models.ForeignKey(User))
	
	
