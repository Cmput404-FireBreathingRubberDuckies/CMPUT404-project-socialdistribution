from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'^author/(?P<username>\w+)/$', views.Author_detail, 'author')

urlpatterns = [
    #url(r'^author/(?P<pk>[0-9]+)/$', views.Author_detail),
    url(r'^author/(?P<username>\w+)/$', views.Author_detail, name='detail'),
]
