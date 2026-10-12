from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import Post
from .forms import PostForm, SignUpForm


def post_list(request):
    """List all posts with search (?q=) and pagination (?page=)."""
    query = request.GET.get('q', '').strip()
    posts = Post.objects.select_related('author')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    paginator = Paginator(posts, 5)  # 5 posts per page
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'query': query})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'heading': 'New Post'})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied  # only the author can edit

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'heading': 'Edit Post'})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied  # only the author can delete

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in right after signup
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
