from django.db import models
from django.contrib.auth.models import User
from questions.models import Question


# Create your models here.

class FollowQuestion(models.Model):

  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_follow_question')
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='people_following')
  date = models.DateTimeField(auto_now_add=True)


  class Meta:
    ordering = ('-date',)
    unique_together = ['user', 'question']

  