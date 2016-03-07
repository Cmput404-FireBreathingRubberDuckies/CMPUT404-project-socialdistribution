from django.contrib.auth.models import User, Group
from rest_framework import serializers
from socialp2p.models import Author


class AuthorSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Author
        fields = ('id', 'uuid', 'user', 'host', 'photo','friends',)


