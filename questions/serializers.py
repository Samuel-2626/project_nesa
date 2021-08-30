from rest_framework import serializers
from .models import Question, QuestionVotes, Answer, VoteAnswer

from notification.models import Notification
from account.models import Profile


class QuestionSerializer(serializers.ModelSerializer):

  class Meta:
    model = Question
    fields = ('slug', 'counter', 'status')


class QuestionVoteSerializer(serializers.ModelSerializer):

  class Meta:
    model = QuestionVotes
    fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

  class Meta:
    model = Answer
    fields = ('counter', 'status', 'accepted')


class VoteAnswerSerializer(serializers.ModelSerializer):

  class Meta:
    model = VoteAnswer
    fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):

  class Meta:
    model = Notification
    fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

  class Meta:
    model = Profile
    fields = ('user', 'reputation')