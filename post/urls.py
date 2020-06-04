from django.conf import settings
from django.urls import path

from . import views

app_name = 'post'

urlpatterns = [
    path('%s/add-post/' % settings.ADMIN_BASE_URL, views.add_post, name='add_post'),
    path('hashtag-list/', views.hashtag_list, name="hashtag_list")
]
