from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

POSTS_ON_MAIN_PAGE = 5


def get_posts():
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    ).select_related(
        'author',
        'location',
        'category',
    )


def index(request):
    posts = get_posts()[:POSTS_ON_MAIN_PAGE]
    context = {
        'post_list': posts,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        get_posts(),
        id=post_id,
    )
    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = get_posts().filter(
        category=category,
    )
    context = {
        'category': category,
        'post_list': posts,
    }
    return render(request, 'blog/category.html', context)
