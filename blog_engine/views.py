from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Post, Tag
from .forms import PostCreateForm


class PostsListView(ListView):
    """
    List of all posts
    """
    model = Post
    template_name = 'blog_engine/posts_list.html'
    context_object_name = 'posts'
    paginate_by = 2
    ordering = ['-date_pub']


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_engine/post_detail.html'


class TagsListView(ListView):
    """
    List of all tags
    """
    model = Tag
    template_name = 'blog_engine/tags_list.html'
    context_object_name = 'tags'


class TagDetailView(DetailView):
    """
    List of posts with specific tag
    """
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


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog_engine/post_delete.html'

    def get_success_url(self):
        return reverse('posts_list')

    def get_login_url(self):
        return reverse('posts_list')
