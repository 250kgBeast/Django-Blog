from django.test import TestCase

from ..forms import PostCreateForm
from ..models import Tag


class PostCreateFormTest(TestCase):
    def setUp(self) -> None:
        self.tag = Tag.objects.create(title='python')
        self.form_data = {
            'title': 'new title',
            'body': 'new body',
            'tags': (self.tag, ),
        }

    def test_post_create_form_is_valid(self):
        form = PostCreateForm(data=self.form_data)
        self.assertTrue(form.is_valid())
