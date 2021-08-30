from django.contrib import admin
from .models import Profile, ProfileViews


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'reputation', 'university', 'faculty', 'department', 'level',
                    'photo', 'facebook_name', 'instagram_name', 'twitter_name', 'linkedin_name', 'website']


@admin.register(ProfileViews)
class ProfileViewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'host', 'ip', 'created')
    search_fields = ('profile',)
    raw_id_fields = ('profile',)
    date_hierarchy = 'created'
    ordering = ('-created',)
