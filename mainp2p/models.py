from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Posts(models.Model):
	uid = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.CharField(max_length=30)
	image = models.ImageField(upload_to="images/")
	contentType = models.TextField()
	visibilty = models.CharField(max_length=30)
