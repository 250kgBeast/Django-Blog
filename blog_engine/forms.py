from django import forms

from .models import Post, Tag


class PostCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'class': 'form-control'}
        self.fields['body'].widget.attrs = {
            'class': 'form-control',
            'rows': 5,
            'cols': 15
        }
        self.fields['tags'] = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-label'})
        )

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')
