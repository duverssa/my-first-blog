from django.conf.urls import include, url
from . import views #import from current directory

urlpatterns = [
    url(r'^$',  views.post_list, name='post_list'), #shows all the posts
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'), #creates url for individual post
    url(r'^post/new/$', views.post_new, name='post_new'), #url for a new post
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'), #url to edit post
    url(r'^blog/register/$', views.register, name='register'), #added new URL for registration 4/13
    url(r'^login/$', views.user_login, name='login'), #added login view 4/20
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'), # added logout view 4/20
]
