from django import forms
from chapter.models import *

class EmailPostForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=100)
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','body']
