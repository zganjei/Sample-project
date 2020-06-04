from django.urls import path
from graph import views

urlpatterns = [
    path('', views.show_graph, name="show_graph"),
    path('render-post/', views.render_post, name="render_post"),
    path('hashtag/', views.hashtag, name="hashtag")
]
