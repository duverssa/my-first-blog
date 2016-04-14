from django.conf.urls import include, url
from . import views #import from current directory

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'), #shows all the posts
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'), #creates url for individual post
    url(r'^post/new/$', views.post_new, name='post_new'), #url for a new post
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'), #url to edit post
    url(r'^register/$', views.register, name='register'), #added new URL for registration 4/13
]
