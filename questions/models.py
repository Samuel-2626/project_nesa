import uuid

from django.db import models
from django.contrib.auth.models import User

from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


from django.shortcuts import reverse



class PublishedManager(models.Manager):
  def get_queryset(self):
    return super(PublishedManager, self).get_queryset()\
      .filter(status='published')



class Question(models.Model):

  STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
  )

  """ A Model To enable Authenticated Users to Post Ask Question """
  
  title = models.CharField(max_length=100, help_text='Maximum of 100 characters')
  slug = AutoSlugField(populate_from='title', unique=True)
  author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='my_questions', null=True)
  body = RichTextUploadingField(help_text="Explain your question")
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  counter = models.BigIntegerField(default=0)
  views = models.PositiveIntegerField(default=0)


  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

  tags = TaggableManager(help_text='A list of comma separated values. e.g healtheconomics, macroeconomics, etc.')

  class Meta:
    ordering = ('-created',)

  def __str__(self):
    return f'Qusetion by {self.author}'

  objects = models.Manager()
  published = PublishedManager()

  def get_absolute_url(self):
      return reverse("questions:question-detail", args=[self.slug])



class QuestionViews(models.Model):

  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_views')
  host = models.CharField(max_length=500)
  ip = models.GenericIPAddressField()
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('-created',)
    unique_together = ['question', 'ip']

  def __str__(self):
      return self.ip
  






# class CommentQuestion(models.Model):
#   question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_comments')
#   author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_question_comments')
#   comment = models.TextField()
#   created = models.DateTimeField(auto_now_add=True)
#   updated = models.DateTimeField(auto_now=True)
#   active = models.BooleanField(default=True)

#   class Meta:
#     ordering = ('created',)

#   def __str__(self):
#     return f'Comment by {self.author} on {self.question}'


class Answer(models.Model):
  
  STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
  )

  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
  author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='my_answers', null=True)
  answer = RichTextUploadingField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  accepted = models.BooleanField(default=False)
  counter = models.BigIntegerField(default=0)

  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


  class Meta:
    ordering = ('-counter',)
    unique_together = ['question', 'author']

  def __str__(self):
    return f'Answer by {self.author} on {self.question}'

  objects = models.Manager()
  published = PublishedManager()


class QuestionVotes(models.Model):

  STATUS_CHOICES = (
    ('upvote', 'Upvote'),
    ('downvote', 'Downvote'),
  )

  author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='my_vote_questions', null=True)
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='questions_votes')
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=10, choices=STATUS_CHOICES)

  class Meta:
    ordering = ('-created',)
 

  def __str__(self):
    return f'Vote by {self.author} on {self.question}'
    


class VoteAnswer(models.Model):

  STATUS_CHOICES = (
    ('upvote', 'Upvote'),
    ('downvote', 'Downvote'),
  )

  answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answers_votes')
  author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='my_vote_answers', null=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=10, choices=STATUS_CHOICES)


  class Meta:
    ordering = ('-created',)
    unique_together = ['answer', 'author']

  def __str__(self):
    return f'Vote by {self.author} on {self.answer}'



# class CommentAnswer(models.Model):
#   answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_comments')
#   author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_answer_comments')
#   comment = models.TextField()
#   created = models.DateTimeField(auto_now_add=True)
#   updated = models.DateTimeField(auto_now=True)
#   active = models.BooleanField(default=True)

#   class Meta:
#     ordering = ('created',)

#   def __str__(self):
#     return f'Comment by {self.author} on {self.answer}'

