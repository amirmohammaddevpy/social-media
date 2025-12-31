from django import forms
from .models import Posts,Comment

class CreatPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('post','descriptions')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment':forms.TextInput(attrs={'class':'form-control','placeholder':'Write a comment...'})
        }