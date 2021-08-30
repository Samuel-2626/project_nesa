from django.contrib import admin
from .models import Blog

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'slug', 'created', 'author',)
  prepopulated_fields = {'slug': ('title',)}
  list_filter = ( 'created', 'author')
  search_fields = ('title', 'body')
  raw_id_fields = ('author',)
  date_hierarchy = 'created'
  ordering = ('created',)
