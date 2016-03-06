from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^login', views.login_view, name='login'),
    url(r'^authenticate', views.authenticate_view, name='authenticate'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^signup', views.signup_view, name='signup'),
    url(r'^profile/(?P<username>\w+)/$', views.detail, name='detail'),
    #url(r'^profile/(?P<userid>[0-9]+)/$', views.detail, name='detail'),
] + static('images', document_root=settings.BASE_DIR+'/images')
