from utils.forms import BaseModelForm
from utils.persian import arToPersianCharWithoutStripTags
from .models import Post, Hashtag
from django import forms
import re


class PostForm(BaseModelForm):
    exclude_from_clean = ['description']

    class Meta:
        model = Post
        fields = ['title', 'brief', 'image_preview', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'brief': forms.TextInput(attrs={'class': 'form-control'}),
        }

    class Media:
        js = ('post/post.js',)

    def clean(self):
        cd = super(PostForm, self).clean()
        for field in self.fields:
            if isinstance(self.fields[field], forms.CharField):
                value = cd.get(field)
                if value and isinstance(value, str):
                    cd[field] = arToPersianCharWithoutStripTags(value)

        return cd

    def save(self, commit=True):
        obj = super(PostForm, self).save(commit)
        listOfHashtages = set(re.findall(r"#(\w+)", obj.description))
        for hashtagText in listOfHashtages:
            hashtagModel = Hashtag.objects.get_or_create(tag=hashtagText)[0]
            obj.hashtags.add(hashtagModel)
