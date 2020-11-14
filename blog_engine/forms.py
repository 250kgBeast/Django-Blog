from django import forms

from .models import Post, Tag


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('title',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
