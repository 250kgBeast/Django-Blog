from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Post, Tag
from ..views import PostsList


class PostsListViewTest(TestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(title='Post1', slug='new_post1', body='body of the post1')
        self.tag = Tag.objects.create(title='python', slug='python')
        self.post.tags.set([self.tag.pk])
        self.url = reverse('posts_list')
        self.response = self.client.get(self.url)

    def test_views_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_posts_list_url_resolves_posts_list_view(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, PostsList)

    def test_posts_list_contains_links(self):
        tag_detail_url = reverse('tag_posts_list', kwargs={'slug': self.tag.slug})
        tags_list_url = reverse('tags_list')
        post_detail_url = reverse('post_detail', kwargs={'slug': self.post.slug})
        self.assertContains(self.response, tag_detail_url)
        self.assertContains(self.response, tags_list_url)
        self.assertContains(self.response, post_detail_url)
