from django.contrib.auth.models import User, Group
from rest_framework import serializers
from socialp2p.models import Author, FriendRequest
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'groups', 'user_permissions')

class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Author
        fields = '__all__'
        depth = 1

class FriendRequestSerializer(serializers.Serializer):
	query = serializers.CharField(source='friend_request')
	Author = UserSerializer(source='requester')
	Friend = UserSerializer(source='receiver')

class FriendSerializer(serializers.ModelSerializer):
	query = serializers.CharField(source='friend')
	class Meta:
		model = Author
		exclude = ('id', 'host', 'photo', 'user')
