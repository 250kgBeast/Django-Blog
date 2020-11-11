from django.test import TestCase

from ..models import Post, Tag


class TestModels(TestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(title='Post1', slug='new_post1', body='body of the post1')
        self.tag1 = Tag.objects.create(title='python', slug='python')
        self.tag2 = Tag.objects.create(title='django', slug='django')

    def test_post_has_tag(self):
        self.post.tags.set([self.tag1.pk, self.tag2.pk])
        self.assertEqual(self.post.tags.count(), 2)

    def test_tag_has_post(self):
        self.tag1.posts.add(self.post)
        self.tag2.posts.add(self.post)
        self.assertEqual(self.post.tags.count(), 2)

    def test_post_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), f'/post/{self.post.slug}/')
        self.assertEqual(self.tag1.get_absolute_url(), f'/tag/{self.tag1.slug}/')
        self.assertEqual(self.tag2.get_absolute_url(), f'/tag/{self.tag2.slug}/')

    def test_model_str(self):
        self.assertEqual(str(self.post), 'Post1')
        self.assertEqual(str(self.tag1), 'python')
