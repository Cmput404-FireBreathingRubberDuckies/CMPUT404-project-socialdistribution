from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.
class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	markdown = models.BooleanField(default=False)
	content = models.TextField()
	image = models.ImageField(upload_to="images/post")
	visibility = models.CharField(max_length=30)
	user_can_view = models.ForeignKey(User, related_name='+', blank=True)

class Author(AbstractBaseUser):
	host = models.CharField(max_length=100, default="local")
	photo = models.ImageField(upload_to="images/profile", blank=True)
