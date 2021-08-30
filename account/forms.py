from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'university', 'faculty', 'department', 'level', 'photo',
                  'facebook_name', 'instagram_name', 'twitter_name', 'linkedin_name', 'website')


class MessageForm(forms.Form):
    message = forms.CharField(required=True, widget=forms.Textarea)
