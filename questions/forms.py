from django import forms
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
  class Meta:
    model = Question
    fields = ('title', 'body', 'tags')





class AnswerForm(forms.ModelForm):
  class Meta:
    model = Answer
    fields = ('answer',)


    

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
