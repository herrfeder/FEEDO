from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'createfeed/$',views.createfeed,name='createfeed'),
    url(r'^(?P<url_id>[0-9]+)/dashboard/$',views.dashboard,name='dashboard'),
    url(r'showfeed/$',views.showfeed,name='showfeed'),
    url(r'^createfeed/ajax/loadproxysite/$', 
        views.loadproxysite, 
        name='loadproxysite'),

    url(r'^createfeed/ajax/processframe/$', 
        views.processframe,
        name='processframe'),
]


