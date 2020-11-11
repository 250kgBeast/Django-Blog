from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse

from .models import Post, Tag
from .forms import PostCreateForm


class PostsListView(ListView):
    model = Post
    template_name = 'blog_engine/posts_list.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_engine/post_detail.html'


class TagsListView(ListView):
    model = Tag
    template_name = 'blog_engine/tags_list.html'
    context_object_name = 'tags'


class TagDetailView(DetailView):
    model = Tag
    template_name = 'blog_engine/tag_detail.html'


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog_engine/post_create.html'

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.slug])


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog_engine/post_create.html'

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.slug])
