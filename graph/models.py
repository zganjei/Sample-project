from _ast import mod

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from ckeditor.fields import RichTextField

# Create your models here.
from django.forms import ModelForm


class Hashtag(models.Model):
    tag = models.CharField(blank=False, null=False, unique=True, max_length=255)


class Post(models.Model):
    title = models.CharField(blank=True, null=True, max_length=255)
    description = RichTextUploadingField(blank=True, null=True, config_name='default')
    hashtags = models.ManyToManyField(Hashtag)


class TestForm(ModelForm):
    class Meta:
        model = Post
        fields = ['description']
