from rest_framework import serializers

from .models import Article, PostLikesOrDislikes


class PostLikesOrDislikesSerializer(serializers.ModelSerializer):

  class Meta:

    model = PostLikesOrDislikes
    fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):

  class Meta:
    model = Article
    fields = ('likes', 'dislikes')