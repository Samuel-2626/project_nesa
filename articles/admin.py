from django.contrib import admin
from .models import Article, Comment, PostLikesOrDislikes, PostViews


@admin.register(Article)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'created', 'author', 'status', 'views', 'likes', 'dislikes')
    list_filter = ('status', 'created', 'author')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ('status', 'created')


@admin.register(PostViews)
class PostViewsAdmin(admin.ModelAdmin):
  list_display = ('id', 'article', 'host', 'ip','created')
  search_fields = ('article',)
  raw_id_fields = ('article',)
  date_hierarchy = 'created'
  ordering = ('-created',)


@admin.register(PostLikesOrDislikes)
class PostLikesOrDislikesAdmin(admin.ModelAdmin):
  list_display = ('id', 'author', 'article', 'created','updated', 'status')
  list_filter = ('status',)
  search_fields = ('article', 'author')
  raw_id_fields = ('author',)
  date_hierarchy = 'created'
  ordering = ('-created',)



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment', 'created', 'updated', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')