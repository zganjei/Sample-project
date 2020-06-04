from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'newerposts', views.NewerPostList)
router.register(r'posts-tag', views.PostListWithTag)
router.register(r'most-used-tags', views.MostUsedTags)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    # path('most-used-tags/', views.MostUsedTags.as_view()),
]
