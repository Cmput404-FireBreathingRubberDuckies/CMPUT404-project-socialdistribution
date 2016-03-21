from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^authenticate/$', views.authenticate_view, name='authenticate'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^posts/$', views.posts_view, name='posts'),
    url(r'^new_comment/$', views.new_comment, name='new_comment'),
]
