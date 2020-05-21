from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label='Name')
    email = forms.EmailField(label='Email from')
    to = forms.EmailField(label='Email to')
    comments = forms.CharField(required=False, widget=forms.Textarea, label='Comments')
