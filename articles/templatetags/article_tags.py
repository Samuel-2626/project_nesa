from django import template
from django.db.models import Count

from ..models import Article


register = template.Library()


@register.simple_tag
def total_posts():
    return Article.published.count()


@register.inclusion_tag('article/post/latest_post.html')
def show_latest_posts(count=15):
    latest_posts = Article.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=15):
    return Article.published.annotate(
               total_comments=Count('comments')
           ).order_by('-total_comments')[:count]
