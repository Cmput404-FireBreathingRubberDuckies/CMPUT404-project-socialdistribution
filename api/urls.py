from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from api import views, models
from rest_framework import routers


# router = routers.DefaultRouter()
# router.register(r'author', models.AuthorViewSet)

urlpatterns = [
    url(r'^authors/$', views.author_list, name='author_list'),
    url(r'^authors/(?P<author_uuid>[^/]+)/$', views.author_detail, name='author_detail'),
    url(r'^friendrequest/$', views.friend_request, name='friend_request'),
    #url(r'^author/(?P<pk>[0-9]+)/$', views.Author_detail),
    # url(r'^authors/(?P<user_uuid>\w+)/$', views.author_info, name='info'),
    # url(r'^author/(?P<username>\w+)/$', views.Author_detail, name='detail'),
]
