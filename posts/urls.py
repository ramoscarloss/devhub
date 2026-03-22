from django.urls import path
from posts.views import feed, ini, create_post, post_detail

urlpatterns = [
    path('', ini, name='ini'),
    path('feed/', feed, name='feed'),
    path('feed/create', create_post, name='create_posts'),
    path('feed/<int:id>', post_detail, name="post_detail")
] 