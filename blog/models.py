
from django.shortcuts import reverse

from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Blog(models.Model):

  title = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255, unique=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  body = RichTextUploadingField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ('-created',)

  def __str__(self):
      return self.title

  def get_absolute_url(self):
      return reverse("detail-blog", kwargs={"slug": self.slug})
  
  
