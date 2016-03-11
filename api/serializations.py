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
    query = serializers.SerializerMethodField('friend_request')
    Author = UserSerializer(source='requester')
    Friend = UserSerializer(source='receiver')

    def friend_request(self, obj):
        return "friendrequest"

class FriendSerializer(serializers.Serializer):
    query = serializers.SerializerMethodField('friend_str')
    uuid = serializers.CharField(source='uuid_str')
    authors = serializers.SerializerMethodField('getFriends')

    def getFriends(self, author_obj):
        friends = author_obj.friends.all()
	list1 = []
	for a in friends:
		list1.append(a.author.uuid)
	return list1

    def friend_str(self, obj):
	return "friends"
