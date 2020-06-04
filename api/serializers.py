from rest_framework import serializers
from post.models import Post, Hashtag


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'brief', 'jalali_created_on', 'image_preview', 'description')


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('id', 'tag')
