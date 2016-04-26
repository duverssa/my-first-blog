from django import forms
from .models import Post, UserProfile, Category, Page
from django.contrib.auth.models import User

class PostForm(forms.ModelForm): #create a post
	class Meta:
		model = Post
		fields = ('title', 'text',)

#edit 4/12
class UserForm(forms.ModelForm): #create a user registration form
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm): #create the user profile 
	class Meta:
		model = UserProfile
		fields = ('website', 'picture')