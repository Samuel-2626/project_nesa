from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from autoslug import AutoSlugField


def validate_image(image):
    file_size = image.file.size
    limit_kb = 50
    if file_size > 0.5*1024*1024:
        raise ValidationError("Max size of image is %s KB" % 500)

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
            .filter(status='published')


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    image = models.ImageField(
        upload_to='images/%Y/%m/%d', validators=[validate_image],)
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='article_posts', null=True)
    body = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='published')
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('articles:post_detail',
                       args=[self.created.year,
                             self.created.month,
                             self.created.day, self.slug])

    tags = TaggableManager()


class PostViews(models.Model):

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='post_views')
    host = models.CharField(max_length=500)
    ip = models.GenericIPAddressField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        unique_together = ['article', 'ip']

    def __str__(self):
        return self.ip


class PostLikesOrDislikes(models.Model):

    STATUS_CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )

    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='my_vote_articles', null=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='article_votes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Like or Dislike by {self.author} on {self.article}'


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='my_comments_for_article')

    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.author} on {self.article}'
