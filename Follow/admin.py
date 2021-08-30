from django.contrib import admin
from .models import FollowQuestion

# Register your models here.


@admin.register(FollowQuestion)
class FollowQuestionAdmin(admin.ModelAdmin):

  list_display = ['id', 'user', 'question', 'date']
  search_fields = ['question',]
  ordering = ('-date',)