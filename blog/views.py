from django.shortcuts import render
from django.utils import timezone
from . models import Post#import from current directory, file models,
from django.shortcuts import render, get_object_or_404
from . forms import PostForm, UserForm, UserProfileForm #import from current directory, file forms
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

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
	
	# A boolean value for telling the template whether the registration was successful.
	# Set to False intially. Code changes value to True when registration succeeds
	registered = False

	# If it's a HTTP POST, we're interested in processing form data
	if request.method == 'POST':
		# Attempt to grab information from the raw form information
		# Note that we make use of both UserForm and UserProfileForm
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		# If the two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database
			user = user_form.save()

			# Now we hash the password with the set_password method
			# Once hashed, we can update the user object
			user.set_password(user.password)
			user.save()

			# Now sort out the UserProfile instance
			# Since we need to se the user attribute ourselves, we set commit=False
			# This delays saving the model until we're ready to avoid integrity problems
			profile = profile_form.save(commit=False)
			profile.user = user
			
			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and put it in the UserProfile model
			if 'picture' in request.FILES: #possibly need to create folder here
				profile.picture = request.FILES['picture']

			# No we save the UserProfile model instance
			profile.save()

			# Update our variable to tell the template registration was successful
			registered = True

		# Invalid form of forms - mistake or something else?
		# Print problems to the terminal
		# They'll also be showm to the user
		else:
			print(user_form.errors, profile_form.errors)


	# Not a HTTP POST, so we render our form using two ModelForm intances
	# Print problems to the terminal
	# They'll also be shown to the user
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	#Render the template depending on the context
	return render(request, 'blog/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered' : registered} )

def user_login(request):
	#if the user is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password proivded by the user.
		# This information is obtained from the Login form.
			# use request.POST.get('<variable') as opposed to request.POST['<variable'],
			# because the request.POST.get('<variable>') return None if the value does not exist,
			# while the request.POST['<variable>'] will raise key error exception
		username = request.POST.get('username')
		password = request.POST.get('password')
		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User objectis returned if it is
		user = authenticate(username=username, password=password)
		# if we have a User object, the details are correct.
		# if None, no user# with matching credentials was found.
		if user: 
			# is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in
				# send user back to homepage
				login(request, user)
				return HttpResponseRedirect('/login') #may need to change this to 'blog/' or '/'
		else:
			# Bad Login details were provided, so user cannot log in
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
	# The request is not a HTTP POST, so display the Login form.
	# This scenario would most likely be a HTTP GET
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'blog/login.html', {})

@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")

#use the login_required() decorator to ensure only those logged in can access the view
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out
	logout(request)

	# Take the user back to the homepage
	return HttpResponseRedirect('/') #might need to change this
