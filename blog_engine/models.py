from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Auto add slug when saving new model
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Auto add slug when saving new model
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag_posts_list', kwargs={'slug': self.slug})

