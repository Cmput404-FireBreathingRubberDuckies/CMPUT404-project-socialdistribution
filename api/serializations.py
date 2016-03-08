from django.contrib.auth.models import User, Group
from rest_framework import serializers
from socialp2p.models import Author
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login')

class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Author
        fields = '__all__'
        depth = 1
