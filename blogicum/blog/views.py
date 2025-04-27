from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from blog.constants import QUANTITY_PUB
from blog.forms import CommentForm, EditProfileForm, PostForm
from blog.models import Category, Comment, Post
from blog.service import get_published_posts, paginate


def index(request) -> None:
    """Отображает главную страницу с постами."""
    post_list = (get_published_posts(
        filter_flag=True, count_comment_flag=True
    ))
    page_obj = paginate(post_list, request, QUANTITY_PUB)
    return render(request, 'blog/index.html',
                  {'page_obj': page_obj})


def post_detail(request, post_id):
    """Отображает подробности поста по его id."""
    post = get_object_or_404(
        Post.objects.select_related('author', 'location', 'category'),
        pk=post_id
    )
    user = request.user
    if not post.is_published and post.author != user:
        raise Http404()
    form = CommentForm()
    return render(request, 'blog/detail.html',
                  {'post': post, 'form': form,
                   'comments': post.comments.all()})


def category_posts(request, category_slug: str) -> None:
    """Отображает посты по категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    filtered_posts = (get_published_posts(
        filter_flag=True,
        count_comment_flag=True
    ).filter(category=category))
    page_obj = paginate(filtered_posts, request, QUANTITY_PUB)
    return render(request, 'blog/category.html',
                  {'page_obj': page_obj, 'category': category})


def profile(request, username):
    """Отображает профиль авторизованного пользователя."""
    user = get_object_or_404(User, username=username)
    current_user = request.user
    posts = (get_published_posts(
        queryset=Post.objects.filter(author=user),
        user=current_user, count_comment_flag=True
    ))
    page_obj = paginate(posts, request, QUANTITY_PUB)
    return render(request, 'blog/profile.html',
                  {'profile': user, 'page_obj': page_obj})


@login_required
def edit_profile(request):
    """Отображает страницу редактирования профиля."""
    form = EditProfileForm(request.POST,
                           instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile',
                        username=request.user.username)
    return render(request, 'blog/user.html',
                  {'form': form})


@login_required
def create_post(request):
    """Отображает страницу создания нового поста."""
    form = PostForm(request.POST or None, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile',
                        username=request.user.username)
    return render(request, 'blog/create.html',
                  {'form': form})


@login_required
def edit_post(request, post_id):
    """Отображает страницу редактирования поста по id."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html',
                  {'form': form})


@login_required
def add_comment(request, post_id):
    """Отображает страницу добавления комментария."""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('blog:post_detail',
                        post_id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Отображает страницу редактирования комментария."""
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden()
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect(
            'blog:post_detail',
            post_id=post_id
        )
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment.html',
                  {'form': form, 'comment': comment})


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаляет комментарий и перенаправляет пользователя на страницу поста."""
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author and not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail',
                        post_id=comment.post_id)
    return render(request, 'blog/comment.html',
                  {'comment': comment})


@login_required
def delete_post(request, post_id):
    """Удаляет пост и перенаправляет пользователя на страницу профиля."""
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    if request.method == 'POST':
        if user == post.author or user.is_superuser:
            post.delete()
            return redirect('blog:profile', username=request.user.username)
        return HttpResponseForbidden()
    return render(request, 'blog/create.html',
                  {'post': post, 'form': form})
