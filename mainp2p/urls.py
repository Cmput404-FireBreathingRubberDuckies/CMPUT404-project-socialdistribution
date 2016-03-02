from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^login', views.login_view, name='login'),
    url(r'^authenticate', views.authenticate_view, name='authenticate'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^signup', views.signup_view, name='signup'),
]
