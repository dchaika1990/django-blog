from django import forms
from .models import Comment
from django.forms import ModelForm


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label='Name')
    email = forms.EmailField(label='Email from')
    to = forms.EmailField(label='Email to')
    comments = forms.CharField(required=False, widget=forms.Textarea, label='Comments')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
