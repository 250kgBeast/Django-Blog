from django.shortcuts import render
from django.http import HttpResponse

from .models import Post


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog_engine/post_detail.html', {'posts': posts})
