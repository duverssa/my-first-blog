from django.contrib import admin
from .models import Post, UserProfile, Category, Page

admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Post) #create post
admin.site.register(UserProfile) #create user