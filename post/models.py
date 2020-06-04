from django.db import models

# Create your models here.
from django.forms import ModelForm
from ckeditor_uploader.fields import RichTextUploadingField
from django import forms

from utils.calverter import gregorian_to_jalali, gregorian_to_jalali_time


class Hashtag(models.Model):
    tag = models.CharField(blank=False, null=False, unique=True, max_length=255)


class Post(models.Model):
    title = models.TextField('عنوان')
    description = RichTextUploadingField('توضیحات', blank=True, null=True, config_name='default')
    brief = models.TextField('چکیده')
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    hashtags = models.ManyToManyField(Hashtag)
    image_preview = models.ImageField(verbose_name='عکس پیش نمایش پست', blank=True, null=True,
                                      upload_to='post-preview/%Y/%m/%d')

    @property
    def jalali_created_on(self):
        return gregorian_to_jalali_time(self.created_on)
