from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Notification(models.Model):

  user = models.ForeignKey(User, on_delete=models.CASCADE)

  message = RichTextUploadingField()

  date = models.DateTimeField(auto_now_add=True)

  class Meta:

    ordering = ('-date',) 





class Observer(models.Model):

  user = models.OneToOneField(User, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now=True)

  class Meta:

    ordering = ('-date',) 







