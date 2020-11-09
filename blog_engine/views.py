from django.shortcuts import render, get_object_or_404

from .models import Post, Tag


def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'blog_engine/posts_list.html', context={'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog_engine/post_detail.html', context={'post': post})


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog_engine/tags_list.html', context={'tags': tags})


def tag_detail(request, slug):
    tag = Tag.objects.get(slug__exact=slug)
    return render(request, 'blog_engine/tag_detail.html', context={'tag': tag})
