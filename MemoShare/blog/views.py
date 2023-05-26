from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post, Profile, Like, Comment
from .forms import PostForm, ProfileForm, MailChangeForm, CommentForm, ContactForm
import random
from taggit.models import Tag
import csv

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

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.posted_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.posted_date = timezone.now()
            post.save()
            form.save_m2m()
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
    date_query = request.GET.get("date", "")
    timestart_query = request.GET.get("start", "")
    timeend_query = request.GET.get("end", timezone.now())
    location_query = request.GET.get("location", "")

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
    if location_query:
        results = results.filter(location__icontains=location_query)
        empty = False
    if date_query:
        results = results.filter(memory_date__gte=date_query).filter(memory_date__lte=date_query)
        empty = False
    if timestart_query:
        results = results.filter(memory_date__gte=timestart_query)
        empty = False
    if timeend_query:
        results = results.filter(memory_date__lte=timeend_query)
        empty = False
    if empty:
        results = None

    context = {
        'results': results,
        'query': query,
        'tag_query': tag_query,
        'author_query': author_query,
        'date_query': date_query,
        'timestart_query': timestart_query,
        'timeend_query': timeend_query
    }
    return render(request, 'blog/post_search.html', context)

@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            form.save_m2m()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_edit.html', {'form': form})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_list')

def about(request):
    post = random.choice(Post.objects.all())
    return render(request, 'blog/about.html', {'post': post})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            file = open('responses.csv', 'a')
            writer = csv.writer(file)
            writer.writerow([name,email,message])
            file.close()
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile')
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

def user_delete(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profile.delete()
    user.delete()
    return redirect('post_list')

def user_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(author=user).order_by('posted_date')
    comments = Comment.objects.filter(author=user).order_by('posted_date')
    context = {'user': user, 'profile': profile, 'posts': posts, 'comments': comments}
    return render(request, 'blog/user_profile.html', context)

@login_required
def user_profile_edit(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            form.save_m2m()
            return redirect('user_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/user_profile_edit.html', {'form': form})

@login_required
def user_mail_edit(request):
    user = request.user
    if request.method == "POST":
        form = MailChangeForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()
            return redirect('user_profile')
    else:
        form = MailChangeForm(instance=user)
    return render(request, 'blog/user_mail_edit.html', {'form': form})

def user_page(request, usernamex):
    userx = User.objects.get(username=usernamex)
    profilex = Profile.objects.get(user=userx)
    profile = request.user.profile
    if request.user.is_authenticated and request.method == "POST":
        button = request.POST["follow"]
        if button == "follow":
            profile.follows.add(profilex)
        elif button == "unfollow":
            profile.follows.remove(profilex)
        profile.save()
    postsx = Post.objects.filter(author=userx).order_by('posted_date')
    context = {'userx': userx, 'profile': profile, 'profilex': profilex, 'postsx': postsx}
    return render(request, 'blog/user_page.html', context)
