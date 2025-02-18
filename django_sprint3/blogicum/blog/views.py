from django.shortcuts import get_object_or_404, render

from .models import Post, Category
from datetime import datetime


def index(request):
    template = "blog/index.html"
    post_list = Post.objects.filter(
        pub_date__date__lt=datetime.date(datetime.now()),
        is_published=True,
        category__is_published=True,
    ).order_by("id")[:5]
    context = {"post_list": post_list}
    return render(request, template, context)


def post_detail(request, number):
    template = "blog/detail.html"
    post = get_object_or_404(
        Post,
        pub_date__date__lt=datetime.date(datetime.now()),
        is_published=True,
        category__is_published=True,
        pk=number,
    )
    context = {"post": post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = "blog/category.html"
    category = get_object_or_404(Category, is_published=True, slug=category_slug)
    posts = Post.objects.filter(
        is_published=True,
        category__slug=category_slug,
        pub_date__date__lt=datetime.date(datetime.now()),
    )
    context = {"category": category, "post_list": posts}
    return render(request, template, context)
