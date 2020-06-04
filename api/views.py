from django.db.models import Count
from rest_framework import viewsets
from post.models import Post, Hashtag
from .serializers import PostSerializer, HashtagSerializer
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


class NewerPostList(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = (CustomTokenAuthentication,)
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    queryset = Post.objects.all().order_by('-created_on')

    # def get_queryset(self):
    #     k = 1
    #     return Post.objects.all()


class MostUsedTags(viewsets.ReadOnlyModelViewSet):
    serializer_class = HashtagSerializer

    queryset = Hashtag.objects.all().annotate(num_post=Count('post')).order_by('-num_post')[:7]


class PostListWithTag(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = (CustomTokenAuthentication,)
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    queryset = Post.objects.none()

    def get_queryset(self):
        postListOfQueryWithSpecificTag = Post.objects.none()
        if 'tag' in self.request.GET:
            tag = self.request.GET.get('tag')
            try:
                postListOfQueryWithSpecificTag = Hashtag.objects.get(tag=tag).post_set.all().order_by('-created_on')
            except Post.DoesNotExist:
                pass
        return postListOfQueryWithSpecificTag
