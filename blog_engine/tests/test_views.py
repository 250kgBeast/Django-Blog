from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import resolve

from ..views import *


class PostsListViewTest(TestCase):
    def test_posts_list_view_status_code(self):
        url = reverse('posts_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_posts_list_url_resolves_view(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, PostsList)


class TagsListViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('tags_list')
        self.tag1 = Tag.objects.create(title='python')
        self.tag2 = Tag.objects.create(title='django')

    def test_posts_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_posts_list_url_resolves_view(self):
        view = resolve('/tags/')
        self.assertEqual(view.func.view_class, TagsList)


class PostDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.tag = Tag.objects.create(title='python')
        self.post = Post.objects.create(title='new post', body='post body')
        self.post.tags.add(self.tag)

    def test_post_detail_view_success_status_code(self):
        url = reverse('post_detail', kwargs={'slug': self.post.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_not_found_status_code(self):
        url = reverse('post_detail', kwargs={'slug': 'qweqwe'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_posts_detail_url_resolves_post_detail_view(self):
        view = resolve('/post/new-post/')
        self.assertEqual(view.func.view_class, PostDetail)


class CreateTagViewTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_superuser(username='admin', email='admin@test.com', password='admin')
        self.url = reverse('tag_create')

    def test_create_tag_view_for_admin_user(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertIsInstance(form, TagCreateForm)

    def test_create_tag_view_permission_denied_for_non_admin_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_post_detail_url_resolves_view(self):
        view = resolve('/tags/create/')
        self.assertEqual(view.func.view_class, TagCreate)

    def test_create_tag_valid_post_data(self):
        self.client.login(username='admin', password='admin')
        data = {
            'title': 'django'
        }
        self.client.post(self.url, data)
        self.assertTrue(Tag.objects.exists())

    def test_create_tag_invalid_post_data(self):
        self.client.login(username='admin', password='admin')
        data = {}
        response = self.client.post(self.url, data)
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_create_tag_invalid_post_data_empty_fields(self):
        self.client.login(username='admin', password='admin')
        data = {
            'title': ''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tag.objects.exists())


class CreatePostViewTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_superuser(username='admin', email='admin@test.com', password='admin')
        self.url = reverse('post_create')
        self.tag = Tag.objects.create(title='python')

    def test_user_doesnt_have_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_post_detail_url_resolves_view(self):
        view = resolve('/post/create/')
        self.assertEqual(view.func.view_class, PostCreate)

    def test_create_post_view_for_admin(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertIsInstance(form, PostCreateForm)

    def test_create_post_valid_post_data(self):
        self.client.login(username='admin', password='admin')
        data = {
            'title': 'new title',
            'body': 'new body',
            'tags': [self.tag.pk]
        }
        self.client.post(self.url, data)
        self.assertTrue(Post.objects.exists())

    def test_create_post_invalid_post_data(self):
        self.client.login(username='admin', password='admin')
        data = {}
        response = self.client.post(self.url, data)
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_create_post_invalid_post_data_empty_fields(self):
        self.client.login(username='admin', password='admin')
        data = {
            'title': '',
            'body': '',
            'tags': ['']
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.exists())


class PostDeleteViewTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_superuser(username='admin', email='admin@test.com', password='admin')
        self.post = Post.objects.create(title='python', body='body')
        self.url = reverse('post_delete', kwargs={'slug': self.post.slug})

    def test_user_doesnt_have_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_post_delete_url_resolves_view(self):
        view = resolve('/post/delete/python/')
        self.assertEqual(view.func.view_class, PostDelete)

    def test_post_delete_success(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.exists())


class TagDeleteViewTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_superuser(username='admin', email='admin@test.com', password='admin')
        self.tag = Tag.objects.create(title='python')
        self.url = reverse('tag_delete', kwargs={'slug': self.tag.slug})

    def test_user_doesnt_have_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_post_delete_url_resolves_view(self):
        view = resolve('/tag/delete/python/')
        self.assertEqual(view.func.view_class, TagDelete)

    def test_post_delete_success(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tag.objects.exists())


class TagUpdateView(TestCase):
    def setUp(self) -> None:
        User.objects.create_superuser(username='admin', email='admin@test.com', password='admin')
        self.tag = Tag.objects.create(title='python')
        self.url = reverse('tag_update', kwargs={'slug': self.tag.slug})

    def test_user_doesnt_have_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_tag_update_url_resolves_view(self):
        view = resolve('/tag/edit/python/')
        self.assertEqual(view.func.view_class, TagUpdate)

    def test_tag_update_response_has_data(self):
        self.client.login(username='admin', password='admin')
        data = {
            'title': 'django'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.title, 'django')

    def test_tag_update_response_data_is_empty(self):
        self.client.login(username='admin', password='admin')
        data = {
            'title': ''
        }
        response = self.client.post(self.url, data)
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)


class PostUpdateView(TestCase):
    def setUp(self) -> None:
        User.objects.create_superuser(username='admin', email='admin@test.com', password='admin')
        self.tag1 = Tag.objects.create(title='python')
        self.tag2 = Tag.objects.create(title='django')
        self.post = Post.objects.create(title='new post', body='body')
        self.post.tags.add(self.tag1)
        self.url = reverse('post_update', kwargs={'slug': self.post.slug})

    def test_user_doesnt_have_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_tag_update_url_resolves_view(self):
        view = resolve('/post/edit/new-post/')
        self.assertEqual(view.func.view_class, PostUpdate)

    def test_tag_update_response_has_data(self):
        self.client.login(username='admin', password='admin')
        data = {
            'title': 'edit',
            'body': 'edit',
            'tags': [self.tag2.pk]
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'edit')
        self.assertEqual(self.post.body, 'edit')
        self.assertTrue(self.tag2 in self.post.tags.all())
        self.assertTrue(self.tag1 not in self.post.tags.all())

    def test_tag_update_response_data_is_empty(self):
        self.client.login(username='admin', password='admin')
        data = {
            'title': '',
            'body': '',
            'tags': ['']
        }
        response = self.client.post(self.url, data)
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)
