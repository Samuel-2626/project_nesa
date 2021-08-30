from django.contrib import admin

from .models import Notification, Observer

# Register your models here.


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'message', 'date')
  list_filter = ('user', 'date')
  search_fields = ('user', 'message')
  raw_id_fields = ('user',)
  date_hierarchy = 'date'
  ordering = ('-date',)


@admin.register(Observer)
class ObserverAdmin(admin.ModelAdmin):
  list_display = ('id', 'user',  'date')
  list_filter = ('user', 'date')
  search_fields = ('user',)
  raw_id_fields = ('user',)
  date_hierarchy = 'date'
  ordering = ('-date',)
