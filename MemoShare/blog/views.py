from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Post, Profile, Like, Comment
from .forms import PostForm
import random

def post_list(request):
    posts = Post.objects.filter(posted_date__lte=timezone.now()).order_by('posted_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    is_liked = post.likes.filter(id=request.user.id).exists()
    comments = post.comments.all()

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        Comment.objects.create(post=post, author=request.user, text=comment_text)
        if 'like-btn' in request.POST:
            if not is_liked:
                Like.objects.create(user=request.user, post=post)
        elif 'unlike-btn' in request.POST:
            if is_liked:
                Like.objects.filter(user=request.user, post=post).delete()

        return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_detail.html', {'post': post, 'is_liked': is_liked, 'comments': comments})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.posted_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
"""
def post_new(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(title=title, content=content, author=request.user)
        return redirect('view_post', pk=post.pk)
    return render(request, 'create_post.html')
"""
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.posted_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    return redirect('post_detail', pk=post.pk)

@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Like.objects.filter(user=request.user, post=post).delete()
    return redirect('post_detail', pk=post.pk)

def post_search(request):
    query = request.GET.get("query", "")
    author_query = request.GET.get("author", "")
    tag_query = request.GET.get("tag", "")
    #date_query = request.GET.get("date", default="")
    #location_query = request.GET.get("location", default="")

    empty = True
    results = Post.objects.all()

    if query:
        results = results.filter(Q(title__icontains=query) | Q(text__icontains=query))
        empty = False
    if tag_query:
        results = results.filter(tags__name__icontains=tag_query)
        empty = False
    if author_query:
        results = results.filter(author__username__icontains=author_query)
        empty = False
    if empty:
        results = None

    context = {
        'results': results,
        'query': query,
        'tag_query': tag_query,
        'author_query': author_query,
    }
    return render(request, 'blog/post_search.html', context)

def about(request):
    post = random.choice(Post.objects.all())
    return render(request, 'blog/about.html', {'post': post})

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'blog/user_register.html', {'form': form})

def user_login(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You have logged in as {username}.")
				return redirect("user_profile")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="blog/user_login.html", context={"login_form":form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have logged out successfully.") 
    return redirect('about')

def user_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(author=user).order_by('posted_date')
    context = {'user': user, 'profile': profile, 'posts': posts}
    return render(request, 'blog/user_profile.html', context)