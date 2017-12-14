from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^user/(\w+)/$', views.index),
    url(r'^login/$', views.login, name='login'),
    url(r'^login/check/$', views.checklogin),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^createfeed/$',views.createfeed,name='createfeed'),
    url(r'^(?P<url_id>[0-9]+)/dashboard/$',views.dashboard,name='dashboard'),
    url(r'^showfeed/$',views.showfeed,name='showfeed'),
    url(r'^createfeed/ajax/loadproxysite/$', 
        views.loadproxysite, 
        name='loadproxysite'),
    url(r'^createfeed/ajax/processframe/$', 
        views.processframe,
        name='processframe'),


]

