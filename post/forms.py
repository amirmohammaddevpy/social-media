from django import forms
from .models import Posts,Comment,ReportPost

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

class ReportPostForm(forms.ModelForm):
    class Meta:
        model = ReportPost
        fields = ('subject',)
        widgets = {
            'subject': forms.Textarea(attrs={
                'class': 'report-desc-input',
                'placeholder': 'Why are you reporting this post?',
                'rows': 4,
            }),
        }