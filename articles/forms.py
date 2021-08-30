from django import forms
from .models import Comment, Article


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('comment',)



class PostForm(forms.ModelForm):
  class Meta:
    model = Article
    fields = ('title', 'image', 'body', 'tags')

