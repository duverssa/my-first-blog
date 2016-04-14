from django.contrib import admin
from .models import Post, UserProfile

admin.site.register(Post) #create post
admin.site.register(UserProfile) #create user