from django.shortcuts import render
from django.utils import timezone
from . models import Post#import from current directory, firl models,
from django.shortcuts import render, get_object_or_404
from . forms import PostForm, UserForm, UserProfileForm #import from current directory, file forms
from django.shortcuts import redirect

def post_list(request): #show post list ordered by publish date
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts}) 

def post_detail(request, pk): #show individual post
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request): #show new post
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk): #show post to edit
	post = get_object_or_404(Post, pk=pk) #creates 404 error if post is not found
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

#created 4/12
def register(request): #show register view

	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES: #possibly need to create folder here
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True

		else:
			print(user_form.errors, profile_form.errors)

	else:
		user_form = UserForm()
		profile_form = UserProfileForm() #below should be request, 'blog/register.html', but changed it
	return render(request, 'blog/base.html', {'user_form': user_form, 'profile_form': profile_form, 'registered' : registered})
