from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Post, Tag
from ..views import PostsList


class PostsTests(TestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(title='Post1', slug='new_post1', body='body of the post1')
        self.tag = Tag.objects.create(title='python', slug='python')
        self.post.tags.set([self.tag.pk])
        self.user = User.objects.create_superuser('admin', 'admin@test.com', 'admin')

    def test_post_list_view(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'body of the post1')
        self.assertContains(response, 'python')
        self.assertTemplateUsed(response, 'blog_engine/posts_list.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.post.slug}))
        no_response = self.client.get(reverse('post_detail', kwargs={'slug': 'new_post_100'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'body of the post1')
        self.assertContains(response, 'python')
        self.assertTemplateUsed(response, 'blog_engine/post_detail.html')

    def test_post_create_view(self):
        response = self.client.get('/post/create/')  # user is not superuser
        self.assertEqual(response.status_code, 403)
        self.client.login(username='admin', password='admin')  # user is superuser
        url = reverse('post_create')
        data = {
            'title': 'New title',
            'body': 'New text',
            'tags': 'python'
        }
        self.client.post(url, data)
        self.assertTrue(Post.objects.filter(title='New title').exists())
        self.assertTrue(Tag.objects.filter(title='python').exists())

    def test_post_update_view(self):
        response = self.client.get('/post/edit/new_post1')  # user is not superuser
        self.assertEqual(response.status_code, 403)
        self.client.login(username='admin', password='admin')  # user is not superuser
        response = self.client.post(reverse('post_update', kwargs={'slug': self.post.slug}), {
            'title': 'updated',
            'body': 'updated'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.title, 'updated')
        self.assertEqual(self.post.body, 'updated')

    def test_post_delete_view(self):
        response = self.client.get('/post/delete/new_post1')  # user is not superuser
        self.assertEqual(response.status_code, 403)
        self.client.login(username='admin', password='admin')  # user is not superuser
        response = self.client.post(
            reverse('post_delete', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(not Post.objects.filter(title='Post1'))


class PostCreateTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser('admin', 'admin@test.com', 'admin')
        self.client.login(username='admin', password='admin')
        self.tag = Tag.objects.create(title='python', slug='python')

    def test_post_create_view(self):
        url = reverse('post_create')
        data = {
            'title': 'New title',
            'body': 'New text',
            'tags': (self.tag, )
        }
        self.client.post(url, data)
        print(Post.objects.get(title='New title'))
        self.assertEqual(Post.objects.last().body, 'New text')
