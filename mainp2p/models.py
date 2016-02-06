from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Post(models.Model):
	uid = models.ForeignKey(User, on_delete=models.CASCADE)
	markdown = models.BooleanField(default=False)
	content = models.TextField()
	image = models.ImageField(upload_to="images/")
	visibility = models.CharField(max_length=30)
