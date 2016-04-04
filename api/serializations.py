from django.contrib.auth.models import User, Group
from rest_framework import serializers
from socialp2p.models import Author, FriendRequest, Post, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'groups', 'user_permissions')

class FriendProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='uuid')
    class Meta:
        model = Author
        fields = ('id', 'host', 'displayname', 'url')

class AuthorSerializer(serializers.ModelSerializer):
    friends = FriendProfileSerializer(many=True)
    id = serializers.CharField(source='uuid')
    profile_image_url = serializers.SerializerMethodField()

    def get_profile_image_url(self, author_obj):
        if author_obj.photo:
            return author_obj.photo.url
    class Meta:
        model = Author
        fields = ('id', 'host', 'displayname', 'profile_image_url', 'url','friends')

class FriendRequestSerializer(serializers.Serializer):
    query = serializers.SerializerMethodField('friend_request')
    author = FriendProfileSerializer(source='requester')
    friend = FriendProfileSerializer(source='receiver')

    def friend_request(self, obj):
        return 'friendrequest'

class FriendSerializer(serializers.Serializer):
    query = serializers.SerializerMethodField('friend_str')
    uuid = serializers.CharField()
    authors = serializers.SerializerMethodField('getFriends')

    def getFriends(self, author_obj):
        friends = author_obj.friends.all()
        list1 = []
        for friend in friends:
            list1.append(friend.uuid)
        return list1

    def friend_str(self, obj):
        return 'friends'

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='uuid')
    comment = serializers.CharField(source='content')
    published = serializers.CharField(source='datetime')
    author = FriendProfileSerializer()
    class Meta:
        model = Comment
        fields = ('id', 'comment', 'published', 'author')

class PostSerializer(serializers.Serializer):
    id = serializers.CharField(source='uuid')
    author = FriendProfileSerializer()
    published = serializers.DateTimeField(source='datetime')
    content_type = serializers.SerializerMethodField()
    title = serializers.CharField()
    content = serializers.CharField()
    title = serializers.CharField()
    visibility = serializers.CharField()
    comments = serializers.SerializerMethodField('get_comment')
    count = serializers.SerializerMethodField('get_num_comments')
    image_url = serializers.SerializerMethodField()

    def get_content_type(self, post_obj):
        markdown = post_obj.markdown
        return 'text/x-markdown' if markdown else 'text/plain'

    def get_comment(self, post_obj):
        comments = Comment.objects.filter(post=post_obj.id)
        comments = CommentSerializer(comments, many=True)
        return comments.data

    def get_num_comments(self, post_obj):
        comments = Comment.objects.filter(post=post_obj.id)
        return len(comments)

    def get_image_url(self, post_obj):
        if post_obj.image:
            return post_obj.image.url
