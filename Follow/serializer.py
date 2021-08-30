from rest_framework import serializers
from .models import FollowQuestion

class FollowQuestionSerializer(serializers.ModelSerializer):

  class Meta:
    model = FollowQuestion
    fields = ('id', 'user', 'question', 'date')

