from django.contrib import admin

from .models import Question, Answer, VoteAnswer, QuestionVotes, QuestionViews

# Register your models here.


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'author', 'created','updated', 'status', 'views', 'counter')
  list_filter = ('status', 'counter')
  search_fields = ('title', 'author')
  raw_id_fields = ('author',)
  date_hierarchy = 'created'
  ordering = ('-created',)


@admin.register(QuestionViews)
class QuestionViewsAdmin(admin.ModelAdmin):
  list_display = ('id', 'question', 'host', 'ip','created')
  search_fields = ('question',)
  raw_id_fields = ('question',)
  date_hierarchy = 'created'
  ordering = ('-created',)


@admin.register(QuestionVotes)
class QuestionVotesAdmin(admin.ModelAdmin):
  list_display = ('id', 'author', 'question', 'created','updated', 'status')
  list_filter = ('status',)
  search_fields = ('question', 'author')
  raw_id_fields = ('author',)
  date_hierarchy = 'created'
  ordering = ('-created',)


# @admin.register(CommentQuestion)
# class CommentQuestionAdmin(admin.ModelAdmin):
#   list_display = ('id', 'question', 'author', 'comment', 'created','updated', 'active')
#   list_filter = ('question', 'author', 'active')
#   search_fields = ('question', 'author', 'comment')
#   raw_id_fields = ('author', 'question')
#   date_hierarchy = 'created'
#   ordering = ('created',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
  list_display = ('id', 'question', 'author','created','updated', 'status', 'counter', 'accepted')
  list_filter = ('status', 'counter', 'accepted')
  search_fields = ('question', 'author')
  raw_id_fields = ('author', 'question', 'author')
  date_hierarchy = 'created'
  ordering = ('-created',)


@admin.register(VoteAnswer)
class VoteAnswerAdmin(admin.ModelAdmin):
  list_display = ('id', 'author', 'answer', 'created','updated', 'status')
  list_filter = ('status',)
  search_fields = ('answer', 'author')
  raw_id_fields = ('author',)
  date_hierarchy = 'created'
  ordering = ('-created',)


# @admin.register(CommentAnswer)
# class CommentAnswerAdmin(admin.ModelAdmin):
#   list_display = ('id', 'answer', 'author','created','updated', 'active')
#   list_filter = ('answer', 'author')
#   search_fields = ('answer', 'author')
#   raw_id_fields = ('author','answer')
#   date_hierarchy = 'created'
#   ordering = ('created',)