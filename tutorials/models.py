import uuid

from django.db import models
from django.contrib.auth.models import User


from ckeditor_uploader.fields import RichTextUploadingField



class Institution(models.Model):

  """ A model to Capture the Institutions that has an Economics Department """

  name = models.CharField(max_length=500, unique=True)
  slug = models.SlugField(max_length=550)
  image = models.ImageField(upload_to='images/%Y/%m/%d')

  class Meta:
    ordering = ('name',)

  def __str__(self):
    return self.name


class Course(models.Model):

  """ A model to Capture the courses available for an Institution with an Economics Department """
  
  title = models.CharField(max_length=500)
  slug = models.SlugField(max_length=550)
  code = models.CharField(max_length=10)
  institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='courses')

  class Meta:
    ordering = ('code',)
    unique_together = [['title', 'institution']]

  def __str__(self):
    return f'{self.title} ({self.code})'


class Tutorial(models.Model):

  STATUS_MODE = (

    ('test', 'Test'),
    ('exam', 'Exam'),

  )

  STATUS_SESSION = (
    ('2021/2022', '2021/2022'),
    ('2020/2021', '2020/2021'),
    ('2019/2020', '2019/2020'),
    ('2018/2019', '2018/2019'),
    ('2017/2018', '2017/2018'),
    ('2016/2017', '2016/2017'),
    ('2015/2016', '2015/2016'),
    ('2014/2015', '2014/2015'),
    ('2013/2014', '2013/2014'),
    ('2012/2013', '2012/2013'),
    ('2011/2012', '2011/2012'),
    ('2010/2011', '2010/2011'),
    ('2009/2010', '2009/2010'),
    ('2008/2009', '2008/2009'),
    ('2007/2008', '2007/2008'),
    ('2006/2007', '2006/2007'),
    ('2005/2006', '2005/2006'),

  )

  """ A model to Capture the Tutorial for a particluar course """

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_tutorials')
  question = RichTextUploadingField()
  mode = models.CharField(max_length=20, choices=STATUS_MODE)
  session = models.CharField(max_length=20, choices=STATUS_SESSION)
  answer = RichTextUploadingField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tutorials')


  class Meta:
    ordering = ('-created',)

  def __str__(self):
    return f'Tutorial by {self.author} on {self.course}'


class Comment(models.Model):

  """ A model to Capture the Comment for a particluar tutorial """

  tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='tutorial_comments')
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_comments')
  comment = RichTextUploadingField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True)

  class Meta:
    ordering = ('created',)

  def __str__(self):
    return f'Comment by {self.author} on {self.tutorial}'




  

class Reply(models.Model):

  comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_replies')
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_replies')
  reply = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True)

  class Meta:
    ordering = ('created',)

  def __str__(self):
    return f'Reply by {self.author} on {self.comment}'
