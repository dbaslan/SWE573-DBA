from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Post, Profile
from .forms import PostForm

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(posted_date__lte=timezone.now()).order_by('posted_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

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
    return render(request, 'blog/about.html')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})