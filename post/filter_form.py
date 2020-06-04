from utils.forms import BaseFilterModelForm
from django import forms
from .models import Post


class PostFilterForm(BaseFilterModelForm):
    title = forms.CharField(label='عنوان')

    class Meta:
        model = Post
        fields = ('title',)
