from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .models import Post
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
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_search(request):
    query = request.GET.get("q", default="")
    text_query = request.GET.get("text", default="")
    author_query = request.GET.get("author", default="")
    tag_query = request.GET.get("tag", default="")
    #date_query = request.GET.get("date", default="")
    #location_query = request.GET.get("location", default="")

    results = Post.objects.all()

    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(author__username__icontains=query) |
            Q(tag__name=query)
            #Q(date__icontains=query) |
            #Q(location__icontains=query) |
        )
    
    if text_query:
        results = results.filter(text__icontains=text_query)
    if tag_query:
        results = results.filter(date__icontains=tag_query)
    if author_query:
        results = results.filter(author__username__icontains=author_query)

    context = {
        'results': results,
        'query': query,
        'text_query': text_query,
        'tag_query': tag_query,
        'author_query': author_query,
    }
    return render(request, 'blog/post_search.html', context)

def about(request):
    return render(request, 'blog/about.html')