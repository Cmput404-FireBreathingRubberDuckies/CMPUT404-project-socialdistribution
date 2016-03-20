from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from api import views, models
from rest_framework import routers


urlpatterns = [
    url(r'^author/$', views.author_list, name='author_list'),
    url(r'^author/posts/$', views.posts, name='authors_posts'),
    url(r'^author/(?P<author_uuid>[^/]+)/posts/$', views.author_posts, name='author_posts'),
    url(r'^author/(?P<author_uuid>[^/]+)/$', views.author_detail, name='author_detail'),
    url(r'^friends/(?P<author_uuid>[^/]+)/$', views.friends, name='friends'),
    url(r'^friendrequest/$', views.friend_request, name='friend_request'),
    url(r'^posts/$', views.public_posts, name='posts'),
    url(r'^posts/(?P<post_uuid>[^/]+)/$', views.post_detail, name='post_detail')
]
