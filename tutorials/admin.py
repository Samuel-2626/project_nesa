from django.contrib import admin

from .models import Institution, Course, Tutorial, Comment, Reply

# Register your models here.

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'slug', 'image')
  prepopulated_fields = {'slug': ('name',)}
  search_fields = ('name',)
  ordering = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = ('id','title', 'code', 'institution')
  prepopulated_fields = {'slug': ('title',)}
  search_fields = ('title', 'code')
  raw_id_fields = ('institution',)
  ordering = ('title',)


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
  list_display = ('id', 'author', 'session', 'course', 'created','updated')
  search_fields = ('question', 'answer')
  raw_id_fields = ('author','course')
  date_hierarchy = 'created'
  ordering = ('created',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ('id', 'created', 'updated', 'author','active')
  list_filter = ('active',)
  search_fields = ('comment', 'author')
  raw_id_fields = ('author',)
  date_hierarchy = 'created'
  ordering = ('created',)



@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
  list_display = ('id', 'created', 'updated', 'author','active')
  list_filter = ('active',)
  search_fields = ('comment', 'author')
  raw_id_fields = ('author',)
  date_hierarchy = 'created'
  ordering = ('created',)