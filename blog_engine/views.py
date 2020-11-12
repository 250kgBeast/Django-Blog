from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404

from .models import Post, Tag
from .forms import PostCreateForm, TagCreateForm


class PostsList(ListView):
    """
    List of all posts
    """
    model = Post
    template_name = 'blog_engine/posts_list.html'
    context_object_name = 'posts'
    paginate_by = 2
    ordering = ['-date_pub']


class PostDetail(DetailView):
    model = Post
    template_name = 'blog_engine/post_detail.html'


class TagsList(ListView):
    """
    List of all tags
    """
    model = Tag
    template_name = 'blog_engine/tags_list.html'
    context_object_name = 'tags'


class TagPostList(ListView):
    """
    List of posts with specific tag
    """
    template_name = 'blog_engine/tag_posts_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog_engine/post_create_or_update.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.slug])


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog_engine/post_create_or_update.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.slug])


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog_engine/post_delete.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('posts_list')


class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagCreateForm
    template_name = 'blog_engine/tag_create_or_update.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('posts_list')


class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagCreateForm
    template_name = 'blog_engine/tag_create_or_update.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('posts_list')


class TagDelete(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'blog_engine/tag_delete.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('tags_list')
